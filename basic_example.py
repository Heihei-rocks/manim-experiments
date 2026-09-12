from manim import *
class BasicExample(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)
        self.play(Create(circle))
        self.wait()
