# Manim Experiments - Reference Documentation

## Installation & Setup

### Prerequisites

```bash
# System dependencies (macOS)
brew install cairo pkg-config ffmpeg

# Python environment
uv init
# Add to pyproject.toml: dependencies = ["manim"]

uv sync
uv run manim --version
```

### Verify Installation

```bash
uv run manim checkhealth
```

## Best Practices

### Scene Structure

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Create
        circle = Circle()
        # Animate
        self.play(Create(circle))
        # Wait
        self.wait(1)
```

### Mobject Organization

```python
# Group related objects
group = VGroup(obj1, obj2, obj3)
group.arrange(RIGHT, buff=0.5)

# Position
obj.to_edge(UP)
obj.next_to(other, DOWN)
obj.move_to(position)
```

### Animation Timing

```python
# Sequential with lag
self.play(*[FadeIn(obj) for obj in objects], lag_ratio=0.1)

# Simultaneous
self.play(Animation1, Animation2, Animation3)

# Chained
self.play(Animation1).then(Animation2)
```

### Common Animation Classes

- **Creation**: Create, Write, FadeIn, DrawBorderThenFill
- **Transform**: Transform, ReplacementTransform, Morph
- **Movement**: MoveTo, Shift, Rotate, Scale
- **Path**: MoveAlongPath, Rotate
- **Timing**: LaggedStart, Succession, AnimationGroup

### Text and Math

```python
# Text
text = Text("Hello", font_size=36)
text = Text("Hello").scale(0.5)

# Math
math = MathTex(r"x^2 + y^2 = r^2")
math = MathTex("y = ", r"x^2")
```

### Axes and Plots

```python
axes = Axes(
    x_range=[-5, 5],
    y_range=[-3, 3],
    axis_config={"color": GREY}
)

graph = axes.plot(lambda x: x**2, color=BLUE)
point = Dot(axes.c2p(1, 1))
```

### Updaters

```python
tracker = ValueTracker(0)
dot = Dot()
dot.add_updater(lambda d: d.move_to(tracker.get_value()))
tracker.set_value(2)
```

### Camera Control

```python
class MyScene(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(1.5)
        self.camera.frame.move_to(ORIGIN)
```

## Quality Guidelines

- **Development**: Always use `-pql` (low quality)
- **Preview**: Use `-pm` (medium quality)
- **Final render**: Use `-pqh` (high quality) or `-qk` (4K)
- **No preview**: Remove `-p` flag

## Common Errors

### Import Error
```python
# Wrong (ManimGL)
from manimlib import *

# Correct (ManimCE)
from manim import *
```

### Animation Error
```python
# Wrong
self.play(circle.scale(1.5))

# Correct
self.play(circle.animate.scale(1.5))
```

### Type Error
```python
# Wrong
self.play(rect1.scale(1.6))

# Correct
self.play(rect1.animate.scale(1.6))
```

## Performance Tips

1. Use low quality for development
2. Minimize number of mobjects
3. Use caching for repeated renders
4. Keep construct() method focused
5. Use .animate for chained transformations

## Resources

- Official Docs: https://docs.manim.community/
- Manim Community: https://github.com/ManimCommunity/manim
- Examples: https://github.com/ManimCommunity/manim/tree/main/examples
- Community Wiki: https://github.com/ManimCommunity/manim/wiki

## Skill Reference

This repository includes two skill documents:

1. **manim-best-practices.md**: Complete best practices guide
2. **manim-agent-skill.md**: Guidelines for AI agents using Manim

Both are in `docs/skills/`.
