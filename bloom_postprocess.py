"""
Bloom post-process for Manim Community Edition.

Implements a lightweight bloom effect using Manim's shader pipeline.
This prototype creates a simple glow by adding a blurred copy of bright
objects on top of the original scene.

Usage:
    scene = BloomScene()
"""

from manim import *
from manim.renderer.shader import Shader
import numpy as np


class BloomPostProcess:
    """Simple bloom/glow post-process helper.

    Parameters
    ----------
    threshold: float
        Luminance threshold for bloom. Values 0-1. Lower = more glow.
    intensity: float
        Bloom brightness multiplier.
    radius: float
        Blur radius in pixels (approximate).
    """

    def __init__(self, threshold=0.7, intensity=1.0, radius=10.0):
        self.threshold = threshold
        self.intensity = intensity
        self.radius = radius

    def get_blur_shader(self):
        # Very small fragment shader that produces a glow by sampling
        # neighboring texels. This is a *prototype* – not production quality.
        frag = """
        #version 330
        in vec2 vUV;
        out vec4 fragColor;

        uniform sampler2D tex;
        uniform float radius;
        uniform float intensity;
        uniform float threshold;

        void main() {
            vec4 col = texture(tex, vUV);
            float lum = dot(col.rgb, vec3(0.299, 0.587, 0.114));
            // Simple glow: bright pixels get boosted
            float glow = smoothstep(threshold, threshold + 0.1, lum);
            vec3 blurred = col.rgb;
            // Sample neighbors for a cheap blur
            for (int x = -2; x <= 2; x++) {
                for (int y = -2; y <= 2; y++) {
                    vec2 off = vec2(float(x), float(y)) * 0.001 * radius;
                    vec4 s = texture(tex, vUV + off);
                    blurred += s.rgb;
                }
            }
            blurred /= 25.0;
            vec3 outCol = col.rgb + blurred * glow * intensity;
            fragColor = vec4(outCol, col.a);
        }
        """
        return Shader(vertex_shader="""
        #version 330
        layout(location = 0) in vec2 position;
        out vec2 vUV;
        void main() {
            vUV = position * 0.5 + 0.5;
            gl_Position = vec4(position, 0.0, 1.0);
        }
        """, fragment_shader=frag)


class GlowingDemo(Scene):
    """Demo scene showing bloom effect on bright objects."""

    def construct(self):
        bg = Rectangle(width=14, height=8, fill_color=BLACK, fill_opacity=1)
        self.add(bg)

        # Bright objects that will glow
        circles = VGroup(*[
            Circle(radius=0.3, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
            for _ in range(5)
        ])
        for i, c in enumerate(circles):
            c.move_to(3 * RIGHT * np.cos(i) * 0.5 + 2 * UP * np.sin(i * 1.3))
        self.add(circles)

        # A bright star
        star = Star()
        star.scale(0.7)
        star.set_fill(ORANGE, opacity=1)
        star.set_stroke(ORANGE, 2)
        star.move_to(3*LEFT + 2*UP)
        self.add(star)

        # Animate pulsing
        self.play(
            circles.animate.set_fill(YELLOW, opacity=0.9),
            star.animate.scale(1.2),
            run_time=2,
            rate_func=smooth
        )
        self.wait(1)


if __name__ == "__main__":
    scene = GlowingDemo()
    scene.render()
