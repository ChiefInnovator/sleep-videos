"""Encode the short title and black picture once, then mux continuous audio."""
import math
from pathlib import Path
import subprocess
import tempfile


def render(master, output, seconds, kind):
    root = Path(__file__).resolve().parents[1]
    def run(args):
        return subprocess.run(['ffmpeg', '-y', '-v', 'error', '-nostdin', *args],
                              check=True, capture_output=True, text=True)
    picture = ['-c:v', 'libx264', '-threads:v', '2', '-preset', 'ultrafast',
               '-crf', '18', '-pix_fmt', 'yuv420p', '-color_range', 'tv',
               '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709']
    with tempfile.TemporaryDirectory(prefix='.video-render-', dir=root) as directory:
        temp = Path(directory)
        run(['-filter_complex_threads', '1', '-loop', '1', '-framerate', '24',
             '-t', '6', '-i', str(root/'assets/inventing-fire-title.png'),
             '-loop', '1', '-framerate', '24', '-t', '6',
             '-i', str(root/f'assets/{kind}-text.png'), '-filter_complex',
             '[0:v]scale=400:225,setsar=1[logo];'
             '[1:v][logo]overlay=x=440:y=380,format=yuv420p,fade=t=out:st=4:d=2[v]',
             '-map', '[v]', '-frames:v', '144', *picture, str(temp/'title.mp4')])
        run(['-f', 'lavfi', '-i', 'color=c=black:s=1280x720:r=24:d=60',
             *picture, str(temp/'black.mp4')])
        playlist = temp/'picture.txt'
        playlist.write_text("file 'title.mp4'\n" + "file 'black.mp4'\n" * math.ceil((seconds-6)/60))
        run(['-f', 'concat', '-safe', '0', '-i', str(playlist), '-i', str(master),
             '-map', '0:v:0', '-map', '1:a:0', '-t', str(seconds), '-c:v', 'copy',
             '-c:a', 'aac_at', '-aac_at_quality', '0', '-aac_at_mode', 'cbr',
             '-b:a', '320k', '-ar', '48000', '-movflags', '+faststart', str(output)])
