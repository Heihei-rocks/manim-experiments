from manim import *
import numpy as np

class AircraftTrails2D(Scene):
    def construct(self):
        title = Text("Aircraft Trails – 2D Top-Down", font_size=24)
        title.to_edge(UP)
        self.add(title)
        
        axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
        )
        axes_labels = axes.get_axis_labels(x_label="X", y_label="Y")
        
        path = VMobject()
        t_vals = np.linspace(0, 2*np.pi, 300)
        points = [axes.c2p(6*np.cos(t), 4*np.sin(2*t)) for t in t_vals]
        path.set_points_smoothly(points)
        path.set_stroke(WHITE, 1, "rough")
        
        aircraft = Triangle().scale(0.2).rotate(PI/2).set_fill(BLUE, opacity=0.8).set_stroke(BLUE)
        trail = TracedPath(aircraft.get_center, stroke_color=RED, stroke_width=3, dissipating_time=2)
        
        self.add(axes, axes_labels, path, trail, aircraft)
        
        def updater(mob, dt):
            mob.move_to(path.point_from_proportion(mob.time))
            mob.rotate(0.05)
        
        aircraft.add_updater(updater)
        self.wait(5)


class Terrain3DAircraft(ThreeDScene):
    def construct(self):
        title = Text("Aircraft Over Terrain – 3D", font_size=24)
        title.to_edge(UP)
        title.move_to(title.get_center().add(UP*3))
        
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # Simple terrain surface
        def terrain_func(u, v):
            x = u * 4 - 4
            y = v * 4 - 4
            z = np.sin(np.sqrt(x**2 + y**2) / 2) * 0.5
            return np.array([x, y, z])
        
        terrain = Surface(terrain_func, u_range=[0, 1], v_range=[0, 1])
        terrain.set_stroke(opacity=0.2)
        terrain.set_fill(GRAY, opacity=0.6)
        self.add(terrain)
        
        # Flight path
        t = np.linspace(0, 1, 200)
        path_points = [np.array([ -4 + 8*t_i, -4 + 8*t_i, 1 + 0.5*np.sin(t_i*10)]) for t_i in t]
        path = VMobject()
        path.set_points_smoothly(path_points)
        path.set_stroke(GREEN, 3)
        
        # Aircraft
        aircraft = Cone(height=0.4, side_length=0.6).set_fill(ORANGE, opacity=0.9)
        trail = TracedPath(aircraft.get_center, stroke_color=YELLOW, stroke_width=4, dissipating_time=3)
        
        self.add(path, trail, aircraft)
        
        # Move aircraft along path
        self.play(
            MoveAlongPath(aircraft, path),
            run_time=10,
            rate_func=linear
        )
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
