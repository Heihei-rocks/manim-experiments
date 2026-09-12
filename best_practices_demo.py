from manim import *

class BestPracticesDemo(Scene):
    def construct(self):
        title = Text("Manim Best Practices", font_size=48)
        title.to_edge(UP)
        subtitle = Text("Community Edition v0.21.0", font_size=24, color=GRAY)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title), Write(subtitle))
        self.wait(0.5)
        
        # Practice 1: Grouping and organization
        group_title = Text("1. Group & Organize", font_size=28).to_edge(LEFT)
        self.play(Write(group_title))
        
        shapes = VGroup(
            Circle(radius=0.3, color=BLUE),
            Square(side_length=0.6, color=RED),
            Triangle(color=GREEN)
        )
        shapes.arrange(RIGHT, buff=0.5)
        shapes.shift(DOWN*1)
        
        self.play(Create(shapes))
        self.play(shapes.animate.scale(1.2).rotate(PI/6))
        self.wait(0.5)
        
        # Practice 2: Animation timing
        timing_title = Text("2. Timing Control", font_size=28).to_edge(LEFT)
        self.play(Transform(group_title, timing_title), FadeOut(shapes))
        
        dots = VGroup(*[Dot(color=YELLOW) for _ in range(5)])
        dots.arrange(RIGHT, buff=0.3)
        dots.shift(DOWN*1)
        
        self.play(
            *[GrowFromCenter(dot) for dot in dots],
            lag_ratio=0.2
        )
        self.wait(0.5)
        
        # Practice 3: Axes and plots
        plot_title = Text("3. Axes & Plots", font_size=28).to_edge(LEFT)
        self.play(Transform(timing_title, plot_title), FadeOut(dots))
        
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-2, 2],
            axis_config={"color": GREY}
        ).scale(0.7).shift(DOWN*1)
        
        graph = axes.plot(lambda x: np.sin(x), color=BLUE)
        self.play(Create(axes), Create(graph))
        self.wait(0.5)
        
        # Practice 4: Transformations
        transform_title = Text("4. Transforms", font_size=28).to_edge(LEFT)
        self.play(Transform(plot_title, transform_title), FadeOut(axes), FadeOut(graph))
        
        orig = Circle(radius=0.5, color=ORANGE)
        dest = Square(side_length=1, color=PURPLE)
        dest.move_to(orig.get_center())
        
        self.play(Create(orig))
        self.play(Transform(orig, dest))
        self.wait(0.5)
        
        # Outro
        self.play(FadeOut(transform_title), FadeOut(orig))
        outro = Text("Good animation = clear primitives", font_size=32).shift(DOWN*0.5)
        self.play(Write(outro))
        self.wait(2)
