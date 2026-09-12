from manim import *

class RecentExperimentShowcase(Scene):
    def construct(self):
        title = Text("Recent Experiments", font_size=40).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # Show each experiment name
        experiments = [
            ("Basic Example", BLUE),
            ("Animated Line", GREEN),
            ("Transform", ORANGE),
            ("Complex Grid", PURPLE),
            ("Fibonacci", RED),
        ]
        
        for name, color in experiments:
            text = Text(name, font_size=36, color=color)
            text.move_to(ORIGIN)
            self.play(Write(text))
            self.wait(0.7)
            self.play(FadeOut(text))
        
        self.play(FadeOut(title))
        conclusion = Text("Manim Community Edition", font_size=32).move_to(ORIGIN)
        self.play(Write(conclusion))
        self.wait(2)
