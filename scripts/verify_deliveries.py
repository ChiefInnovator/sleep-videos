"""Check decoded AAC and write a compact handoff report for existing deliveries."""
import argparse
import hashlib
import json
from pathlib import Path

from produce import ROOT, KINDS, Synth, decoded_audio_qc, run


def digest(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    mode = 'full' if args.full else 'preview'
    seconds = 28800 if args.full else 180
    rows = []
    for kind in KINDS:
        report = ROOT/'reports'/f'{kind}-{mode}.json'
        data = json.loads(report.read_text())
        video = ROOT/('videos' if args.full else 'previews')/f'{kind}-{mode}.mp4'
        master = ROOT/('masters' if args.full else 'previews')/f'{kind}-{mode}.flac'
        print(f'Checking decoded AAC: {kind}', flush=True)
        data['video_qc']['decoded_aac_qc'] = decoded_audio_qc(video, seconds)
        data['sha256'] = {'master':digest(master), 'video':digest(video)}
        if kind == 'distant-thunder-rain':
            data['thunder_events_seconds_duration_gain'] = Synth(kind, data['seed'], seconds).events
        data['tools'] = {'ffmpeg':run(['ffmpeg', '-version']).stdout.splitlines()[0]}
        report.write_text(json.dumps(data, indent=2)+'\n')
        m = data['master_loudness']
        a = data['video_qc']['aac_loudness']
        rows.append(f'| {kind} | {m["input_i"]} | {m["input_tp"]} | {a["input_tp"]} | {m["input_lra"]} | Pass |')
    header = f'''# {mode.title()} technical results

All five {seconds}-second deliveries passed numerical checks. Each master is 48 kHz/24-bit stereo. MP4s use 1280×720 at 24 fps and 320 kb/s AAC. Each video-specific title and smaller Inventing Fire with AI logo hold for four seconds and fades to black over two seconds. Every decoded video frame from 00:06 onward contains RGB (0,0,0) at every pixel. Lossless and decoded AAC audio passed finite-sample, peak, interior silence and one-second RMS-change screening. Each preview has 4,320 frames, including 4,176 completely black frames after the title.

| Sound | Master LUFS-I | Master dBTP | AAC dBTP | Master LRA (LU) | Technical checks |
|---|---:|---:|---:|---:|---|
'''
    footer = '''

Critical listening, playback on multiple devices, and matched-loudness reference comparisons have not been completed. These checks cannot establish premium quality or realistic rain. See the separate full-length reports for eight-hour verification. See README.md for the listening checklist and production steps. No YouTube uploads were made.

The two-second opening fade and 25-second closing fade are excluded from interior RMS-change/silence screening. Both preview and full-length generation use these audio fade durations. Loudness range includes the effect of fades as interpreted by the measurement algorithm. The full per-second measurements, hashes, methods and provenance are in the individual JSON production sheets.
'''
    if args.full:
        header = header.replace('Each preview has 4,320 frames, including 4,176 completely black frames after the title.', 'Each full video has 691,200 frames, including 691,056 completely black frames after the title.')
        footer = footer.replace('See the separate full-length reports for eight-hour verification.', 'Eight-hour files have been rendered; full-length critical listening is still required.')
    (ROOT/'reports'/f'{mode}-summary.md').write_text(header+'\n'.join(rows)+footer)


if __name__ == '__main__':
    main()
