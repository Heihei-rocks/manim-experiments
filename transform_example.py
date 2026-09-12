from manim import *

class TransformExample(Scene):
    def construct(self):
        # Create two shapes
        square = Square(color=BLUE)
        circle = Circle(color=RED).scale(0.8)
        
        # Initial arrangement
        self.play(Create(square))
        self.wait()
        
        # Transform square into circle
        self.play(Transform(square, circle))
        self.wait()
        
        # Create text label
        title = Text("Transform Example", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Fade out
        self.play(FadeOut(square), FadeOut(title))
        self.wait()
