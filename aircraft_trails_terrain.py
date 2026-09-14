from manim import *
import numpy as np

class AircraftTrails2D(Scene):
    def construct(self):
        title = Text("Aircraft Trails - 2D Top-Down", font_size=24, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
        )
        # Skip axis labels to avoid LaTeX dependency
        # axes_labels = axes.get_axis_labels(x_label="X", y_label="Y")

        # Elliptical flight path
        path = VMobject()
        t_vals = np.linspace(0, 2*np.pi, 300)
        points = [axes.c2p(6*np.cos(t), 4*np.sin(2*t)) for t in t_vals]
        path.set_points_smoothly(points)
        path.set_stroke(WHITE, 1, opacity=0.3)

        # Aircraft with blue glow
        aircraft = Triangle().scale(0.2).rotate(PI/2).set_fill(BLUE, opacity=0.8).set_stroke(BLUE, width=2)
        trail = TracedPath(aircraft.get_center, stroke_color=RED, stroke_width=3, dissipating_time=2)

        # Sensor pulse rings
        sensor_pulses = VGroup()

        self.add(axes, path, trail, aircraft)

        # Aircraft movement tracker
        aircraft.time = 0
        aircraft.current_angle = PI/2  # Initial rotation

        def aircraft_updater(mob, dt):
            mob.time += dt / 5  # 5 second total flight
            if mob.time > 1:
                mob.time = 1
            mob.move_to(path.point_from_proportion(mob.time))
            # Rotate to face direction of movement
            if mob.time < 0.99:
                next_pos = path.point_from_proportion(min(mob.time + 0.01, 1))
                curr_pos = mob.get_center()
                angle = np.arctan2(next_pos[1] - curr_pos[1], next_pos[0] - curr_pos[0])
                mob.rotate(angle - mob.current_angle)
                mob.current_angle = angle

        # Sensor pulse creator
        def create_sensor_pulse():
            pulse = Circle(radius=0.1, color=BLUE_C, stroke_width=2)
            pulse.move_to(aircraft.get_center())
            sensor_pulses.add(pulse)
            self.add(pulse)
            self.play(
                pulse.animate.scale(15).set_stroke(opacity=0),
                run_time=1.5,
                rate_func=linear
            )
            self.remove(pulse)
            sensor_pulses.remove(pulse)

        aircraft.add_updater(aircraft_updater)

        # Emit sensor pulses periodically
        for i in range(5):
            self.wait(1)
            create_sensor_pulse()

        aircraft.remove_updater(aircraft_updater)
        self.wait(0.5)


class Terrain3DAircraft(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=0.8)

        title = Text("Aircraft Over Terrain - 3D", font_size=28, font="Monospace")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # Enhanced terrain with varied topology
        def terrain_func(u, v):
            x = u * 8 - 4
            y = v * 8 - 4
            # Multi-frequency terrain for realistic topology
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
        terrain.set_style(
            fill_opacity=0.7,
            stroke_color=TEAL,
            stroke_width=0.5,
            stroke_opacity=0.3
        )
        # Simplified solid color terrain
        terrain.set_fill(GREEN_D, opacity=0.7)

        self.add(title, terrain)
        self.wait(0.5)

        # Complex 3D flight path - spiral with elevation changes
        t_range = np.linspace(0, 4*PI, 300)
        path_points = []
        for t in t_range:
            x = 3 * np.cos(t/2)
            y = 3 * np.sin(t/2)
            z = 1.2 + 0.6*np.sin(t) + 0.3*np.cos(t*2)
            path_points.append(np.array([x, y, z]))

        path = VMobject()
        path.set_points_smoothly(path_points)
        path.set_stroke(GREEN, 2, opacity=0.4)

        # Aircraft (cone pointing in flight direction)
        aircraft = Cone(
            base_radius=0.2,
            height=0.5,
            direction=RIGHT
        ).set_fill(ORANGE, opacity=0.95).set_stroke(YELLOW, width=1)

        # Multi-colored fading trail
        trail = TracedPath(
            aircraft.get_center,
            stroke_color=YELLOW,
            stroke_width=4,
            dissipating_time=3.5
        )

        self.add(path, trail, aircraft)

        # Add sensor coverage sphere that follows aircraft
        sensor_sphere = Sphere(radius=1.5, resolution=(12, 12))
        sensor_sphere.set_fill(BLUE_C, opacity=0.15)
        sensor_sphere.set_stroke(BLUE_C, width=1, opacity=0.3)
        sensor_sphere.move_to(aircraft.get_center())
        self.add(sensor_sphere)

        # Updater to keep sensor with aircraft
        sensor_sphere.add_updater(lambda m: m.move_to(aircraft.get_center()))

        # Animate along path with camera following
        self.play(
            MoveAlongPath(aircraft, path),
            run_time=12,
            rate_func=linear
        )

        sensor_sphere.clear_updaters()

        # Rotate camera for final view
        self.move_camera(phi=75*DEGREES, theta=-30*DEGREES, run_time=2)
        self.wait(1)


