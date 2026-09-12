from manim import *
import numpy as np
from scipy.stats import norm

class VariationHistogram(Scene):
    def construct(self):
        title = Text("Data Variation: Histogram → Density", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[0, 0.5, 0.1],
            axis_config={"color": BLUE}
        ).scale(0.8)
        axes.to_edge(DOWN)
        
        # Generate data varying over time
        data = np.random.normal(0, 1, 1000)
        hist, edges = np.histogram(data, bins=30, density=True)
        bars = VGroup(*[Rectangle(width=(edges[i+1]-edges[i])*0.8, height=hist[i]*2, stroke_width=0)
                        for i in range(len(hist))])
        # Simpler: use bar graphs via BarChart?
        self.play(Create(axes))
        self.wait(0.5)
        
        # Morph to smoother density
        curve = axes.plot(lambda x: norm.pdf(x,0,1), color=YELLOW)
        self.play(Create(curve))
        self.wait(2)
        
        text = Text("Variation captured in spread & shape", font_size=24).to_edge(DOWN)
        self.play(Write(text))
        self.wait(2)

class RidgelinePlots(Scene):
    def construct(self):
        title = Text("Ridgeline: Variation Across Conditions", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        
        axes = Axes(x_range=[-5,5], y_range=[-0.5,4], axis_config={"color": GREY})
        curves = VGroup()
        for i in range(5):
            mu = i -2
            curve = axes.plot(lambda x: norm.pdf(x, mu, 0.8), color=interpolate_color(BLUE, RED, i/4))
            curve.shift(UP * i*0.6)
            curves.add(curve)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.2))
        self.wait(3)

class ViolinJitter(Scene):
    def construct(self):
        title = Text("Violin + Jitter: Variation Anatomy", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        
        axes = Axes(x_range=[0,1], y_range=[0,1], axis_config={"color": GREY})
        # Generate points
        points = VGroup()
        for i in range(100):
            x = 0.5 + np.random.normal(0,0.05)
            y = np.random.uniform(0,1)
            dot = Dot(point=axes.c2p(x,y), color=WHITE, radius=0.02)
            points.add(dot)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in points], lag_ratio=0.01))
        self.wait(2)
        
        # Kernel density outline
        xs = np.linspace(0,1,200)
        # simplified density visualization
        self.play(FadeOut(points))
        self.wait(1)

class NovelBreathingData(Scene):
    def construct(self):
        title = Text("Novel: Breathing Variation Field", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create grid of dots that pulse with varying amplitude
        dots = VGroup()
        grid = [[Dot(point=np.array([x, y, 0])*0.5, radius=0.03, color=interpolate_color(TEAL, PURPLE, (x+y)/8))
                 for y in range(-4,5)] for x in range(-4,5)]
        for row in grid:
            for d in row:
                dots.add(d)
        self.add(dots)
        
        # Animate breathing
        def updater(mob, dt):
            t = self.time
            for dot in dots:
                base = np.linalg.norm(dot.get_center()[:2])
                scale = 1 + 0.3*np.sin(t*2 + base)
                dot.scale(scale)
        dots.add_updater(updater)
        self.wait(5)
        dots.remove_updater(updater)
        self.wait(1)
