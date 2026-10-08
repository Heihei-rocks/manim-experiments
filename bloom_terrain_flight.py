"""
Bloom-enhanced 3D flight over terrain demo.

Based on Terrain3DAircraft from aircraft_trails_terrain.py.
Bright emissive aircraft and trails are rendered for a post-process bloom pass.
"""

from manim import *
import numpy as np


class BloomFlightTerrain3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES, zoom=0.9)

        title = Text("Bloom Flight Over Terrain", font_size=28, font="Monospace")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # Terrain
        def terrain_func(u, v):
            x = u * 8 - 4
            y = v * 8 - 4
            z = (0.4 * np.sin(np.sqrt(x**2 + y**2) / 1.5) +
                 0.2 * np.sin(x * 1.5) * np.cos(y * 1.5) +
                 0.1 * np.sin(x * 3) * np.sin(y * 3))
            return np.array([x, y, z])

        terrain = Surface(
            terrain_func,
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(40, 40)
        )
        terrain.set_style(fill_opacity=0.6, stroke_color=TEAL, stroke_width=0.5, stroke_opacity=0.2)
        terrain.set_fill(GREEN_D, opacity=0.6)
        self.add(terrain)

        # Flight path
        t_range = np.linspace(0, 4*PI, 300)
        path_points = []
        for t in t_range:
            x = 3 * np.cos(t/2)
            y = 3 * np.sin(t/2)
            z = 1.2 + 0.6*np.sin(t) + 0.3*np.cos(t*2)
            path_points.append(np.array([x, y, z]))

        path = VMobject()
        path.set_points_smoothly(path_points)
        path.set_stroke(YELLOW, 3, opacity=0.8)
        self.add(path)

        # Bright emissive aircraft
        aircraft = Cone(base_radius=0.2, height=0.5, direction=RIGHT)
        aircraft.set_fill(YELLOW, opacity=1.0)
        aircraft.set_stroke(YELLOW, width=4)
        self.add(aircraft)

        # Bright fading trail
        trail = TracedPath(
            aircraft.get_center,
            stroke_color=YELLOW,
            stroke_width=8,
            dissipating_time=3.5
        )
        self.add(trail)

        # Sensor sphere with transparency
        sensor_sphere = Sphere(radius=1.5, resolution=(12, 12))
        sensor_sphere.set_fill(BLUE_C, opacity=0.15)
        sensor_sphere.set_stroke(BLUE_C, width=1, opacity=0.3)
        sensor_sphere.move_to(aircraft.get_center())
        self.add(sensor_sphere)
        sensor_sphere.add_updater(lambda m: m.move_to(aircraft.get_center()))

        # Move aircraft along path
        self.play(
            MoveAlongPath(aircraft, path),
            run_time=12,
            rate_func=linear
        )

        sensor_sphere.clear_updaters()
        self.move_camera(phi=75*DEGREES, theta=-30*DEGREES, run_time=2)
        self.wait(1)
