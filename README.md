# Manim Experiments

Python Manim Community Edition experiments and examples for creating 3Blue1Brown style mathematical animations.

## Quick Start

```bash
# Setup
uv sync

# Render animation
uv run manim -pql basic_example.py BasicExample

# View GIFs
ls media/animations/*.gif
```

## Project Structure

```
manim-experiments/
├── basic_example.py              # Simple circle
├── animated_line.py              # Axes with moving point
├── transform_example.py          # Shape transformation
├── complex_animation.py          # Grid with animations
├── fibonacci_spiral.py           # Mathematical concept
├── best_practices_demo.py        # Best practices overview
├── recent_showcase.py            # Showcase of experiments
├── docs/
│   └── skills/
│       ├── manim-best-practices.md
│       └── manim-agent-skill.md
├── media/animations/             # Animated GIFs
└── pyproject.toml
```

## Recent Experiments

### 1. Basic Example
Simple circle creation with fill and stroke.

![Basic Example](media/animations/basic_example.gif)

**Code**: `basic_example.py`

### 2. Animated Line
Axes with quadratic function plot and moving point.

![Animated Line](media/animations/animated_line.gif)

**Code**: `animated_line.py`

### 3. Transform Example
Square morphing into circle with text labels.

![Transform Example](media/animations/transform_example.gif)

**Code**: `transform_example.py`

### 4. Complex Animation
9 colored circles in grid with rotation and expansion.

![Complex Animation](media/animations/complex_animation.gif)

**Code**: `complex_animation.py`

### 5. Fibonacci Spiral
Golden ratio concept with growing rectangles.

![Fibonacci Spiral](media/animations/fibonacci_spiral.gif)

**Code**: `fibonacci_spiral.py`

### 6. Best Practices Demo
Overview of key Manim patterns and practices.

![Best Practices Demo](media/animations/best_practices_demo.gif)

**Code**: `best_practices_demo.py`

### 7. Recent Showcase
Summary of all experiments.

![Recent Showcase](media/animations/recent_showcase.gif)

**Code**: `recent_showcase.py`

## Best Practices

### Installation

```bash
# Python environment
uv sync

# Check installation
uv run manim --version
uv run manim checkhealth
```

### Quality Flags

- `-pql`: Preview low quality (fast development)
- `-pm`: Preview medium quality
- `-pqh`: Preview high quality
- `-qk`: 4K quality

### Core Patterns

**Basic Scene**
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))
        self.wait()
```

**Grouping**
```python
group = VGroup(Circle(), Square(), Triangle())
group.arrange(RIGHT)
```

**Sequential Animation**
```python
self.play(*[GrowFromCenter(obj) for obj in objects], lag_ratio=0.1)
```

**Transformations**
```python
self.play(Transform(old_shape, new_shape))
```

## Skills & References

- [Manim Best Practices](docs/skills/manim-best-practices.md) - Comprehensive guide
- [Agent Skill](docs/skills/manim-agent-skill.md) - For AI agents using Manim
- Official docs: https://docs.manim.community/
- GitHub: https://github.com/ManimCommunity/manim

## Existing Skills

- **adithya-s-k/manim_skill**: Comprehensive best practices collection (1,054 stars)
  - URL: https://github.com/adithya-s-k/manim_skill
  - Includes manimce-best-practices with rule files

## Common Pitfalls

1. Version confusion: ManimCE vs ManimGL
2. Missing system dependencies (cairo, ffmpeg, LaTeX)
3. Outdated tutorials with old syntax
4. Performance: Always use low quality for testing

## License

MIT
