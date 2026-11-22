# Venus–Earth Orbital Resonance: Narration Script

**For use with `manim-voiceover` RecorderService**
**Author:** Aaron Sells — STEM Tutoring
**Date:** November 2026

---

## How to Use This Script

Each section below corresponds to one Manim scene in `venus_earth_dance.py`.
The `[SCENE]` header tells you which class to run. The `[CUE]` markers
tell you when to start speaking relative to the animation. Pauses are
marked with `[PAUSE 2s]` etc.

When recording with `manim-voiceover`'s `RecorderService`, each
`with self.voiceover(text="...")` block will prompt you to record.
The text shown here is what appears on screen as your recording prompt.

---

## Scene 1: TitleScene
**Duration:** ~8 seconds

> [CUE: On title card appearance]
>
> "The Rose and Pentagram of Venus. How one planet's orbit draws
> a flower around another — using real NASA data."
>
> [PAUSE 2s]

---

## Scene 2: HeliocentricOrbits
**Duration:** ~45 seconds

> [CUE: Sun appears at center]
>
> "Let's start with what the solar system actually looks like — the
> heliocentric view, centered on the Sun."
>
> [CUE: Venus orbit drawn]
>
> "Venus orbits at zero-point-seven-two AU, completing a full orbit
> every two hundred twenty-five days."
>
> [CUE: Earth orbit drawn]
>
> "Earth orbits at one AU — about one-point-five times farther out —
> taking three hundred sixty-five days per orbit."
>
> [CUE: Planets begin animated motion]
>
> "Watch how Venus gradually pulls ahead. It moves about eighteen
> percent faster than Earth — roughly thirty-five kilometers per
> second versus Earth's thirty."
>
> [CUE: Trail paths visible]
>
> "These trails show each planet's path. From up here, it's just
> two concentric circles. But something remarkable happens when
> we change our point of view."
>
> [PAUSE 2s]

---

## Scene 3: OrbitalResonance
**Duration:** ~40 seconds

> [CUE: Period values appear]
>
> "Here's the key relationship. Venus's orbital period is two hundred
> twenty-four-point-seven days. Earth's is three hundred sixty-five-
> point-two-six days."
>
> [CUE: Ratio calculation shown]
>
> "If we divide Earth's period by Venus's, we get one-point-six-two-five.
> That is remarkably close to the fraction thirteen over eight."
>
> [CUE: Verification numbers appear]
>
> "Let's verify: thirteen Venus orbits take two thousand nine hundred
> twenty-one days. Eight Earth orbits take two thousand nine hundred
> twenty-two days. They differ by just one-point-two days over
> eight years."
>
> [CUE: Fibonacci highlight]
>
> "And notice — five, eight, and thirteen are all Fibonacci numbers.
> That's not a coincidence. We'll come back to that."
>
> [PAUSE 2s]

---

## Scene 4: SynodicPeriod
**Duration:** ~50 seconds

> [CUE: Angular velocity equations appear]
>
> "To understand the pattern Venus draws, we need the synodic period —
> the time between successive alignments of Venus, Earth, and the Sun."
>
> [CUE: Derivation step 1]
>
> "Venus has angular velocity omega-V equals two-pi over T-V.
> Earth has omega-E equals two-pi over T-E. In Earth's reference
> frame, Venus gains angle at the difference of these rates."
>
> [CUE: Formula boxed]
>
> "Setting the gained angle equal to two-pi and solving gives us
> the synodic period formula: one over P-syn equals one over T-V
> minus one over T-E."
>
> [CUE: Numerical result]
>
> "Plugging in NASA's values: P-syn equals five hundred eighty-four
> days, or about one-point-six years. That's how long between each
> time Venus passes between Earth and the Sun — an event called
> inferior conjunction."
>
> [CUE: Count result]
>
> "And in eight Earth years? Exactly five synodic periods.
> Five alignments. Five petals."
>
> [PAUSE 2s]

---

## Scene 5: GeocentricTransform
**Duration:** ~30 seconds

> [CUE: Coordinate formula appears]
>
> "Now let's transform our viewpoint. To see Venus from Earth,
> we subtract Earth's position vector from Venus's."
>
> [CUE: Vector equation highlighted]
>
> "R-Venus-geocentric equals R-Venus-heliocentric minus
> R-Earth-heliocentric. This is a simple vector subtraction,
> but it produces something beautiful."
>
> [CUE: Pipeline diagram]
>
> "Our computation pipeline: start with time, compute mean anomaly,
> solve Kepler's equation for the eccentric anomaly, convert to
> true anomaly, get the radius, and finally the x-y coordinates.
> We do this for both planets, then subtract."
>
> [PAUSE 2s]

---

## Scene 6: RoseOfVenus ★ (Main Scene)
**Duration:** ~90 seconds

