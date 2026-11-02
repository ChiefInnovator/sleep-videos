"""Original procedural audio, constant-gain mastering, black video, and decoded QC.

Run from the project folder; see README.md for the listening gate and limitations.
"""
import argparse
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parents[1]
SR = 48000
KINDS = ['white-noise', 'distant-thunder-rain', 'rain-on-window', 'brown-noise', 'ambient-drone']
TARGETS = [-25, -26, -27, -27, -28]
TITLE_SECONDS = 6
FADE_IN_SECONDS = 2
FADE_OUT_SECONDS = 25
METHODS = [
    'Gaussian broadband noise; 11 kHz second-order low-pass for comfort; shared center and restrained independent sides. Softened white noise, not mathematically pure white noise.',
    'Continuous filtered Gaussian rain layers at 180-8500 Hz and 800-6500 Hz, slow random intensity drift; newly synthesized band-limited thunder with irregular 29-67 second gaps, 10-19 second smooth envelopes and restrained stereo width.',
    'Synthetic indoor rain bed at 350-5800 Hz; randomized noise-burst droplets through a 1300-6500 Hz band, with smooth 25-95 ms envelopes and fixed gentle stereo placement; no external recordings.',
    'Leaky integration of Gaussian noise, 30 Hz high-pass for DC/subsonic control plus a 60 Hz high-pass to restrain low-bass energy surges, 1800 Hz low-pass; stable shared center and restrained independent sides. Fixed frequency shaping only, with no dynamic compression.',
    'Original sustained D/A harmonic pad at 73.416, 110, 146.832, 220 and 293.664 Hz with gentle upper partials and independent very slow phase/amplitude evolution. No binaural beat design, percussion, melody or external samples.'
]


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True)


def measure(path):
    result = run(['ffmpeg', '-hide_banner', '-nostdin', '-i', str(path), '-vn',
                  '-af', 'ebur128=peak=true:framelog=verbose', '-f', 'null', '-'])
    summary = result.stderr.rsplit('Summary:', 1)[-1]
    def value(pattern):
        match = re.search(pattern, summary)
        if not match:
            raise RuntimeError('Missing EBU R128 measurement')
        return match.group(1)
    return {'input_i':value(r'\bI:\s+([-\d.]+) LUFS'),
            'input_tp':value(r'Peak:\s+([-\d.]+) dBFS'),
            'input_lra':value(r'LRA:\s+([-\d.]+) LU'),
            'input_thresh':value(r'Threshold:\s+([-\d.]+) LUFS'),
            'analyzer':'FFmpeg ebur128 with true-peak analysis; summary precision 0.1 dB. No normalization applied.'}