class MultiAircraftFormation(ThreeDScene):
    """Novel: Multiple coordinated aircraft with synchronized sensor coverage"""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES, zoom=0.7)

        title = Text("Formation Flight: Coordinated Sensor Coverage", font_size=26, font="Monospace")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # Simplified terrain
        def terrain_func(u, v):
            x = u * 10 - 5
            y = v * 10 - 5
            z = 0.3 * np.sin(x/2) * np.cos(y/2)
            return np.array([x, y, z])

        terrain = Surface(terrain_func, u_range=[0, 1], v_range=[0, 1], resolution=(30, 30))
        terrain.set_style(fill_opacity=0.6, stroke_width=0.5, stroke_opacity=0.2)
        terrain.set_fill(GREEN_E, opacity=0.6)

        self.add(title, terrain)

        # Create formation of 3 aircraft
        colors = [RED, BLUE, GREEN]
        aircraft_group = VGroup()
        trails = VGroup()

        for i, color in enumerate(colors):
            # Create circular paths at different radii and heights
            radius = 2.5 + i * 0.5
            height = 1.5 + i * 0.3

            t_vals = np.linspace(0, 2*PI, 200)
            offset = i * 2*PI/3  # 120 degree spacing

            path_points = [
                np.array([
                    radius * np.cos(t + offset),
                    radius * np.sin(t + offset),
                    height + 0.2*np.sin(3*t)
                ]) for t in t_vals
            ]

            path = VMobject().set_points_smoothly(path_points)
            path.set_stroke(color, 1, opacity=0.3)

            aircraft = Cone(base_radius=0.15, height=0.4, direction=RIGHT)
            aircraft.set_fill(color, opacity=0.9)
            aircraft.set_stroke(color, width=1)

            trail = TracedPath(aircraft.get_center, stroke_color=color, stroke_width=3, dissipating_time=2.5)
            trails.add(trail)

            aircraft.path = path
            aircraft.param = 0
            aircraft_group.add(aircraft)
            self.add(path, trail)

        self.add(aircraft_group)

        # Coordinated movement updater
        def formation_updater(mob, dt):
            for i, aircraft in enumerate(mob):
                aircraft.param += dt / 8
                if aircraft.param <= 1:
                    pos = aircraft.path.point_from_proportion(aircraft.param)
                    aircraft.move_to(pos)

        aircraft_group.add_updater(formation_updater)

        # Begin ambient rotation
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(8)

        aircraft_group.clear_updaters()
        self.stop_ambient_camera_rotation()
        self.wait(1)


class SensorHeatmapTerrain(Scene):
    """Novel: Sensor coverage intensity heat map over 2D terrain"""

    def construct(self):
        title = Text("Sensor Coverage Heat Map: Accumulated Intensity", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # Create grid for heat map
        grid_size = 20
        cell_size = 0.4

        # Initialize grid with zeros
        heat_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

        # Create visual grid
        cells = VGroup()
        for i in range(grid_size):
            for j in range(grid_size):
                x = (i - grid_size/2) * cell_size
                y = (j - grid_size/2) * cell_size
                cell = Square(side_length=cell_size, stroke_width=0.5, stroke_opacity=0.3)
                cell.move_to(np.array([x, y, 0]))
                cell.set_fill(BLUE, opacity=0.1)
                cell.grid_i = i
                cell.grid_j = j
                cells.add(cell)

        self.add(cells)

        # Aircraft path
        t_vals = np.linspace(0, 4*PI, 300)
        path_points = [np.array([3*np.cos(t/2), 2.5*np.sin(t/2), 0]) for t in t_vals]
        path = VMobject().set_points_smoothly(path_points)
        path.set_stroke(WHITE, 1, opacity=0.3)

        aircraft = Triangle().scale(0.15).rotate(PI/2).set_fill(YELLOW, opacity=1).set_stroke(YELLOW, width=2)

        self.add(path, aircraft)

        sensor_range = 2.0

        # Update heat map as aircraft moves
        def update_heatmap(mob, alpha):
            pos = path.point_from_proportion(alpha)
            aircraft.move_to(pos)

            # Update cells within sensor range
            for cell in cells:
                cell_pos = cell.get_center()
                dist = np.linalg.norm(pos - cell_pos)

                if dist < sensor_range:
                    # Add heat based on proximity (inverse square-ish)
                    heat_add = (1 - dist/sensor_range) * 0.15
                    i, j = cell.grid_i, cell.grid_j
                    heat_grid[i][j] = min(heat_grid[i][j] + heat_add, 1.0)

                    # Update color - blue to red based on heat
                    heat = heat_grid[i][j]
                    color = interpolate_color(BLUE, RED, heat)
                    cell.set_fill(color, opacity=0.3 + 0.6*heat)

        self.play(
            UpdateFromAlphaFunc(aircraft, update_heatmap),
            run_time=10,
            rate_func=linear
        )

        # Final annotation
        annotation = Text("Red = High Coverage | Blue = Low Coverage", font_size=20, color=GRAY, font="Monospace")
        annotation.to_edge(DOWN)
        self.play(FadeIn(annotation))
        self.wait(2)
