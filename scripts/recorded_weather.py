"""Sequence licensed field recordings at their native speed and cadence."""
import hashlib
import json
import subprocess
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

ROOT = Path(__file__).resolve().parents[1]


def sources(kind):
    items = json.loads((ROOT/'assets/recordings/sources.json').read_text())['sources']
    roles = {'window', 'rain'} if kind == 'rain-on-window' else {'storm', 'rain'}
    selected = [item for item in items if item['role'] in roles]
    if any(s['license'] not in {'CC0-1.0', 'Public-Domain', 'CC-BY-3.0', 'CC-BY-4.0'} for s in selected):
        raise RuntimeError('Unsupported recording license in source bank')
    return selected


def credits(kind):
    return 'Weather recording source bank: ' + '; '.join(
        f"{s['creator']} — {s.get('title', s['id'])} — {s['source_url']} — {s['license']} {s['license_url']}"
        for s in sources(kind)) + '. Changes: excerpts, resampling, fixed EQ/level adjustment, quiet-rain crossfades.'


@lru_cache(maxsize=16)
def load(source_id, sample_rate, window=False):
    item = next(s for s in json.loads((ROOT/'assets/recordings/sources.json').read_text())['sources']
                if s['id'] == source_id)
    path = ROOT/'assets/recordings'/item['file']
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise RuntimeError(f'Recording checksum mismatch: {path.name}')
    result = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-i', str(path),
                             '-map', '0:a:0', '-ac', '2', '-ar', str(sample_rate), '-f', 'f32le', '-'],
                            check=True, capture_output=True)
    x = np.frombuffer(result.stdout, dtype='<f4').reshape(-1, 2).copy()
    if window:
        # Restrain coastal wind and soften glass detail with fixed EQ only.
        x = sosfilt(butter(2, [180, 6500], btype='bandpass', fs=sample_rate, output='sos'), x, axis=0).astype(np.float32)
    x -= x.mean(axis=0, dtype=np.float64)
    assert np.isfinite(x).all() and len(x) > sample_rate*4
    levels = np.array([np.sqrt(np.mean(x[i:i+sample_rate].astype(float)**2))
                       for i in range(0, len(x)-sample_rate+1, sample_rate)])
    ambient = max(float(np.percentile(levels, 30)), 1e-6)
    return x, levels, ambient


