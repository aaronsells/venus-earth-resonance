# Venus–Earth Orbital Resonance: The Rose and Pentagram of Venus

A comprehensive undergraduate-level astronomy and physics lesson exploring the stunning geometric pattern Venus traces around Earth over 8 years, built with real NASA/JPL orbital data.

## What Is This?

If you track Venus's position relative to Earth for 8 years, it draws a 5-petaled flower — the **Rose of Venus**. Connect the 5 alignment points in order and you get a **pentagram**. This project explains *why* with real orbital mechanics and animates the whole thing.

**Key numbers:** 13 Venus orbits = 8 Earth years = 5 synodic periods. All Fibonacci numbers. The period ratio (1.625) is within 0.5% of the golden ratio.

## Contents

| File | Description |
|------|-------------|
| `venus_earth_dance.py` | Manim Community Edition animation — 11 scenes covering heliocentric orbits, synodic period, Kepler's laws, the rose pattern, pentagram, golden ratio, and practice problems |
| `orbital_resonance_lesson.tex` | Full LaTeX theory document (~25 pages) for Overleaf — derivations, NASA data tables, TikZ diagrams, glossary |
| `practice_problems.tex` | 8 practice problems with full worked solutions — synodic period, Kepler III, orbital velocities, pentagram geometry, Kepler's equation, pattern precession, other planet pairs, golden ratio |
| `narration_script.md` | Timestamped narration script for all 11 scenes, with CUE markers and delivery tips |
| `recording_guide.md` | How to add your own voice using `manim-voiceover` with `RecorderService` |

## Quick Start

```bash
# Install dependencies
pip install manim
pip install "manim-voiceover[recorder]"

# Preview the main scene (low quality, fast)
manim render -ql venus_earth_dance.py RoseOfVenus

# Render all scenes at 1080p
manim render -qh venus_earth_dance.py TitleScene HeliocentricOrbits \
  OrbitalResonance SynodicPeriod GeocentricTransform RoseOfVenus \
  PentagramOfVenus KeplerLaws GoldenRatioConnection PhysicsChallenges CreditsScene
```

## NASA Data Sources

- Orbital elements: [NASA NSSDC Planetary Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/)
- Ephemeris verification: [NASA JPL Horizons](https://ssd.jpl.nasa.gov/horizons/)

## Credits

- **Author:** Aaron Sells — STEM Tutoring, Lee's Summit, MO
- **Inspired by:** [Cosmic Starships](https://www.youtube.com/@CosmicStarships) YouTube channel
- **Animation engine:** [Manim Community Edition](https://www.manim.community/)
- **Orbital data:** NASA/JPL

## License

Educational use. Attribution appreciated.
