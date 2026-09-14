'use strict';
const tracks = {
  'white-noise': ['01', 'Softened white noise', 'A steady noise texture with softened high frequencies for a less bright, more rounded sound. No music or voices.'],
  'distant-thunder-rain': ['02', 'Distant thunder & rain', 'A continuous bed of synthetic rain with occasional distant thunder. A sheltered storm atmosphere, without lightning visuals.'],
  'rain-on-window': ['03', 'Gentle rain on a window', 'Soft, synthesized rainfall with delicate, irregular window textures. An indoor listening perspective, with no thunder, music, or voices.'],
  'brown-noise': ['04', 'Deep brown noise', 'A deep, low-frequency noise texture with controlled subsonic energy and softened highs. Warm and steady, with no music or voices.'],
  'ambient-drone': ['05', 'Deep ambient sleep drone', 'Sustained warm tones and slowly evolving harmonies. An original ambient composition without percussion or a prominent melody.']
};
const player = document.getElementById('player');
const buttons = [...document.querySelectorAll('[data-track]')];
const error = document.getElementById('player-error');
buttons.forEach(button => button.addEventListener('click', () => {
  if (button.getAttribute('aria-pressed') === 'true') return;
  const id = button.dataset.track;
  const [index, title, description] = tracks[id];
  player.pause();
  player.poster = `media/${id}-title.png`;
  player.src = `media/${id}-preview.mp4`;
  player.setAttribute('aria-label', `${title} preview`);
  document.getElementById('track-index').textContent = index;
  document.getElementById('track-title').textContent = title;
  document.getElementById('track-description').textContent = description;
  document.getElementById('download').href = `media/${id}-preview.mp4`;
  buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
  error.hidden = true;
  player.load();
}));
player.addEventListener('error', () => { error.hidden = false; });
