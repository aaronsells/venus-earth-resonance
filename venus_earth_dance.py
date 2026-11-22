#!/usr/bin/env python3
"""
venus_earth_dance.py
====================
The Dance of Venus & Earth: Orbital Resonance and the Pentagram of Venus

A comprehensive Manim Community Edition animation for undergraduate-level
Astronomy and Physics education.

Data Source: NASA/JPL Planetary Fact Sheets (NSSDC)
             https://nssdc.gsfc.nasa.gov/planetary/factsheet/

Render individual scenes:
    manim -pqh venus_earth_dance.py TitleScene
    manim -pqh venus_earth_dance.py HeliocentricOrbits
    manim -pqh venus_earth_dance.py RoseOfVenus
    ... etc.

Render all scenes to files:
    manim -qh venus_earth_dance.py

For voiceover integration (record your own narration):
    pip install "manim-voiceover[recorder]"
    See the companion recording_guide.md for full instructions.

Author: Aaron Sells — STEM Tutoring, Lee's Summit MO
Animation Engine: Manim Community Edition (ManimCE)
"""

from manim import *
import numpy as np

# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SECTION 1 — NASA/JPL ORBITAL DATA  (J2000 Epoch)                 ║
# ║  Source: https://nssdc.gsfc.nasa.gov/planetary/factsheet/          ║
# ╚══════════════════════════════════════════════════════════════════════╝

AU_KM = 149_597_870.7  # 1 Astronomical Unit in km

VENUS = dict(
    name   = "Venus",
    a      = 0.72333199,         # Semi-major axis  (AU)
    e      = 0.00677323,         # Eccentricity
    i_deg  = 3.39471,            # Inclination      (deg)
    Omega  = 76.68069,           # Long. asc. node  (deg)
    omega_bar = 131.53298,       # Long. perihelion  (deg)
    L0     = 181.97973,          # Mean longitude at J2000 (deg)
    T_days = 224.701,            # Sidereal period   (days)
    color  = "#FFD700",          # Gold
)

EARTH = dict(
    name   = "Earth",
    a      = 1.00000011,         # Semi-major axis  (AU)
    e      = 0.01671022,         # Eccentricity
    i_deg  = 0.00005,            # Inclination      (deg)
    Omega  = -11.26064,          # Long. asc. node  (deg)
    omega_bar = 102.94719,       # Long. perihelion  (deg)
    L0     = 100.46435,          # Mean longitude at J2000 (deg)
    T_days = 365.256,            # Sidereal period   (days)
    color  = "#4169E1",          # Royal Blue
)

# Convert periods to years for internal math
for body in (VENUS, EARTH):
    body["T_yr"] = body["T_days"] / 365.256

# Derived constants
SYNODIC_DAYS = 1.0 / (1.0/VENUS["T_days"] - 1.0/EARTH["T_days"])   # ~583.9 d
SYNODIC_YR   = SYNODIC_DAYS / 365.256                                # ~1.599 yr
PERIOD_RATIO = EARTH["T_days"] / VENUS["T_days"]                     # ~1.6253
N_PETALS     = 5          # 13 − 8 inferior conjunctions per 8 yr

# Display scales  (AU → Manim scene units)
HELIO_SCALE = 3.0   # For heliocentric views
GEO_SCALE   = 1.8   # For geocentric views (keeps petals on screen)

# Colour palette
BG_COLOR        = "#0a0a2e"
SUN_COLOR       = YELLOW
VENUS_CLR       = "#FFD700"
EARTH_CLR       = "#4169E1"
ORBIT_DIM       = GREY_D
PETAL_COLORS    = ["#e74c3c", "#e67e22", "#2ecc71", "#1abc9c", "#9b59b6"]
PENTAGRAM_COLOR = "#FF6B6B"


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SECTION 2 — KEPLERIAN ORBITAL-MECHANICS ENGINE                    ║
# ╚══════════════════════════════════════════════════════════════════════╝

