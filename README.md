# Manim Experiments

Python Manim Community Edition (v0.21.0) experiments using Grant Sanderson's library.

## Setup

This project uses `uv` for Python environment management.

```bash
uv sync
uv run manim --version
```

## Best Practices Research

### Key Skills/Agents
- **adithya-s-k/manim_skill**: Comprehensive collection of best practices, patterns, examples (1,054 stars)
  - URL: https://github.com/adithya-s-k/manim_skill
  - Includes manimce-best-practices skill
- **manim_skill**: Open-source AI agent skill (yusuke710)
  - URL: https://github.com/adithya-s-k/manim_skill
- **Alternative skills**: animo.video/skills directory, skillsllm.com/manim-skill

### Installation Best Practices
1. **Use uv** for Python version management (project configured for Python 3.11)
2. **Install prerequisites**: cairo, pkg-config, ffmpeg, LaTeX
3. **Use `pip install manim`** for Community Edition
4. **Check health**: `manim checkhealth`
5. **Quality flags**: -ql (low), -qm (medium), -qh (high), -qk (4k)
6. **Development**: Always use `-pql` for preview low quality
7. **Separate projects**: Each project gets its own virtual environment

### Common Pitfalls
- Version confusion: Manim Community (`from manim import *`, `manim` CLI) vs ManimGL (`from manimlib import *`, `manimgl` CLI)
- Missing system dependencies (cairo, pkg-config, ffmpeg)
- Outdated tutorials referencing old ManimGL syntax
- Text rendering requires manimpango
- LaTeX required for MathTex
- Performance: Use quality flags appropriately

### Recommended Workflow for Agents
1. **Research**: Check official docs (docs.manim.community), examples
2. **Storyboard**: Break animation into chunks
3. **Map primitives**: Identify Manim mobjects/animations needed
4. **Generate code**: Follow patterns from manim_skill
5. **Render**: Use low quality for testing, high for final
6. **Iterate**: Adjust timing, positioning, colors

## Examples

See `*.py` files for various animation examples:
- basic_example.py - Simple circle
- animated_line.py - Axes with moving point
- transform_example.py - Shape transformation
- complex_animation.py - Grid with animations
- fibonacci_spiral.py - Mathematical concept

## Rendering

```bash
# Low quality preview (fast)
uv run manim -pql scene.py SceneName

# Medium quality
uv run manim -pm scene.py SceneName

# High quality
uv run manim -pqh scene.py SceneName

# No preview, just render
uv run manim -ql scene.py SceneName
```

Videos output to `media/videos/<scene>/480p15/<Scene>.mp4`
