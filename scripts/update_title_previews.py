"""Rebuild the five preview videos with the branded opening, retaining audio masters."""
import json
from produce import ROOT, KINDS, video, video_qc, run

for kind in KINDS:
    print(f'{kind}: adding branded title and verifying', flush=True)
    folder = ROOT/'previews'
    target = folder/f'{kind}-preview.mp4'
    temporary = folder/f'{kind}-preview.branded.mp4'
    report = ROOT/'reports'/f'{kind}-preview.json'
    data = json.loads(report.read_text())
    video(folder/f'{kind}-preview.flac', temporary, data['seconds'], kind)
    qc = video_qc(temporary, data['seconds'], report)
    temporary.replace(target)
    run(['ffmpeg', '-y', '-v', 'error', '-i', str(target), '-frames:v', '1',
         str(ROOT/f'assets/{kind}-title.png')])
    qc['probe']['format']['filename'] = str(target)
    data['video_qc'] = qc
    data.pop('sha256', None)
    data['visual_revision'] = 'Video-specific title with smaller Inventing Fire with AI logo: hold four seconds, fade two seconds, then pure black. Included in existing runtime.'
    report.write_text(json.dumps(data, indent=2)+'\n')
    print(f'{kind}: PASS', flush=True)