> [CUE: Earth centered, first petal begins drawing]
>
> "Now — the main event. Earth is at the center. We're watching
> Venus's path as seen from Earth, computed from real NASA
> orbital elements."
>
> [CUE: First petal completes, conjunction marked]
>
> "After five hundred eighty-four days — one synodic period —
> Venus has traced the first petal and returned to inferior
> conjunction. That's our first alignment point."
>
> [PAUSE 1s]
>
> [CUE: Second petal begins, different color]
>
> "The second petal begins. Notice it's rotated about one hundred
> forty-four degrees from the first. That's not arbitrary — it's
> two-fifths of three hundred sixty degrees."
>
> [CUE: Third petal drawing]
>
> "Petal three. The pattern is becoming clear — a five-fold
> rotational symmetry."
>
> [CUE: Fourth petal drawing]
>
> "Four petals now. You can see the flower taking shape."
>
> [CUE: Fifth petal completes, full rose visible]
>
> "And there it is — the Rose of Venus. Five petals, eight years,
> thirteen orbits. All from Newton's gravity and Kepler's laws
> applied to real planetary data."
>
> [CUE: Year counter shows ~8.0]
>
> "The pattern doesn't close perfectly — there's a drift of about
> two-and-a-half degrees per cycle. But it's close enough to
> produce this stunning near-symmetry."
>
> [PAUSE 3s]

---

## Scene 7: PentagramOfVenus
**Duration:** ~35 seconds

> [CUE: Five conjunction points marked]
>
> "Now let's connect the five inferior conjunction points in the
> order they occurred."
>
> [CUE: Lines drawn forming pentagram]
>
> "When we draw lines from each conjunction to the next in time —
> skipping the adjacent petal — we get a pentagram. A five-pointed
> star inscribed in the rose."
>
> [CUE: Angular separation annotated]
>
> "Each consecutive conjunction is separated by about one hundred
> forty-four degrees. Five times seventy-two is three hundred sixty,
> but connecting every other vertex at one-forty-four degrees is
> exactly how you construct a pentagram — a star polygon with
> winding number two."
>
> [PAUSE 2s]

---

## Scene 8: KeplerLaws
**Duration:** ~45 seconds

> [CUE: First Law]
>
> "Everything we've seen rests on Kepler's three laws. The First Law:
> orbits are ellipses with the Sun at one focus. Venus's eccentricity
> is only zero-point-zero-zero-seven — nearly circular — which is
> why the petals are so symmetric."
>
> [CUE: Second Law]
>
> "The Second Law: a planet sweeps equal areas in equal times.
> This means planets move faster at perihelion and slower at
> aphelion. For Venus, the speed variation is tiny — just
> one-point-four percent."
>
> [CUE: Third Law]
>
> "The Third Law: T-squared is proportional to a-cubed. This is
> the law that locks in the thirteen-to-eight ratio. Given Venus's
> semi-major axis of zero-point-seven-two-three AU, Kepler's
> Third Law predicts its period to within a hundredth of a percent
> of the measured value."
>
> [PAUSE 2s]

---

## Scene 9: GoldenRatioConnection
**Duration:** ~35 seconds

> [CUE: Fibonacci sequence appears]
>
> "One, one, two, three, five, eight, thirteen. The Fibonacci
> sequence. Notice our three key numbers — five petals, eight years,
> thirteen orbits — are three consecutive Fibonacci numbers."
>
> [CUE: Golden ratio comparison]
>
> "The ratio of consecutive Fibonacci numbers converges to the
> golden ratio, phi, which equals one-point-six-one-eight.
> Our period ratio of one-point-six-two-five is just zero-point-
> four-six percent away."
>
> [CUE: "Most irrational" text]
>
> "Phi is the most irrational number — its rational approximations
> converge the slowest. That's why Venus's pattern has so few
> petals while nearly closing. Thirteen-over-eight is a sweet spot:
> close enough to repeat, far enough to drift beautifully."
>
> [PAUSE 2s]

---

## Scene 10: PhysicsChallenges
**Duration:** ~25 seconds

> [CUE: Problems appear on screen]
>
> "Here are six practice problems to test your understanding.
> They cover synodic period derivation, Kepler's Third Law
> verification, orbital velocities, pentagram geometry, Kepler's
> equation, and pattern precession."
>
> [CUE: Solutions reference]
>
> "Full worked solutions are in the companion PDF. Try them
> before looking — they'll solidify everything we've covered."
>
> [PAUSE 2s]

---

## Scene 11: CreditsScene
**Duration:** ~10 seconds

> [CUE: Credits appear]
>
> "Created by Aaron Sells, STEM Tutoring, Lee's Summit, Missouri.
> Orbital data from NASA JPL. Inspired by the Cosmic Starships
> YouTube channel. Built with Manim Community Edition."
>
> [PAUSE 3s — let credits linger]

---

## Total Estimated Duration: ~7 minutes

## Tips for Recording

1. **Speak slowly and clearly.** Math content needs time to land.
2. **Match your pace to the animation.** The CUE markers help.
3. **Don't rush equations.** When reading a formula, pause before
   and after each term.
4. **Record in a quiet room** with minimal echo. A closet full of
   clothes works surprisingly well.
5. **Keep water nearby.** Seven minutes of narration is a lot of
   talking.
6. **Record each scene separately.** `manim-voiceover` prompts
   you per voiceover block, so you can re-record any section.
7. **Preview first.** Render each scene without voiceover
   (`manim render -ql venus_earth_dance.py SceneName`) to see
   the timing before you record.
