from manim import *

class ComplexAnimation(Scene):
    def construct(self):
        # Create grid of shapes
        shapes = VGroup(*[Circle(radius=0.3, fill_opacity=0.7) for _ in range(9)])
        shapes.arrange_in_grid(rows=3, cols=3)
        
        # Color them differently
        colors = [RED, BLUE, GREEN, ORANGE, PURPLE, YELLOW, TEAL, PINK, WHITE]
        for i, shape in enumerate(shapes):
            shape.set_fill(colors[i % len(colors)], opacity=0.6)
            shape.set_stroke(colors[i % len(colors)], width=2)
        
        # Animate in sequence
        self.play(*[GrowFromCenter(shape) for shape in shapes], lag_ratio=0.1)
        self.wait(0.5)
        
        # Rotate entire group
        self.play(Rotate(shapes, angle=PI/4), run_time=2)
        self.wait(0.5)
        
        # Move shapes outward
        center = shapes.get_center()
        for shape in shapes:
            end_pos = shape.get_center() * 1.5
            self.play(shape.move_to(end_pos).animate.scale(0.8), lag_ratio=0.05)
        self.wait(1)