def solve_kepler(M: float, e: float, tol: float = 1e-12) -> float:
    """
    Solve Kepler's equation   M = E − e sin E   for eccentric anomaly E.

    Uses Newton–Raphson iteration with Danby's initial guess.
    Works for scalar or array M.
    """
    M = np.asarray(M, dtype=float)
    E = M + 0.85 * e * np.sign(np.sin(M))          # Danby start
    for _ in range(80):
        dE = (M - E + e * np.sin(E)) / (1.0 - e * np.cos(E))
        E += dE
        if np.all(np.abs(dE) < tol):
            break
    return float(E) if E.ndim == 0 else E


def true_anomaly(E: float, e: float) -> float:
    """Eccentric anomaly → true anomaly  ν."""
    return 2.0 * np.arctan2(
        np.sqrt(1 + e) * np.sin(E / 2.0),
        np.sqrt(1 - e) * np.cos(E / 2.0),
    )


def planet_xy(t: float, body: dict, scale: float) -> np.ndarray:
    """
    Position (x, y, 0) of *body* at time *t* (years from J2000).

    Pipeline:  t → M → E (Kepler) → ν → r → (x, y)
    """
    a = body["a"]
    e = body["e"]
    T = body["T_yr"]
    omega = np.radians(body["omega_bar"] - body["Omega"])   # arg. perihelion

    n  = 2.0 * np.pi / T                                    # mean motion
    M0 = np.radians(body["L0"] - body["omega_bar"])          # M at epoch
    M  = (M0 + n * t) % (2.0 * np.pi)                       # mean anomaly

    E  = solve_kepler(M, e)
    nu = true_anomaly(E, e)
    r  = a * (1.0 - e * np.cos(E))                          # orbital radius

    angle = nu + omega
    return np.array([r * np.cos(angle) * scale,
                     r * np.sin(angle) * scale,
                     0.0])


def venus_geo(t: float, scale: float = GEO_SCALE) -> np.ndarray:
    """Venus position in geocentric (Earth-centred) frame."""
    return planet_xy(t, VENUS, scale) - planet_xy(t, EARTH, scale)


def find_inferior_conjunctions(t0: float = 0.0, t1: float = 8.0,
                               n_scan: int = 12000) -> list:
    """Return list of times (yr) of inferior conjunctions in [t0, t1]."""
    ts = np.linspace(t0, t1, n_scan)
    ds = np.array([np.linalg.norm(venus_geo(t)) for t in ts])

    conjs = []
    for i in range(1, len(ds) - 1):
        if ds[i] < ds[i - 1] and ds[i] < ds[i + 1]:
            # Golden-section refinement
            lo, hi = ts[i - 1], ts[i + 1]
            gr = (np.sqrt(5) + 1) / 2
            for _ in range(120):
                if hi - lo < 1e-12:
                    break
                a = hi - (hi - lo) / gr
                b = lo + (hi - lo) / gr
                if np.linalg.norm(venus_geo(a)) < np.linalg.norm(venus_geo(b)):
                    hi = b
                else:
                    lo = a
            conjs.append((lo + hi) / 2.0)
    return conjs


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SECTION 3 — HELPER UTILITIES FOR MANIM SCENES                    ║
# ╚══════════════════════════════════════════════════════════════════════╝

def make_orbit_ellipse(body, scale, **kw):
    a = body["a"] * scale
    b = a * np.sqrt(1 - body["e"]**2)
    return Ellipse(width=2*a, height=2*b, **kw)


def geocentric_path_mobject(t0, t1, n_pts=600, scale=GEO_SCALE,
                            color=WHITE, width=2.0):
    """Return a VMobject tracing Venus's geocentric path from t0 to t1."""
    pts = [venus_geo(t, scale) for t in np.linspace(t0, t1, n_pts)]
    path = VMobject(stroke_color=color, stroke_width=width)
    path.set_points_as_corners(pts)
    return path


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 1 — TITLE                                                  ║
# ╚══════════════════════════════════════════════════════════════════════╝

