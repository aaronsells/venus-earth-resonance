# Recording Guide: Adding Your Voice to the Venus Animation

**Author:** Aaron Sells — STEM Tutoring
**Date:** November 2026

---

## Overview

This guide walks you through adding your own voice narration to the
Manim animation using the `manim-voiceover` plugin with
`RecorderService`. This lets you record your microphone audio in
sync with each animation scene.

---

## 1. Install Dependencies

```bash
# Install Manim Community Edition (if not already installed)
pip install manim

# Install manim-voiceover with recorder support
pip install "manim-voiceover[recorder]"
```

**System requirements:**
- Python 3.8+
- FFmpeg (for audio/video processing)
- A working microphone
- Sox (optional, for audio normalization): `sudo apt install sox`
  or `brew install sox` on macOS

---

## 2. How manim-voiceover Works

The plugin provides two key components:

1. **`VoiceoverScene`** — a Manim scene class that replaces the
   standard `Scene` class
2. **`RecorderService`** — a speech service that records from your
   microphone

When you run a scene that uses voiceover, the plugin:
1. Displays the voiceover text on screen as a prompt
2. Waits for you to press Enter to start recording
3. Records your microphone until you press Enter again
4. Syncs the recorded audio with the animation timeline
5. Embeds the audio in the final rendered video

---

## 3. Modifying the Animation for Voiceover

To add voiceover to any scene in `venus_earth_dance.py`, you need
to make two changes:

### Step 1: Change the class inheritance

```python
# Before:
from manim import *

class RoseOfVenus(Scene):
    def construct(self):
        ...

# After:
from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService

class RoseOfVenus(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService())
        ...
```

### Step 2: Wrap animation blocks in voiceover contexts

```python
class RoseOfVenus(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService())

        # Each voiceover block syncs audio with animations
        with self.voiceover(
            text="""Now — the main event. Earth is at the center.
            We're watching Venus's path as seen from Earth,
            computed from real NASA orbital elements."""
        ) as tracker:
            # Animations that play during this narration
            self.play(Create(earth_dot))
            self.play(Create(path_trace))
            # Wait for narration to finish if animations are shorter
            self.wait_until_bookmark("end")

        with self.voiceover(
            text="""After five hundred eighty-four days — one synodic
            period — Venus has traced the first petal."""
        ) as tracker:
            self.play(petal_animation, run_time=tracker.duration)
```

### Key API Details

- **`tracker.duration`**: Total duration of your recorded audio.
  Use this as `run_time` to sync animation length to speech length.
- **`self.wait_until_bookmark("name")`**: Pause animation until a
  specific point in the audio (set bookmarks with `<bookmark
  mark="name"/>` in the text).
- **`tracker.time_until_bookmark("name")`**: Get seconds until a
  bookmark — useful for `run_time` of partial animations.

---

## 4. Recording Workflow

### 4.1 Render without voiceover first

Preview the animation to understand timing:

```bash
# Low quality preview (fast)
manim render -ql venus_earth_dance.py RoseOfVenus

# Medium quality
manim render -qm venus_earth_dance.py RoseOfVenus
```

### 4.2 Record with voiceover

Once you've modified the scene for voiceover:

```bash
manim render -qm venus_earth_dance.py RoseOfVenus
```

The terminal will prompt you:

```
Press Enter to start recording...
[Recording] Press Enter to stop...
```

For each `self.voiceover(...)` block, you'll:
1. See the text displayed on screen
2. Press Enter when ready
3. Speak the narration (refer to `narration_script.md`)
4. Press Enter when done

The plugin saves recordings in `media/voiceover/` and automatically
syncs them with the animation.

### 4.3 Render final quality

After recording all voiceovers:

```bash
# High quality (1080p)
manim render -qh venus_earth_dance.py RoseOfVenus

# 4K quality
manim render -qk venus_earth_dance.py RoseOfVenus
```

---

## 5. Scene-by-Scene Conversion Outline

Here's which scenes to convert and in what order. The
`narration_script.md` file has the exact text for each.