class Synth:
    def __init__(self, kind, seed, seconds):
        self.kind = kind
        self.rng = np.random.default_rng(seed)
        self.state = {}
        self.events = []
        event_rng = np.random.default_rng(seed + 10000)
        t = 34.0
        if kind == 'distant-thunder-rain':
            while t < seconds:
                duration = event_rng.uniform(10, 19)
                self.events.append((t, duration, event_rng.uniform(.10, .18)))
                t += duration + event_rng.uniform(29, 67)
        self.next_drop = 0.0
        self.drops = []
        knots = np.arange(-45, seconds + 90, 45)
        self.knots = knots
        self.drift = event_rng.uniform(.94, 1.06, len(knots))

    def filt(self, key, x, frequencies, kind='bandpass', order=2):
        if key not in self.state:
            sos = butter(order, frequencies, btype=kind, fs=SR, output='sos')
            self.state[key] = [sos, np.zeros((len(sos), 2, x.shape[1]))]
        sos, zi = self.state[key]
        y, self.state[key][1] = sosfilt(sos, x, axis=0, zi=zi)
        return y

    def noise(self, n):
        z = self.rng.normal(size=(n, 3))
        return .85 * z[:, :1] + .35 * z[:, 1:]

    def block(self, start, n):
        t = (start + np.arange(n)) / SR
        k = self.kind
        if k == 'white-noise':
            y = self.filt('white', self.noise(n), 11000, 'lowpass') * .1
        elif k == 'brown-noise':
            y = self.filt('integrator', self.noise(n), 8, 'lowpass')
            y = self.filt('subsonic', y, 30, 'highpass')
            y = self.filt('bass_surges', y, 60, 'highpass')
            y = self.filt('brown_top', y, 1800, 'lowpass') * 9
        elif k == 'distant-thunder-rain':
            y = self.filt('rain', self.noise(n), [180, 8500]) * .07
            y += self.filt('near', self.noise(n), [800, 6500]) * .025
            y *= np.interp(t, self.knots, self.drift)[:, None]
            rumble = self.filt('thunder', self.noise(n), [35, 240])
            for begin, duration, gain in self.events:
                if begin < t[-1] and begin + duration > t[0]:
                    u = np.clip((t - begin) / duration, 0, 1)
                    env = np.sin(np.pi * u) ** 2
                    y += rumble * (gain * env)[:, None]
        elif k == 'rain-on-window':
            y = self.filt('exterior', self.noise(n), [350, 5800]) * .05
            texture = self.filt('glass', self.noise(n), [1300, 6500])
            end = (start + n) / SR
            while self.next_drop < end:
                self.drops.append((self.next_drop, self.rng.uniform(.025, .095),
                                   self.rng.uniform(.004, .016), self.rng.uniform(.35, .65)))
                self.next_drop += self.rng.exponential(.026)
            envelope = np.zeros((n, 2))
            for begin, duration, gain, pan in self.drops:
                a = max(0, int((begin - start / SR) * SR))
                b = min(n, math.ceil((begin + duration - start / SR) * SR))
                if b > a:
                    u = np.clip((t[a:b] - begin) / duration, 0, 1)
                    envelope[a:b] += (np.sin(np.pi * u) ** 2 * gain)[:, None] * np.array([1-pan, pan])
            self.drops = [e for e in self.drops if e[0] + e[1] > end]
            y += texture * envelope
            y *= np.interp(t, self.knots, self.drift)[:, None]
        else:
            y = np.zeros((n, 2))
            for i, hz in enumerate([73.416, 110, 146.832, 220, 293.664]):
                phase = 2*np.pi*hz*t + .13*np.sin(2*np.pi*t/(113+i*37) + i)
                amp = .025 / (1+i*.55) * (1 + .12*np.sin(2*np.pi*t/(149+i*53)+i))
                for channel in range(2):
                    p = phase + channel*.08*np.sin(2*np.pi*t/(181+i*23)+i)
                    y[:, channel] += amp * (np.sin(p) + .10*np.sin(2*p+i) + .025*np.sin(3*p))
        return y


def generate(kind, seed, seconds, path):
    synth = Synth(kind, seed, seconds)
    # Settle filter startup before the opening fade. Negative-time samples are discarded.
    synth.block(-SR*2, SR*2)
    total = seconds * SR
    with sf.SoundFile(path, 'w', samplerate=SR, channels=2, subtype='PCM_24', format='FLAC') as out:
        for start in range(0, total, SR*5):
            n = min(SR*5, total-start)
            y = synth.block(start, n)
            pos = start + np.arange(n)
            fade = np.minimum(np.clip(pos/(FADE_IN_SECONDS*SR), 0, 1),
                              np.clip((total-1-pos)/(FADE_OUT_SECONDS*SR), 0, 1))
            y *= (.5-.5*np.cos(np.pi*fade))[:, None]
            if not np.isfinite(y).all() or np.max(np.abs(y)) >= .98:
                raise RuntimeError('Unsafe synthesis amplitude')
            out.write(y)


def audio_qc(path, seconds):
    maximum = 0.0
    square = 0.0
    count = 0
    dc = np.zeros(2)
    levels = []
    max_boundary_step = 0.0
    previous = None
    with sf.SoundFile(path) as f:
        assert f.samplerate == SR and f.channels == 2 and f.subtype == 'PCM_24'
        assert len(f) == seconds * SR
        for block in f.blocks(blocksize=SR):
            assert np.isfinite(block).all()
            maximum = max(maximum, float(np.max(np.abs(block))))
            square += float(np.sum(block**2))
            dc += block.sum(axis=0)
            count += len(block)
            levels.append(float(20*np.log10(max(np.sqrt(np.mean(block**2)), 1e-15))))
            if previous is not None:
                max_boundary_step = max(max_boundary_step, float(np.max(np.abs(block[0]-previous))))
            previous = block[-1]
    interior = levels[FADE_IN_SECONDS:-FADE_OUT_SECONDS]
    assert maximum < 1 and min(interior) > -65
    jumps = np.abs(np.diff(interior))
    assert float(max(jumps)) < 3, 'Abrupt one-second RMS change requires investigation'
    return {'sample_peak_dbfs':20*np.log10(maximum), 'dc_mean':(dc/count).tolist(),
            'rms_dbfs':20*np.log10(np.sqrt(square/(count*2))),
            'interior_one_second_rms_min_dbfs':min(interior),
            'interior_one_second_rms_max_dbfs':max(interior),
            'largest_interior_one_second_rms_change_db':float(max(jumps)),
            'one_second_rms_dbfs':levels, 'block_boundary_max_sample_step':max_boundary_step,
            'limitations':'Numerical screening cannot establish absence of audible clicks, repetition, or unnatural texture.'}


