# Manim Community Edition - Best Practices Skill

> **Trigger**: User mentions "manim" or "Manim Community" or "ManimCE", or code contains `from manim import *`
>
> **Scope**: Best practices for Manim Community Edition (ManimCE) - the community-maintained Python animation engine. NOT for ManimGL/3b1b version.

## Quick Start

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Create mobjects
        circle = Circle()
        # Add to scene (static)
        self.add(circle)
        # Or animate
        self.play(Create(circle))
        # Wait
        self.wait(1)
```

Render command:
```bash
manim -pql scene.py MyScene  # Preview low quality
manim -pqh scene.py MyScene  # Preview high quality
```

## Core Concepts

### Scene Structure
- **Scene**: Container for animation
- **construct()**: Main method where animation logic lives
- **Scene types**: Scene (2D), ThreeDScene (3D), MovingCameraScene (camera control)

### Mobjects
- **VMobject**: Base class for visual objects
- **Groups**: VGroup for grouping mobjects
- **Positioning**: `to_edge()`, `next_to()`, `arrange()`, `align_to()`

### Animations
- **Creation**: Create, Write, FadeIn, DrawBorderThenFill
- **Transform**: Transform, ReplacementTransform, ApplyMethod
- **Movement**: MoveTo, Rotate, Scale, Shift
- **Timing**: run_time, lag_ratio, rate_func

## Best Practices

### 1. Organize with Groups
```python
shapes = VGroup(Circle(), Square(), Triangle())
shapes.arrange(RIGHT)
```

### 2. Use LaggedStart for Sequencing
```python
self.play(*[GrowFromCenter(obj) for obj in objects], lag_ratio=0.1)
```

### 3. Animate with .animate
```python
circle.animate.scale(1.5).rotate(PI/4)
```

### 4. Use ValueTracker for Dynamic Animations
```python
tracker = ValueTracker(0)
dot = Dot().add_updater(lambda d: d.move_to(tracker.get_value()))
```

### 5. Quality Flags for Development
- `-ql`: Low quality (fast iteration)
- `-qm`: Medium quality
- `-qh`: High quality
- `-qk`: 4k quality

## Common Pitfalls

1. **Version confusion**: ManimCE uses `from manim import *`, ManimGL uses `from manimlib import *`
2. **Missing dependencies**: Ensure cairo, pkg-config, ffmpeg, LaTeX installed
3. **Outdated tutorials**: Many videos reference old ManimGL syntax
4. **Text rendering**: Requires manimpango
5. **Performance**: Use low quality for testing

## Installation

```bash
pip install manim
manim checkhealth
```

## Resources

- Official docs: https://docs.manim.community/
- GitHub: https://github.com/ManimCommunity/manim
- Examples: https://github.com/ManimCommunity/manim/tree/main/examples