| Scene Class | Priority | Duration | Notes |
|---|---|---|---|
| `TitleScene` | Optional | 8s | Simple title — voiceover optional |
| `HeliocentricOrbits` | High | 45s | Good intro, sets the stage |
| `OrbitalResonance` | High | 40s | Key concept, needs clear delivery |
| `SynodicPeriod` | High | 50s | Math-heavy, pace yourself |
| `GeocentricTransform` | Medium | 30s | Short, conceptual |
| `RoseOfVenus` | **Critical** | 90s | The main event |
| `PentagramOfVenus` | High | 35s | Dramatic reveal |
| `KeplerLaws` | Medium | 45s | Review/recap feel |
| `GoldenRatioConnection` | Medium | 35s | Fun conclusion |
| `PhysicsChallenges` | Low | 25s | Brief callout |
| `CreditsScene` | Optional | 10s | Sign-off |

**Recommended approach:** Start with `RoseOfVenus` (the centerpiece),
then `HeliocentricOrbits` and `OrbitalResonance`. Add others
incrementally.

---

## 6. Pro Tips for Quality Audio

### Environment
- Record in a small, carpeted room (closets work great)
- Close windows and turn off fans/AC during recording
- Put your phone on silent
- Record a 5-second silence sample to check background noise

### Microphone
- USB condenser mics (Blue Yeti, Audio-Technica AT2020) work well
- Position 6–8 inches from your mouth, slightly off-axis
- Use a pop filter if available
- Laptop built-in mics work in a pinch but pick up fan noise

### Delivery
- Speak at about 130 words per minute (slower than conversation)
- Pause 1–2 seconds before and after equations
- Spell out numbers: "three hundred sixty-five" not "365"
- Record each scene multiple times — you can pick the best take
- Drink water between scenes

### Post-processing (optional)
If you want to clean up audio after recording:

```bash
# Normalize volume levels across all recordings
sox input.wav output.wav norm -1

# Remove background noise (record 5s of silence first as profile)
sox silence.wav -n noiseprof noise.prof
sox input.wav output.wav noisered noise.prof 0.21
```

---

## 7. Combining Scenes into One Video

After rendering individual scenes with voiceover, combine them:

```bash
# Create a file list
ls media/videos/venus_earth_dance/1080p60/*.mp4 > filelist.txt

# Edit filelist.txt to have this format:
# file 'path/to/TitleScene.mp4'
# file 'path/to/HeliocentricOrbits.mp4'
# ... (in viewing order)

# Concatenate with FFmpeg
ffmpeg -f concat -safe 0 -i filelist.txt -c copy final_lesson.mp4
```

---

## 8. Alternative: Text-to-Speech (No Recording)

If you want a quick prototype before recording your own voice,
`manim-voiceover` also supports TTS services:

```python
# Using gTTS (free, robotic but functional)
pip install "manim-voiceover[gtts]"

from manim_voiceover.services.gtts import GTTSService

class RoseOfVenus(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"))
        ...
```

This is useful for previewing timing before you commit to recording.

---

## 9. Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: manim_voiceover` | `pip install "manim-voiceover[recorder]"` |
| No audio in output | Check FFmpeg: `ffmpeg -version` |
| Recording too quiet | Move closer to mic, check system input volume |
| Audio out of sync | Use `tracker.duration` for `run_time` |
| `OSError: No default input device` | Check system sound settings, select microphone |
| Choppy playback | Render at lower quality first (`-ql`) |

---

## Quick Start Checklist

- [ ] Install `manim` and `manim-voiceover[recorder]`
- [ ] Preview all scenes without voiceover (`manim render -ql`)
- [ ] Read through `narration_script.md` aloud once
- [ ] Convert `RoseOfVenus` scene to `VoiceoverScene`
- [ ] Record `RoseOfVenus` narration
- [ ] Preview the result
- [ ] Convert and record remaining scenes
- [ ] Combine into final video with FFmpeg
- [ ] Upload to website and social media