def video(master, output, seconds, kind, efficient=False):
    if efficient:
        from efficient_video import render
        return render(master, output, seconds, kind)
    run(['ffmpeg', '-y', '-hide_banner', '-nostdin', '-filter_complex_threads', '1', '-loop', '1', '-framerate', '24',
         '-t', str(TITLE_SECONDS), '-i', str(ROOT/'assets/inventing-fire-title.png'),
         '-f', 'lavfi', '-i', f'color=c=black:s=1280x720:r=24:d={seconds-TITLE_SECONDS}',
         '-i', str(master), '-loop', '1', '-framerate', '24',
         '-t', str(TITLE_SECONDS), '-i', str(ROOT/f'assets/{kind}-text.png'), '-filter_complex',
         '[0:v]scale=400:225,setsar=1[logo];'
         '[3:v][logo]overlay=x=440:y=380,format=yuv420p,fade=t=out:st=4:d=2[title];'
         '[title][1:v]concat=n=2:v=1:a=0[v]', '-map', '[v]', '-map', '2:a',
         '-t', str(seconds), '-c:v', 'libx264', '-threads:v', '2', '-preset', 'ultrafast', '-crf', '18',
         '-force_key_frames', str(TITLE_SECONDS),
         '-pix_fmt', 'yuv420p', '-color_range', 'tv', '-colorspace', 'bt709',
         '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'aac', '-b:a', '320k',
         '-ar', str(SR), '-movflags', '+faststart', str(output)])


def video_qc(path, seconds, report):
    probe = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)]).stdout)
    assert float(probe['format']['duration']) <= seconds
    v = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    assert int(v['nb_frames']) == seconds*24
    # Full renders compare every RGB byte in memory, avoiding expensive per-frame MD5.
    if seconds > 180:
        checked = json.loads(run([str(ROOT/'.venv/bin/verify-black-frames'), str(path),
                                  str(seconds*24), str(TITLE_SECONDS*24)]).stdout)
        frame_count = checked['decoded_rgb_frames']
        pixel_check = 'Every decoded RGB byte compared directly against zero using verify_black_frames.c.'
    else:
        hashes = report.with_suffix('.rgb-framemd5')
        run(['ffmpeg', '-y', '-v', 'error', '-nostdin', '-threads', '2', '-filter_threads', '1',
             '-i', str(path), '-map', '0:v:0', '-threads:v', '2',
             '-pix_fmt', 'rgb24', '-f', 'framemd5', str(hashes)])
        expected = hashlib.md5(bytes(1280*720*3)).hexdigest()
        lines = [line for line in hashes.read_text().splitlines() if line and not line.startswith('#')]
        assert len(lines) == seconds*24
        assert lines[0].split(',')[-1].strip() != expected, 'Opening title is missing'
        assert all(line.split(',')[-1].strip() == expected for line in lines[TITLE_SECONDS*24:])
        frame_count = len(lines)
        pixel_check = 'Every decoded RGB frame hash compared against an all-zero RGB frame.'
    result = measure(path)
    assert float(result['input_tp']) <= -2
    decoded = decoded_audio_qc(path, seconds)
    return {'duration':probe['format']['duration'], 'decoded_rgb_frames':frame_count,
            'pixel_verification':pixel_check,
            'title_seconds':TITLE_SECONDS, 'title_hold_seconds':4, 'title_fade_seconds':2,
            'every_rgb_pixel_zero_after_seconds':TITLE_SECONDS,
            'black_frame_count':frame_count-TITLE_SECONDS*24,
            'aac_loudness':result, 'decoded_aac_qc':decoded, 'probe':probe}


