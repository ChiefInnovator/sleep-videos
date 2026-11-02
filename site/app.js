'use strict';
// Full-video links live here so each can later point to its YouTube video.
const release = 'https://github.com/ChiefInnovator/sleep-videos/releases/download/v1.0.0/';
const revisedWeather = 'https://github.com/ChiefInnovator/sleep-videos/raw/refs/heads/main/videos/';
const tracks = {
  'white-noise': ['01', 'Softened white noise', 'A steady noise texture with softened high frequencies for a less bright, more rounded sound. No music or voices.', release + 'white-noise-full.mp4'],
  'distant-thunder-rain': ['02', 'Distant thunder & rain', 'Real storm recordings with natural thunder timing and rolling decays. Passages play sequentially with quiet rain joins.', revisedWeather + 'distant-thunder-rain-full.mp4'],
  'rain-on-window': ['03', 'Gentle rain on a window', 'Real window rain with soft glass detail and a quiet recorded rain bed. Calm passages give a sheltered indoor perspective.', revisedWeather + 'rain-on-window-full.mp4'],
  'brown-noise': ['04', 'Deep brown noise', 'A deep, low-frequency noise texture with controlled subsonic energy and softened highs. Warm and steady, with no music or voices.', release + 'brown-noise-full.mp4'],
  'ambient-drone': ['05', 'Deep ambient sleep drone', 'Sustained warm tones and slowly evolving harmonies. An original ambient composition without percussion or a prominent melody.', release + 'ambient-drone-full.mp4']
};
const player = document.getElementById('player');
const buttons = [...document.querySelectorAll('[data-track]')];
const error = document.getElementById('player-error');
const stacked = matchMedia('(max-width: 700px)');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
buttons.forEach(button => button.addEventListener('click', () => {
  if (button.getAttribute('aria-pressed') === 'true') return;
  const id = button.dataset.track;
  const [index, title, description, full] = tracks[id];
  player.pause();
  player.poster = `media/${id}-title.png`;
  player.src = `media/${id}-preview.mp4`;
  player.setAttribute('aria-label', `${title} preview`);
  document.getElementById('track-index').textContent = index;
  document.getElementById('track-title').textContent = title;
  document.getElementById('track-description').textContent = description;
  document.getElementById('download').href = `media/${id}-preview.mp4`;
  document.getElementById('download-full').href = full;
  document.querySelector('.file-note').textContent = `MP4 · about ${full.startsWith(revisedWeather) ? '0.6' : '1.2'} GB · from GitHub`;
  buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
  error.hidden = true;
  player.load();
  if (stacked.matches) player.scrollIntoView({behavior: reducedMotion.matches ? 'auto' : 'smooth', block: 'center'});
}));
player.addEventListener('error', () => { error.hidden = false; });