class TitleScene(Scene):
    """Opening title card."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("The Dance of Venus & Earth",
                      font_size=44, color=WHITE, weight=BOLD)
        sub = Text("Orbital Resonance and the Pentagram of Venus",
                    font_size=24, color=GREY_B).next_to(title, DOWN, 0.35)
        nasa = Text("Computed from NASA / JPL Ephemeris Data",
                     font_size=18, color=YELLOW_D).next_to(sub, DOWN, 0.5)
        credit = Text("A STEM Tutoring Lesson  ·  Aaron Sells",
                       font_size=16, color=GREY_C).next_to(nasa, DOWN, 0.4)

        self.play(Write(title, run_time=2))
        self.play(FadeIn(sub, shift=UP*0.2))
        self.play(FadeIn(nasa, shift=UP*0.15), FadeIn(credit, shift=UP*0.15))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 2 — HELIOCENTRIC ORBITS                                    ║
# ╚══════════════════════════════════════════════════════════════════════╝

class HeliocentricOrbits(Scene):
    """Sun-centred view: Venus and Earth orbiting with real data."""
    def construct(self):
        self.camera.background_color = BG_COLOR
        sc = HELIO_SCALE

        header = Text("Heliocentric View  —  The Solar System Frame",
                       font_size=28, color=WHITE).to_edge(UP, buff=0.3)
        self.play(Write(header))

        # Sun
        sun_glow = Dot(ORIGIN, radius=0.28, color=SUN_COLOR, fill_opacity=0.25)
        sun      = Dot(ORIGIN, radius=0.18, color=SUN_COLOR)
        sun_lbl  = Text("☉ Sun", font_size=14, color=SUN_COLOR).next_to(sun, DOWN, 0.12)
        self.play(FadeIn(sun_glow), FadeIn(sun), Write(sun_lbl))

        # Orbit ellipses
        v_orb = make_orbit_ellipse(VENUS, sc, color=VENUS_CLR,
                                   stroke_width=1, stroke_opacity=0.4)
        e_orb = make_orbit_ellipse(EARTH, sc, color=EARTH_CLR,
                                   stroke_width=1, stroke_opacity=0.4)
        self.play(Create(v_orb), Create(e_orb), run_time=1.5)

        # Planet dots
        t_trk = ValueTracker(0)

        v_dot = always_redraw(lambda: Dot(
            planet_xy(t_trk.get_value(), VENUS, sc),
            radius=0.09, color=VENUS_CLR))
        e_dot = always_redraw(lambda: Dot(
            planet_xy(t_trk.get_value(), EARTH, sc),
            radius=0.11, color=EARTH_CLR))

        v_lbl = always_redraw(lambda: Text("Venus", font_size=13, color=VENUS_CLR)
                              .next_to(v_dot, UR, 0.08))
        e_lbl = always_redraw(lambda: Text("Earth", font_size=13, color=EARTH_CLR)
                              .next_to(e_dot, UR, 0.08))

        self.add(v_dot, e_dot, v_lbl, e_lbl)

        # Data panel
        panel = VGroup(
            Text("NASA / JPL Orbital Data", font_size=16, color=YELLOW_D),
            Text(f"Venus  a = {VENUS['a']:.4f} AU   T = {VENUS['T_days']:.1f} d",
                 font_size=13, color=VENUS_CLR),
            Text(f"Earth  a = {EARTH['a']:.4f} AU   T = {EARTH['T_days']:.1f} d",
                 font_size=13, color=EARTH_CLR),
            Text(f"Period ratio  T_E / T_V = {PERIOD_RATIO:.4f} ≈ 13 / 8",
                 font_size=13, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(DR, buff=0.3)
        self.play(FadeIn(panel))

        # Trails
        v_trail = TracedPath(v_dot.get_center, stroke_color=VENUS_CLR,
                             stroke_width=1.8, stroke_opacity=0.55)
        e_trail = TracedPath(e_dot.get_center, stroke_color=EARTH_CLR,
                             stroke_width=1.8, stroke_opacity=0.55)
        self.add(v_trail, e_trail)

        # Animate 2 Earth-years of motion
        self.play(t_trk.animate.set_value(2.0), run_time=10, rate_func=linear)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 3 — ORBITAL PERIODS & THE 13 : 8 RATIO                     ║
# ╚══════════════════════════════════════════════════════════════════════╝

class OrbitalResonance(Scene):
    """Why 13 Venus orbits ≈ 8 Earth orbits matters."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("The 13 : 8  Near-Commensurability",
                      font_size=32, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Key equation block
        eq1 = MathTex(r"13\,T_V", r"\;\approx\;", r"8\,T_E",
                      font_size=52)
        eq1[0].set_color(VENUS_CLR)
        eq1[2].set_color(EARTH_CLR)
        eq1.shift(UP * 1.2)

        num = MathTex(
            r"13 \times 224.701\;\text{d}", r"=", r"2{,}921.1\;\text{d}",
            font_size=34, color=VENUS_CLR
        ).next_to(eq1, DOWN, 0.5)
        den = MathTex(
            r"8 \times 365.256\;\text{d}", r"=", r"2{,}922.0\;\text{d}",
            font_size=34, color=EARTH_CLR
        ).next_to(num, DOWN, 0.3)

        diff = MathTex(
            r"\Delta = 0.9\;\text{d in 8 yr}\;\;(\approx 0.032\%)",
            font_size=28, color=GREY_B
        ).next_to(den, DOWN, 0.5)

        fib = MathTex(
            r"5,\;8,\;13\;\text{are consecutive Fibonacci numbers}",
            font_size=26, color=GREEN_C
        ).next_to(diff, DOWN, 0.5)

        golden = MathTex(
            r"\frac{13}{8} = 1.625 \;\approx\; \varphi = 1.618\ldots",
            font_size=30, color=GOLD
        ).next_to(fib, DOWN, 0.35)

        self.play(Write(eq1, run_time=2))
        self.wait(1)
        self.play(FadeIn(num, shift=LEFT*0.3))
        self.play(FadeIn(den, shift=LEFT*0.3))
        self.wait(1)
        self.play(Write(diff))
        self.wait(1)
        self.play(Write(fib), Write(golden))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 4 — SYNODIC PERIOD DERIVATION                              ║
