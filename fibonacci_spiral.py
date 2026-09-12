from manim import *

class FibonacciSpiral(Scene):
    def construct(self):
        # Create Fibonacci word description
        title = Text("Fibonacci Spiral", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Animation of golden ratio growth
        axes = Axes(
            x_range=[0, 1],
            y_range=[0, 1],
            axis_config={"color": GREY_BROWN}
        ).scale(0.5).shift(LEFT*2)
        
        # Simple rectangle growth
        rect_width = 1
        rect_height = 0.6
        
        rect1 = Rectangle(width=rect_width, height=rect_height, color=BLUE, fill_opacity=0.5)
        rect1.move_to(ORIGIN)
        
        rect2 = Rectangle(width=rect_height, height=rect_width*0.8, color=RED, fill_opacity=0.5)
        rect2.next_to(rect1, RIGHT)
        
        self.play(Create(rect1), Create(rect2))
        self.wait(0.5)
        
        # Animate
        self.play(rect1.animate.scale(1.6), rect2.animate.scale(1.6))
        self.wait()
        
        # Add golden ratio label
        phi_text = Text("φ ≈ 1.618", font_size=28).next_to(title, DOWN)
        self.play(Write(phi_text))
        self.wait(2)