class RecordedWeather:
    def __init__(self, kind, seed, seconds, sample_rate=48000):
        self.sr = sample_rate
        self.kind = kind
        self.scenes = []
        rng = np.random.default_rng(seed)
        items = [s for s in sources(kind) if s['role'] != 'rain']
        rain = next(s for s in sources(kind) if s['role'] == 'rain')
        rain_audio, rain_levels, _ = load(rain['id'], self.sr)
        # Match the natural rain level at both loop edges so a quiet floor does not surge on wrap.
        rain_db = 20*np.log10(np.maximum(rain_levels, 1e-12))
        loops = [(a, b) for a in range(len(rain_levels)-12)
                 for b in range(a+12, len(rain_levels)+1)
                 if np.max(np.abs(np.diff(rain_db[a:b]))) < 1.5
                 and abs(float(np.mean(rain_db[a:a+2])-np.mean(rain_db[b-2:b]))) < .5]
        if not loops:
            raise RuntimeError('Recorded rain has no level-matched quiet loop')
        a, b = max(loops, key=lambda pair:pair[1]-pair[0])
        self.rain = rain_audio[a*self.sr:b*self.sr]
        if kind == 'rain-on-window':
            self.rain = sosfilt(butter(2, 2500, btype='lowpass', fs=self.sr, output='sos'), self.rain, axis=0).astype(np.float32)
        ambient = max(float(np.sqrt(np.mean(self.rain.astype(float)**2))), 1e-6)
        self.rain_gain = (.022 if kind == 'rain-on-window' else .008)/ambient
        self.rain_metadata = {'recording_id':rain['id'], 'source_range_seconds':[a, b],
                              'gain':self.rain_gain, 'crossfade_seconds':2}
        position = 0
        previous = None
        while position < seconds*self.sr:
            available = [s for s in items if s['id'] != previous] or items
            if kind == 'distant-thunder-rain' and not self.scenes:
                item = next(s for s in items if s['id'] == 'thunder-fission9')
            else:
                item = available[int(rng.integers(len(available)))]
            x, levels, ambient = load(item['id'], self.sr, kind == 'rain-on-window')
            # Quiet cut candidates require three low-energy seconds and distance from loud peals.
            quiet = levels < np.percentile(levels, 45)
            loud = levels > max(ambient*3, float(np.percentile(levels, 90)))
            guard = np.convolve(loud.astype(int), np.ones(17, dtype=int), mode='full')[8:8+len(levels)]
            stable = np.convolve(quiet.astype(int), np.ones(3, dtype=int), mode='full')[1:1+len(levels)] == 3
            points = np.flatnonzero(stable & (guard == 0))
            start, end = 0, len(x)
            minimum, maximum = (3, 10) if kind == 'rain-on-window' else (60, 240)
            if kind == 'rain-on-window':
                # This coastal recording includes gusts. Curate genuinely quiet window passages,
                # retaining their captured droplets rather than synthesizing or compressing taps.
                db = 20*np.log10(np.maximum(levels, 1e-12))
                ceiling = np.percentile(levels, 65)
                pairs = [(a, b) for a in range(1, len(levels)-minimum)
                         for b in range(a+minimum, min(len(levels), a+maximum+1))
                         if np.max(np.abs(np.diff(db[a:b]))) < 1.5
                         and levels[a] < ceiling and levels[b-1] < ceiling]
                if not pairs:
                    raise RuntimeError('No calm window-rain passages in recording')
                a, b = pairs[int(rng.integers(len(pairs)))]
                start, end = int(a*self.sr), int(b*self.sr)
            elif len(x) > self.sr*maximum and len(points) > 1:
                pairs = [(a, b) for a in points for b in points if minimum <= b-a <= maximum]
                if pairs:
                    a, b = pairs[int(rng.integers(len(pairs)))]
                    start, end = int(a*self.sr), int(b*self.sr)
            # Preserve the full decay: if the file ends on an active peal, stop at an earlier quiet cut.
            quiet_ceiling = max(ambient*2, float(np.max(levels))*.05)
            if kind == 'distant-thunder-rain' and end == len(x) and levels[-1] > quiet_ceiling:
                ends = points[points*self.sr > start+self.sr*5]
                if len(ends):
                    end = int(ends[-1]*self.sr)
                else:
                    raise RuntimeError(f"Recording has no quiet ending: {item['id']}")
            length = end-start
            peak = max(float(np.max(np.abs(x[start:end]))), 1e-6)
            reference = max(float(np.sqrt(np.mean(x[start:end].astype(float)**2))), 1e-6) if kind == 'rain-on-window' else ambient
            gain = min((.012 if kind == 'rain-on-window' else .014)/reference, .32/peak)
            # Thunder scenes never overlap. Continuous window rain uses quiet complementary fades.
            fade = int(min(2, length/self.sr/2)*self.sr) if kind == 'rain-on-window' else int(min(.2, length/self.sr/10)*self.sr)
            self.scenes.append({'recording_id':item['id'], 'begin_sample':position,
                                'source_start_sample':start, 'frames':length,
                                'gain':gain, 'edge_fade_samples':fade})
            position += length-(fade if kind == 'rain-on-window' else 0)
            previous = item['id']

    def block(self, start, n):
        sr = self.sr
        absolute = start + np.arange(n)
        # A quiet, genuinely recorded rain floor bridges scene edges; it contains no thunder.
        span = len(self.rain)-sr*2
        phase = absolute % span
        base = self.rain[phase].astype(float)
        edge = phase < sr*2
        if edge.any():
            u = phase[edge]/(sr*2)
            base[edge] = (self.rain[phase[edge]]*np.sin(np.pi*u/2)[:, None]
                          + self.rain[phase[edge]+span]*np.cos(np.pi*u/2)[:, None])
        y = base*self.rain_gain
        for scene in self.scenes:
            begin, length = scene['begin_sample'], scene['frames']
            a, b = max(0, begin-start), min(n, begin+length-start)
            if b <= a:
                continue
            age = start+np.arange(a, b)-begin
            offset = scene['source_start_sample']+age
            x, _, _ = load(scene['recording_id'], sr, self.kind == 'rain-on-window')
            fade = scene['edge_fade_samples']
            envelope = np.minimum(np.clip(age/fade, 0, 1), np.clip((length-1-age)/fade, 0, 1))
            shape = .5-.5*np.cos(np.pi*envelope)
            y[a:b] += x[offset]*(scene['gain']*shape)[:, None]
        # Fixed headroom; final mastering uses a single constant gain.
        return y*.25

    def metadata(self):
        return {'timing':('Native timing within recordings; no independently triggered or overlapping thunder clips.'
                          if self.kind == 'distant-thunder-rain' else 'Native window rain passages with quiet complementary crossfades.'),
                'segment_count':len(self.scenes), 'sample_rate':self.sr,
                'segments':self.scenes, 'source_bank':sources(self.kind),
                'rain_floor':self.rain_metadata,
                'reuse':'Finite field recordings are reused in varied passage order; this is a constructed eight-hour mix.'}