# ╚══════════════════════════════════════════════════════════════════════╝

class SynodicPeriod(Scene):
    """Step-by-step derivation of the synodic period formula."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Deriving the Synodic Period",
                      font_size=32, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Step 1 — angular velocities
        s1_lbl = Text("Angular velocities:", font_size=22,
                       color=GREY_B).shift(UP*2 + LEFT*4)
        s1 = MathTex(
            r"\omega_V = \frac{2\pi}{T_V}", r"\qquad",
            r"\omega_E = \frac{2\pi}{T_E}",
            font_size=36
        ).next_to(s1_lbl, DOWN, 0.3, aligned_edge=LEFT)
        s1[0].set_color(VENUS_CLR)
        s1[2].set_color(EARTH_CLR)

        self.play(Write(s1_lbl), Write(s1))
        self.wait(1)

        # Step 2 — relative angular velocity
        s2_lbl = Text("Relative angular velocity (inner faster):",
                       font_size=22, color=GREY_B
                      ).next_to(s1, DOWN, 0.5, aligned_edge=LEFT)
        s2 = MathTex(
            r"\omega_{\text{syn}} = \omega_V - \omega_E "
            r"= \frac{2\pi}{T_V} - \frac{2\pi}{T_E}",
            font_size=34
        ).next_to(s2_lbl, DOWN, 0.25, aligned_edge=LEFT)

        self.play(Write(s2_lbl), Write(s2))
        self.wait(1)

        # Step 3 — synodic period
        s3_lbl = Text("One full lap of relative angle = 2π:",
                       font_size=22, color=GREY_B
                      ).next_to(s2, DOWN, 0.5, aligned_edge=LEFT)
        s3 = MathTex(
            r"\frac{1}{P_{\text{syn}}} = \frac{1}{T_V} - \frac{1}{T_E}",
            font_size=40, color=YELLOW_D
        ).next_to(s3_lbl, DOWN, 0.25)

        box = SurroundingRectangle(s3, color=YELLOW_D, buff=0.15,
                                   stroke_width=2)

        self.play(Write(s3_lbl), Write(s3))
        self.play(Create(box))
        self.wait(1)

        # Step 4 — numerical value
        s4 = MathTex(
            r"P_{\text{syn}} = "
            r"\frac{T_V \cdot T_E}{T_E - T_V} = "
            r"\frac{224.7 \times 365.3}{365.3 - 224.7}"
            r"\approx 583.9\;\text{days}",
            font_size=28
        ).next_to(box, DOWN, 0.5)

        petal_note = Text(
            "5 synodic periods ≈ 8 years → 5 petals",
            font_size=22, color=GREEN_C
        ).next_to(s4, DOWN, 0.4)

        self.play(Write(s4))
        self.play(Write(petal_note))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 5 — GEOCENTRIC FRAME TRANSFORMATION                        ║
# ╚══════════════════════════════════════════════════════════════════════╝

class GeocentricTransform(Scene):
    """Explains heliocentric → geocentric coordinate change."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Reference-Frame Transformation",
                      font_size=30, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Formula
        formula = MathTex(
            r"\vec{r}_{\text{Venus}}^{\,\text{geo}}(t)"
            r"= \vec{r}_{\text{Venus}}^{\,\text{helio}}(t)"
            r"- \vec{r}_{\text{Earth}}^{\,\text{helio}}(t)",
            font_size=34
        ).shift(UP * 1.5)

        self.play(Write(formula, run_time=2))
        self.wait(1)

        # Explanation bullets
        bullets = VGroup(
            Text("• Subtract Earth's heliocentric position at every instant",
                 font_size=20, color=GREY_B),
            Text("• Earth becomes the fixed origin",
                 font_size=20, color=EARTH_CLR),
            Text("• Venus traces a looping, flower-like geocentric path",
                 font_size=20, color=VENUS_CLR),
            Text("• The Sun now appears to orbit Earth (Ptolemaic view)",
                 font_size=20, color=SUN_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(formula, DOWN, 0.6)

        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT*0.2), run_time=0.6)
            self.wait(0.4)

        # Pipeline diagram (text-only)
        pipe = MathTex(
            r"t \;\xrightarrow{\;M=n(t-t_0)\;}\;"
            r"M \;\xrightarrow{\;\text{Kepler}\;}\;"
            r"E \;\xrightarrow{\;\nu(E,e)\;}\;"
            r"\nu \;\rightarrow\; (x,y)",
            font_size=26, color=TEAL_C
        ).next_to(bullets, DOWN, 0.7)

        pipe_lbl = Text("Computation pipeline (each planet)",
                         font_size=18, color=GREY_C).next_to(pipe, DOWN, 0.2)

        self.play(Write(pipe), FadeIn(pipe_lbl))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 6 — THE ROSE OF VENUS (main payoff)                        ║
