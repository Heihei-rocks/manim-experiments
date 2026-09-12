# Manim Examples

Quick reference for common animation patterns.

## Basic Shapes

```python
from manim import *

class Shapes(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        square = Square(color=RED)
        triangle = Triangle(color=GREEN)
        
        self.play(Create(circle))
        self.play(Create(square))
        self.play(Create(triangle))
```

## Text and Math

```python
class TextMath(Scene):
    def construct(self):
        text = Text("Hello Manim", font_size=36)
        math = MathTex(r"E = mc^2")
        
        self.play(Write(text))
        self.play(Write(math))
```

## Axes and Plots

```python
class PlotExample(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-2, 2]
        )
        
        graph = axes.plot(lambda x: x**2, color=BLUE)
        
        self.play(Create(axes))
        self.play(Create(graph))
```

## Transformations

```python
class TransformExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        
        self.play(Create(square))
        self.play(Transform(square, circle))
```

## Grouping

```python
class GroupExample(Scene):
    def construct(self):
        group = VGroup(
            Circle(),
            Square(),
            Triangle()
        )
        group.arrange(RIGHT)
        
        self.play(Create(group))
```

## Sequential Animation

```python
class SequentialExample(Scene):
    def construct(self):
        dots = VGroup(*[Dot() for _ in range(5)])
        dots.arrange(RIGHT)
        
        self.play(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.1)
```

## Dynamic Animation

```python
class DynamicExample(Scene):
    def construct(self):
        tracker = ValueTracker(0)
        dot = Dot().add_updater(
            lambda d: d.move_to(tracker.get_value())
        )
        
        self.play(tracker.animate.set_value(2))
```

## 3D Scene

```python
class ThreeDExample(ThreeDScene):
    def construct(self):
        sphere = Sphere()
        self.set_camera_orientation(phi=75*DEGREES, theta=30*DEGREES)
        self.play(Create(sphere))
```

## Camera Movement

```python
class CameraExample(MovingCameraScene):
    def construct(self):
        text = Text("Hello")
        
        self.play(self.camera.frame.animate.scale(1.5))
        self.play(self.camera.frame.animate.move_to(text))
```

## Complete Examples

See the main examples in the root directory:
- basic_example.py
- animated_line.py
- transform_example.py
- complex_animation.py
- fibonacci_spiral.py
- best_practices_demo.py
