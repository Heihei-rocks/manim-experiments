# Manim Agent Skill

A comprehensive collection of best practices, patterns, and examples for creating 3Blue1Brown style animations with Manim Community Edition.

## For AI Agents

This skill helps AI coding agents effectively use Manim by providing:

1. **Pattern library**: Proven code patterns for common animations
2. **Best practices**: Guidelines for clean, maintainable Manim code
3. **Templates**: Starting points for new scenes
4. **Examples**: Real working examples with explanations

## Agent Workflow

```
User request → Storyboard → Identify primitives → Map to Manim → Generate code → Render → Iterate
```

### Step 1: Understand Request
Break down user request into animation components:
- Visual elements (shapes, text, plots)
- Transformations (movement, scaling, morphing)
- Timing and sequencing
- Styling

### Step 2: Map to Manim Primitives
- Shapes → Circle, Square, Polygon, etc.
- Text → Text, MathTex
- Plots → Axes, Graph
- Animations → Create, Transform, FadeIn/Out, etc.

### Step 3: Generate Code
Follow patterns from docs/skills/manim-best-practices.md

### Step 4: Render and Verify
Use low quality for testing: `manim -pql scene.py SceneName`

## Key Rules

1. **Always use Manim Community Edition** (`from manim import *`)
2. **Group related mobjects** with VGroup
3. **Use descriptive variable names**
4. **Keep construct() method focused**
5. **Use lag_ratio for sequencing**
6. **Test with low quality first**

## Example Patterns

### Pattern: Reveal sequence
```python
self.play(*[FadeIn(obj) for obj in objects], lag_ratio=0.1)
```

### Pattern: Morphing
```python
self.play(Transform(old_shape, new_shape))
```

### Pattern: Moving point along path
```python
point = Dot()
self.play(MoveAlongPath(point, path))
```

## References

- [Manim Community Docs](https://docs.manim.community/)
- [Best Practices](./manim-best-practices.md)
- [Examples](../examples/)