# ╚══════════════════════════════════════════════════════════════════════╝

class RoseOfVenus(Scene):
    """Draw the 5-petal geocentric flower, one synodic period at a time."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("The Rose of Venus  —  Geocentric Path over 8 Years",
                      font_size=28, color=WHITE).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Earth at centre
        earth = Dot(ORIGIN, radius=0.13, color=EARTH_CLR)
        earth_ring = Circle(radius=0.19, color=EARTH_CLR,
                            stroke_width=1, stroke_opacity=0.4)
        e_lbl = Text("⊕ Earth", font_size=14, color=EARTH_CLR
                     ).next_to(earth, DOWN, 0.15)
        self.play(FadeIn(earth), Create(earth_ring), Write(e_lbl))

        # Year counter
        yr_trk = ValueTracker(0)
        yr_txt = always_redraw(lambda: Text(
            f"Year  {yr_trk.get_value():.2f}",
            font_size=20, color=WHITE
        ).to_corner(UL, buff=0.3))
        self.add(yr_txt)

        # Petal-count label
        pet_trk = ValueTracker(0)
        pet_txt = always_redraw(lambda: Text(
            f"Petal  {int(pet_trk.get_value())} / 5",
            font_size=18, color=GREY_B
        ).next_to(yr_txt, DOWN, 0.15, aligned_edge=LEFT))
        self.add(pet_txt)

        # Draw each petal
        syn = SYNODIC_YR
        conj_dots = VGroup()

        for i in range(N_PETALS):
            t_start = i * syn
            t_end   = (i + 1) * syn
            color   = PETAL_COLORS[i]

            # Build the path VMobject
            petal = geocentric_path_mobject(
                t_start, t_end, n_pts=600, color=color, width=2.2)

            # Animate drawing it
            pet_trk.set_value(i + 1)
            self.play(
                Create(petal, rate_func=linear),
                yr_trk.animate(rate_func=linear).set_value(t_end),
                run_time=4,
            )

            # Mark inferior conjunction (closest approach during this petal)
            best_t, best_d = t_start, 1e9
            for t in np.linspace(t_start, t_end, 800):
                d = np.linalg.norm(venus_geo(t))
                if d < best_d:
                    best_d, best_t = d, t
            cpos = venus_geo(best_t)
            cdot = Dot(cpos, radius=0.07, color=PENTAGRAM_COLOR)
            conj_dots.add(cdot)
            self.play(FadeIn(cdot, scale=1.8), run_time=0.4)

        self.wait(1)

        # Summary annotation
        note = Text(
            "5 petals  ·  5 inferior conjunctions  ·  8 Earth years",
            font_size=20, color=YELLOW_D
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 7 — THE PENTAGRAM OF VENUS                                 ║
# ╚══════════════════════════════════════════════════════════════════════╝

class PentagramOfVenus(Scene):
    """Connect inferior-conjunction points to reveal the pentagram."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("The Pentagram of Venus",
                      font_size=30, color=WHITE).to_edge(UP, buff=0.3)
        self.play(Write(title))

        # Redraw the full rose (faded)
        full_rose = geocentric_path_mobject(0, 8*SYNODIC_YR, n_pts=3000,
                                            color=GREY_D, width=1.0)
        earth = Dot(ORIGIN, radius=0.1, color=EARTH_CLR)
        self.add(full_rose, earth)
        self.play(FadeIn(full_rose), FadeIn(earth))

        # Find conjunction positions
        conj_times = find_inferior_conjunctions(0, 8)
        conj_pos   = [venus_geo(t) for t in conj_times[:5]]

        # Dot each conjunction
        c_dots = VGroup()
        for j, pos in enumerate(conj_pos):
            d = Dot(pos, radius=0.09, color=PENTAGRAM_COLOR)
            lbl = Text(str(j+1), font_size=14, color=WHITE
                       ).next_to(d, normalize(pos[:2])*0.3)
            c_dots.add(VGroup(d, lbl))
            self.play(FadeIn(d, scale=2), Write(lbl), run_time=0.5)

        self.wait(0.5)

        # Draw the pentagram  (connect in temporal order: 1→2→3→4→5→1)
        pent_lines = VGroup()
        for j in range(5):
            line = Line(
                conj_pos[j], conj_pos[(j + 1) % 5],
                color=PENTAGRAM_COLOR, stroke_width=2.5
            )
            pent_lines.add(line)
            self.play(Create(line), run_time=0.7)

        self.wait(0.5)

        # Angular-separation note
        angle_note = MathTex(
            r"\text{Each conjunction advances } \approx 215.6°"
            r"\;\Rightarrow\; 360° - 215.6° = 144.4° \approx \frac{2 \times 360°}{5}",
            font_size=22, color=GREY_B
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(angle_note))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 8 — KEPLER'S LAWS                                          ║
# ╚══════════════════════════════════════════════════════════════════════╝