def decoded_audio_qc(path, seconds):
    temporary = path.with_suffix('.decoded.flac')
    try:
        # Decode the entire audible presentation, discarding only AAC end padding beyond the container duration.
        run(['ffmpeg', '-y', '-v', 'error', '-xerror', '-nostdin', '-i', str(path), '-map', '0:a:0',
             '-t', str(seconds), '-c:a', 'flac', '-sample_fmt', 's32', '-bits_per_raw_sample', '24', str(temporary)])
        return audio_qc(temporary, seconds)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--listening-reviewed', action='store_true', help='Only after the documented preview listening checks have passed')
    parser.add_argument('--render-without-listening-review', action='store_true',
                        help='Explicitly requested full render with listening review still pending')
    parser.add_argument('--only', choices=KINDS)
    parser.add_argument('--resume', action='store_true', help='Reuse complete files from an interrupted render; all quality checks still run')
    parser.add_argument('--efficient-video', action='store_true', help='Full renders: reuse encoded black frames and use macOS AudioToolbox AAC')
    args = parser.parse_args()
    if args.efficient_video and not args.full:
        parser.error('--efficient-video is intended for full eight-hour renders.')
    if args.full and not (args.listening_reviewed or args.render_without_listening_review):
        parser.error('Complete preview listening evaluation first; see README.md.')
    seconds = 28800 if args.full else 180
    for index, kind in enumerate(KINDS):
        if args.only and kind != args.only:
            continue
        mode = 'full' if args.full else 'preview'
        folder = ROOT / ('masters' if args.full else 'previews')
        folder.mkdir(exist_ok=True)
        raw = folder / f'{kind}-{mode}-unmastered.flac'
        master = folder / f'{kind}-{mode}.flac'
        output = (ROOT/'videos' if args.full else folder) / f'{kind}-{mode}.mp4'
        report = ROOT/'reports'/f'{kind}-{mode}.json'
        output.parent.mkdir(parents=True, exist_ok=True)
        report.parent.mkdir(parents=True, exist_ok=True)
        print(f'{kind}: synthesizing {seconds} seconds', flush=True)
        def complete_audio(path):
            if not args.resume or not path.exists():
                return False
            try:
                info = sf.info(path)
                return info.frames == seconds*SR and info.samplerate == SR and info.channels == 2 and info.subtype == 'PCM_24'
            except (RuntimeError, sf.LibsndfileError):
                return False
        if not complete_audio(raw):
            generate(kind, 9142026+index, seconds, raw)
        initial = measure(raw)
        gain = min(TARGETS[index]-float(initial['input_i']), -3-float(initial['input_tp']))
        if not complete_audio(master):
            run(['ffmpeg', '-y', '-v', 'error', '-nostdin', '-i', str(raw), '-af', f'volume={gain}dB',
                 '-c:a', 'flac', '-sample_fmt', 's32', '-bits_per_raw_sample', '24', str(master)])
        mastered = measure(master)
        assert float(mastered['input_tp']) <= -2
        qc = audio_qc(master, seconds)
        print(f'{kind}: encoding and verifying every black frame', flush=True)
        reuse_video = False
        if args.resume and output.exists():
            try:
                existing = json.loads(run(['ffprobe', '-v', 'error', '-show_format', '-of', 'json', str(output)]).stdout)
                reuse_video = float(existing['format']['duration']) == seconds
            except (subprocess.CalledProcessError, KeyError, ValueError):
                pass
        if not reuse_video:
            video(master, output, seconds, kind, efficient=args.efficient_video)
        vqc = video_qc(output, seconds, report)
        data = {'kind':kind, 'mode':mode, 'seconds':seconds, 'sample_rate':SR, 'bits':24,
                'seed':9142026+index, 'method':METHODS[index],
                'provenance':'Original procedural synthesis using scripts/produce.py. No recordings, reference audio, samples, or third-party music used.',
                'license_notes':'No third-party source-audio license is needed; this statement is provenance, not a legal determination of copyright eligibility.',
                'fade_in_seconds':FADE_IN_SECONDS, 'fade_out_seconds':FADE_OUT_SECONDS,
                'constant_gain_db':gain, 'target_lufs':TARGETS[index],
                'video_encoding':('Reused existing H264/AAC MP4; encoding was not repeated.' if reuse_video else 'H264 picture segments copied; continuous AudioToolbox AAC at requested 320 kb/s, quality 0.' if args.efficient_video else 'Continuous libx264 video and native AAC at requested 320 kb/s.'),
                'master_loudness':mastered, 'audio_qc':qc, 'video_qc':vqc,
                'listening_review':'Not performed by the agent; no audio-listening tool is available.',
                'reference_comparison':'Not performed; usable reference audio unavailable in the browsing tool.',
                'youtube_transcode_check':'Not performed; no upload requested.',
                'status':'Technical checks passed; critical listening remains required.'}
        report.write_text(json.dumps(data, indent=2)+'\n')
        raw.unlink()
        print(f'{kind}: PASS {mastered["input_i"]} LUFS, {mastered["input_tp"]} dBTP', flush=True)


if __name__ == '__main__':
    main()
