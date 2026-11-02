# Research-backed thunder cracks

Owner feedback, 2026-11-02: the thunder still lacked audible lightning cracks. The requested deep-research skill and connector are not available in this session; the sources below were researched directly.

## What the sources establish

- [NOAA: The Sound of Thunder](https://www.noaa.gov/jetstream/lightning/sound-of-thunder): a sharp initial pressure front produces the crack; later arrivals from other channel sections stretch into a rumble. This supports separating the transient from the rolling tail.
- [NWS: Understanding Lightning — Thunder](https://www.weather.gov/safety/lightning-science-thunder): nearby channel sections produce a sharp crack, while more distant sections arrive later. A collection of equally muffled noise swells does not represent this distinction.
- [Wang et al., 2022, Journal of Applied Physics, DOI 10.1063/5.0110866](https://ira.lib.polyu.edu.hk/bitstream/10397/111147/1/123301_1_online.pdf): near-field return-stroke recordings show an initial N-shaped pressure waveform followed by lower-frequency oscillation. Their initial shock had a 200–400 Hz spectral peak and a principal 200–800 Hz band. These experiment-specific values concern the local shock, not the duration or spectrum of an entire distant thunder roll.
- [Dayeh et al., 2015, Geophysical Research Letters, DOI 10.1002/2015GL064451](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2015GL064451): close thunder measurements contain energy above 1 kHz. Successive return-stroke spacings calculated from Table 1 range from approximately 17 to 286 ms. Electrical return strokes and environmental reflections are different mechanisms; the model must not label one fixed echo pattern as both.
- [Fineberg, Walters and Reiss, 2022: Advances in Thunder Sound Synthesis](https://arxiv.org/html/2204.08026v1): treats the initial impulsive clap, rumble and environmental afterimage as separate components. Its listening results also caution that synthesis can remain distinguishable from recordings. This implementation does not copy their code or audio.

## Decision after listening

The owner rejected the synthesized pressure-front audition as sounding like gunshots, then approved the 59-second audition made from genuine thunder recordings. The owner subsequently required realistic frequency and pattern, with no artificially overlapping thunder.

The final model therefore does not synthesize lightning cracks or schedule individual thunder events. It sequences real storm passages at their native sample speed and keeps the weather cadence within each passage. Storm scenes are contiguous and never overlap. Longer recordings are cut only at quiet candidates away from strong peals; complete source passages retain their natural crack-to-rumble shape. A quiet, genuine rain recording bridges scene edges. Source passages are reused in varied order; this is a constructed mix, not an eight-hour uninterrupted field capture.

The window track uses calm excerpts from an actual window-sill rain recording. Gusty portions are excluded; fixed EQ and quiet recorded rain keep glass detail soft. White noise, brown noise and the ambient composition remain procedural.

## Sources, processing and verification

The machine-readable source bank, creator credits, public download representation, license links and SHA-256 checksums are in [the manifest](../../assets/recordings/sources.json). Weather MP4 metadata embeds the source-bank credits and adaptation notice; [the publication notice](../../site/recording-credits.txt) makes the same credits accessible on the site. Capture and prior-encoding limitations are recorded rather than claiming the downloaded MP3/Vorbis files are original lossless recordings.

The original steady-texture screen retains a 3 dB maximum one-second RMS change for window rain and the noise/drone tracks. Native thunder has intentional clap transients; its 20 dB investigation threshold preserves the dynamics of the approved real-recording audition rather than smoothing them into noise. This is a production-screening choice, not a measured weather law. Fixed loudness mastering, clipping/headroom checks, silence checks, fades and full decoded-delivery verification remain in force.

The eight-hour storm plan was checked for zero scene overlap and valid source ranges. A twelve-minute window mix passed the unchanged 3 dB screen at 1.78 dB maximum change. Both final eight-hour deliveries passed complete technical verification, including every decoded audio sample and video frame; representative full-mix listening remains pending. No claim is made that numerical measurements establish realism or full listening approval.

[NOAA's reference page](https://www.noaa.gov/jetstream/lightning/sound-of-thunder/learning-lesson-determining-distance-to-thunderstorm) supplies sharp-thunder and rumble examples, but their downloads returned HTTP 403 here and no listening comparison is claimed. No NOAA reference recording is embedded.