class KeplerLaws(Scene):
    """Visual summary of Kepler's three laws (foundation for the math)."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        heading = Text("Kepler's Laws of Planetary Motion",
                        font_size=32, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(heading))

        # --- Law 1 ---
        law1_title = Text("I.  The Law of Ellipses", font_size=24,
                           color=YELLOW_D).shift(UP*1.8 + LEFT*2)
        law1_eq = MathTex(
            r"r(\nu) = \frac{a(1-e^2)}{1 + e\cos\nu}",
            font_size=32
        ).next_to(law1_title, DOWN, 0.3, aligned_edge=LEFT)
        law1_txt = Text(
            "Every planet moves in an ellipse with the Sun at one focus.",
            font_size=16, color=GREY_B
        ).next_to(law1_eq, DOWN, 0.2, aligned_edge=LEFT)

        self.play(Write(law1_title))
        self.play(Write(law1_eq), FadeIn(law1_txt))
        self.wait(1)

        # --- Law 2 ---
        law2_title = Text("II.  The Law of Equal Areas", font_size=24,
                           color=YELLOW_D).next_to(law1_txt, DOWN, 0.6,
                                                     aligned_edge=LEFT)
        law2_eq = MathTex(
            r"\frac{dA}{dt} = \frac{L}{2m} = \text{const}",
            font_size=32
        ).next_to(law2_title, DOWN, 0.3, aligned_edge=LEFT)
        law2_txt = Text(
            "A line from the Sun to a planet sweeps equal areas in equal times.",
            font_size=16, color=GREY_B
        ).next_to(law2_eq, DOWN, 0.2, aligned_edge=LEFT)

        self.play(Write(law2_title))
        self.play(Write(law2_eq), FadeIn(law2_txt))
        self.wait(1)

        # --- Law 3 ---
        law3_title = Text("III.  The Harmonic Law", font_size=24,
                           color=YELLOW_D).next_to(law2_txt, DOWN, 0.6,
                                                     aligned_edge=LEFT)
        law3_eq = MathTex(
            r"T^2 = \frac{4\pi^2}{GM_\odot}\,a^3",
            font_size=36
        ).next_to(law3_title, DOWN, 0.3, aligned_edge=LEFT)
        law3_txt = Text(
            "The square of the period ∝ the cube of the semi-major axis.",
            font_size=16, color=GREY_B
        ).next_to(law3_eq, DOWN, 0.2, aligned_edge=LEFT)

        self.play(Write(law3_title))
        self.play(Write(law3_eq), FadeIn(law3_txt))
        self.wait(1)

        # Verify with Venus data
        verify = MathTex(
            r"\text{Check: } \frac{T_V^2}{a_V^3} = "
            r"\frac{(0.6152)^2}{(0.7233)^3} = 1.000",
            font_size=24, color=GREEN_C
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(verify))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 9 — GOLDEN RATIO & FIBONACCI                               ║
# ╚══════════════════════════════════════════════════════════════════════╝

class GoldenRatioConnection(Scene):
    """The 5-8-13 Fibonacci link and golden ratio approximation."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Fibonacci Numbers & the Golden Ratio",
                      font_size=30, color=WHITE).to_edge(UP, buff=0.4)
        self.play(Write(title))

        # Fibonacci sequence
        fib_seq = MathTex(
            r"1,\;1,\;2,\;3,\;", r"5", r",\;", r"8", r",\;", r"13",
            r",\;21,\;34,\;\ldots",
            font_size=36
        ).shift(UP * 1.5)
        fib_seq[1].set_color(RED_C)        # 5 — petals
        fib_seq[3].set_color(EARTH_CLR)    # 8 — Earth years
        fib_seq[5].set_color(VENUS_CLR)    # 13 — Venus orbits

        self.play(Write(fib_seq))
        self.wait(1)

        # Labels
        labels = VGroup(
            Text("5 petals", font_size=18, color=RED_C),
            Text("8 Earth orbits", font_size=18, color=EARTH_CLR),
            Text("13 Venus orbits", font_size=18, color=VENUS_CLR),
        ).arrange(RIGHT, buff=0.8).next_to(fib_seq, DOWN, 0.4)
        self.play(FadeIn(labels))
        self.wait(1)

        # Golden ratio
        phi_eq = MathTex(
            r"\varphi = \frac{1+\sqrt{5}}{2} = 1.6180339\ldots",
            font_size=36, color=GOLD
        ).shift(DOWN * 0.3)

        ratio_eq = MathTex(
            r"\frac{13}{8} = 1.625",
            r"\quad\Rightarrow\quad",
            r"\text{only 0.46\% from } \varphi",
            font_size=28
        ).next_to(phi_eq, DOWN, 0.5)

        self.play(Write(phi_eq))
        self.play(Write(ratio_eq))
        self.wait(1)

        # Why it matters
        why = Text(
            "Nature optimises packing with irrational ratios —\n"
            "the same geometry appears in sunflower seeds,\n"
            "pinecones, and planetary orbits.",
            font_size=18, color=GREY_B, line_spacing=1.3
        ).next_to(ratio_eq, DOWN, 0.6)
        self.play(FadeIn(why))
        self.wait(3)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 10 — PHYSICS CHALLENGE PROBLEMS                            ║
