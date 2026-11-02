"""Re-encode committed deliveries from their FLAC masters at a Git-friendly AAC bitrate."""
import argparse
import json

from produce import ROOT, KINDS, video, video_qc, run
from verify_deliveries import digest

MAX_BYTES = 1_000_000_000


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--only', choices=KINDS)
    parser.add_argument('--bitrate', default='160k')
    args = parser.parse_args()
    mode = 'full' if args.full else 'preview'
    seconds = 28800 if args.full else 180
    has_aac_at = ' aac_at ' in run(['ffmpeg', '-hide_banner', '-encoders']).stdout
    if args.full and not has_aac_at:
        parser.error('--full uses the AudioToolbox encoder (aac_at), which this FFmpeg lacks.')
    for kind in KINDS:
        if args.only and kind != args.only:
            continue
        master = ROOT/('masters' if args.full else 'previews')/f'{kind}-{mode}.flac'
        target = ROOT/('videos' if args.full else 'site/media')/f'{kind}-{mode}.mp4'
        temporary = target.with_suffix('.tmp.mp4')
        report = ROOT/'reports'/f'{kind}-{mode}.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        print(f'{kind}: encoding {args.bitrate} from {master.relative_to(ROOT)}', flush=True)
        try:
            video(master, temporary, seconds, kind, efficient=args.full, bitrate=args.bitrate)
            size = temporary.stat().st_size
            if size > MAX_BYTES:
                raise SystemExit(f'{kind}: {size} bytes exceeds the {MAX_BYTES}-byte limit')
            qc = video_qc(temporary, seconds, report)
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
        qc['probe']['format']['filename'] = str(target)
        data = json.loads(report.read_text())
        data.pop('sha256', None)
        data['video_qc'] = qc
        encoder = 'aac_at' if args.full else 'aac'
        data['video_encoding'] = (f'Re-encoded from the FLAC master by scripts/compress_videos.py: '
                                  f'{"H264 picture segments copied; continuous AudioToolbox" if args.full else "libx264 video and native"} '
                                  f'AAC at requested {args.bitrate}.')
        data['delivery'] = {'bitrate':args.bitrate, 'encoder':encoder, 'bytes':size,
                            'sha256':digest(target), 'path':str(target.relative_to(ROOT))}
        report.write_text(json.dumps(data, indent=2)+'\n')
        print(f'{kind}: PASS {size} bytes', flush=True)


if __name__ == '__main__':
    main()