# ╚══════════════════════════════════════════════════════════════════════╝

class PhysicsChallenges(Scene):
    """Display practice problems on-screen for the student."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        title = Text("Physics Challenges", font_size=32,
                      color=YELLOW_D).to_edge(UP, buff=0.4)
        self.play(Write(title))

        problems = [
            ("1.", r"\text{Derive } P_{\text{syn}} \text{ from } "
                   r"\omega_V - \omega_E = \omega_{\text{syn}}."),
            ("2.", r"\text{Use Kepler III to verify } "
                   r"T_V = 224.7 \text{ d given } a_V = 0.7233 \text{ AU.}"),
            ("3.", r"\text{Calculate Venus's orbital velocity at perihelion}"),
            ("4.", r"\text{Show that 5 inferior conjunctions give a pentagram.}"),
            ("5.", r"\text{If } T_E/T_V = \varphi, "
                   r"\text{ does the rose ever close? Why?}"),
            ("6.", r"\text{Compute the precession period of the rose pattern.}"),
        ]

        prob_group = VGroup()
        for num, tex_str in problems:
            line = VGroup(
                Text(num, font_size=22, color=YELLOW_D),
                MathTex(tex_str, font_size=24),
            ).arrange(RIGHT, buff=0.15)
            prob_group.add(line)

        prob_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        prob_group.next_to(title, DOWN, 0.5, aligned_edge=LEFT)
        prob_group.shift(RIGHT * 0.5)

        for p in prob_group:
            self.play(FadeIn(p, shift=RIGHT*0.2), run_time=0.6)
            self.wait(0.3)

        note = Text(
            "Full solutions in practice_problems.tex  (see companion PDF)",
            font_size=16, color=GREY_C
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(note))
        self.wait(4)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  SCENE 11 — CREDITS & SOURCES                                     ║
# ╚══════════════════════════════════════════════════════════════════════╝

class CreditsScene(Scene):
    """Closing credits and data sources."""
    def construct(self):
        self.camera.background_color = BG_COLOR

        lines = VGroup(
            Text("The Dance of Venus & Earth", font_size=36,
                 color=WHITE, weight=BOLD),
            Text("", font_size=10),
            Text("Created by Aaron Sells", font_size=22, color=GREY_B),
            Text("STEM Tutoring  ·  Lee's Summit, MO", font_size=18,
                 color=GREY_C),
            Text("", font_size=10),
            Text("Data Sources", font_size=20, color=YELLOW_D),
            Text("NASA/JPL Planetary Fact Sheet — NSSDC",
                 font_size=16, color=GREY_B),
            Text("JPL Horizons Ephemeris System",
                 font_size=16, color=GREY_B),
            Text("", font_size=10),
            Text("Animation Engine", font_size=20, color=YELLOW_D),
            Text("Manim Community Edition (ManimCE)",
                 font_size=16, color=GREY_B),
            Text("", font_size=10),
            Text("Inspired by: \"Follow Venus Around Earth for 8 Years\"",
                 font_size=16, color=GREY_C),
            Text("— Cosmic Starships (YouTube)",
                 font_size=14, color=GREY_C),
        ).arrange(DOWN, buff=0.12)

        self.play(FadeIn(lines, shift=UP*0.3), run_time=2)
        self.wait(5)
        self.play(FadeOut(lines))


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  END OF FILE                                                       ║
# ╚══════════════════════════════════════════════════════════════════════╝
#
# To render every scene at 1080p:
#     manim -qh venus_earth_dance.py
#
# To render a single scene at 4K:
#     manim -qk venus_earth_dance.py RoseOfVenus
#
# Scenes in recommended viewing order:
#   1. TitleScene
#   2. HeliocentricOrbits
#   3. OrbitalResonance
#   4. SynodicPeriod
#   5. GeocentricTransform
#   6. RoseOfVenus
#   7. PentagramOfVenus
#   8. KeplerLaws
#   9. GoldenRatioConnection
#  10. PhysicsChallenges
#  11. CreditsScene
