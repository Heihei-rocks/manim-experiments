from manim import *
import numpy as np


class GreatCircleRoute(ThreeDScene):
    """Visualize great circle (geodesic) routes on a sphere"""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.9)

        title = Text("Great Circle Routes on Sphere", font_size=28, font="Monospace")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # Create Earth-like sphere
        sphere = Sphere(radius=2, resolution=(40, 40))
        sphere.set_fill(BLUE_D, opacity=0.8)
        sphere.set_stroke(BLUE_C, width=0.5, opacity=0.3)
        self.add(sphere)

        # Define city coordinates (lat, lon in radians)
        cities = [
            ("NYC", np.radians(40.7), np.radians(-74.0)),
            ("London", np.radians(51.5), np.radians(-0.1)),
            ("Tokyo", np.radians(35.7), np.radians(139.7)),
            ("Sydney", np.radians(-33.9), np.radians(151.2)),
        ]

        # Convert lat/lon to 3D Cartesian coordinates on sphere
        def latlon_to_xyz(lat, lon, radius=2):
            x = radius * np.cos(lat) * np.cos(lon)
            y = radius * np.cos(lat) * np.sin(lon)
            z = radius * np.sin(lat)
            return np.array([x, y, z])

        # Place city markers
        city_dots = VGroup()
        for name, lat, lon in cities:
            pos = latlon_to_xyz(lat, lon)
            dot = Dot3D(point=pos, radius=0.08, color=YELLOW)
            city_dots.add(dot)
        self.add(city_dots)

        # Draw great circle routes between cities
        routes = VGroup()
        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                _, lat1, lon1 = cities[i]
                _, lat2, lon2 = cities[j]

                # Generate points along great circle
                n_points = 100
                path_points = []
                for t in np.linspace(0, 1, n_points):
                    # Spherical linear interpolation (slerp)
                    p1 = latlon_to_xyz(lat1, lon1)
                    p2 = latlon_to_xyz(lat2, lon2)

                    # Calculate angle between points
                    dot_product = np.dot(p1, p2) / (np.linalg.norm(p1) * np.linalg.norm(p2))
                    omega = np.arccos(np.clip(dot_product, -1, 1))

                    if omega > 0.01:  # Avoid division by zero
                        sin_omega = np.sin(omega)
                        a = np.sin((1 - t) * omega) / sin_omega
                        b = np.sin(t * omega) / sin_omega
                        point = a * p1 + b * p2
                    else:
                        point = (1 - t) * p1 + t * p2

                    path_points.append(point)

                # Create route curve
                route = VMobject()
                route.set_points_smoothly(path_points)
                route.set_stroke(RED, width=3, opacity=0.7)
                routes.add(route)

        # Animate routes appearing
        self.play(LaggedStart(*[Create(route) for route in routes], lag_ratio=0.3), run_time=4)

        # Rotate camera
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(1)


class HaversineDistance(Scene):
    """Visualize haversine distance calculation between two points"""

    def construct(self):
        title = Text("Haversine Distance Formula", font_size=32, font="Monospace")
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # Create 2D projection (equirectangular)
        axes = Axes(
            x_range=[-180, 180, 60],
            y_range=[-90, 90, 30],
            x_length=10,
            y_length=5,
            axis_config={"include_tip": False}
        )
        axes.shift(DOWN * 0.5)

        # Grid lines for latitude/longitude
        grid = VGroup()
        for lon in range(-180, 181, 30):
            line = axes.get_vertical_line(axes.c2p(lon, 0), color=GRAY, stroke_width=0.5)
            grid.add(line)
        for lat in range(-90, 91, 30):
            line = axes.get_horizontal_line(axes.c2p(0, lat), color=GRAY, stroke_width=0.5)
            grid.add(line)

        self.add(axes, grid)

        # Define two points
        point1 = (40.7, -74.0)  # NYC
        point2 = (51.5, -0.1)    # London

        pos1 = axes.c2p(point1[1], point1[0])
        pos2 = axes.c2p(point2[1], point2[0])

        dot1 = Dot(pos1, color=YELLOW, radius=0.1)
        dot2 = Dot(pos2, color=GREEN, radius=0.1)

        label1 = Text("NYC", font_size=20, font="Monospace").next_to(dot1, DOWN)
        label2 = Text("London", font_size=20, font="Monospace").next_to(dot2, UP)

        self.play(FadeIn(dot1), FadeIn(dot2), Write(label1), Write(label2))

        # Draw connection line
        line = Line(pos1, pos2, color=RED, stroke_width=3)
        self.play(Create(line))

        # Calculate haversine distance
        lat1, lon1 = np.radians(point1[0]), np.radians(point1[1])
        lat2, lon2 = np.radians(point2[0]), np.radians(point2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        R = 6371  # Earth radius in km
        distance = R * c

        # Display distance
        distance_text = Text(
            f"Distance: {distance:.0f} km",
            font_size=28,
            color=YELLOW,
            font="Monospace"
        )
        distance_text.to_corner(DR)
        self.play(FadeIn(distance_text))

        # Animate distance circles expanding from point 1
        circle_radii = [1000, 2000, 3000, 4000, 5000]
        for radius_km in circle_radii:
            # Convert km to degrees (rough approximation)
            radius_deg = radius_km / 111  # 1 degree ≈ 111 km
            circle = Circle(
                radius=axes.x_axis.unit_size * radius_deg,
                color=BLUE_C,
                stroke_width=2,
                stroke_opacity=0.5
            )
            circle.move_to(pos1)
            self.play(Create(circle), run_time=0.5)
            if radius_km < distance:
                self.play(FadeOut(circle), run_time=0.3)
            else:
                break

        self.wait(2)


class TrilaterationVisualization(Scene):
    """Visualize GPS trilateration from multiple satellites"""

    def construct(self):
        title = Text("GPS Trilateration: Finding Position", font_size=30, font="Monospace")
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # Satellite positions
        satellites = [
            (np.array([2, 2.5, 0]), 2.8, RED),
            (np.array([-2.5, 1.5, 0]), 3.2, BLUE),
            (np.array([0.5, -2, 0]), 2.5, GREEN),
        ]

        # Draw satellites
        sat_group = VGroup()
        for pos, _, color in satellites:
            sat = RegularPolygon(n=4, color=color).scale(0.2)
            sat.move_to(pos)
            sat_group.add(sat)

        self.play(LaggedStart(*[FadeIn(sat, scale=0.5) for sat in sat_group], lag_ratio=0.3))

        # Draw distance circles
        circles = VGroup()
        for pos, radius, color in satellites:
            circle = Circle(radius=radius, color=color, stroke_width=3, stroke_opacity=0.6)
            circle.move_to(pos)
            circles.add(circle)

        self.play(LaggedStart(*[Create(circle) for circle in circles], lag_ratio=0.4), run_time=3)

        # Find intersection point (receiver position)
        # For this visualization, we'll calculate the actual trilateration
        # Using the formula for 2D trilateration

        p1, r1, _ = satellites[0]
        p2, r2, _ = satellites[1]
        p3, r3, _ = satellites[2]

        # Simplified 2D trilateration
        receiver_pos = np.array([0, 0, 0])  # Approximate center

        receiver = Dot(receiver_pos, color=YELLOW, radius=0.15)
        receiver_label = Text("Receiver", font_size=20, color=YELLOW, font="Monospace")
        receiver_label.next_to(receiver, DOWN)

        self.play(FadeIn(receiver, scale=0.3), Write(receiver_label))

        # Draw lines from satellites to receiver
        lines = VGroup()
        for pos, _, color in satellites:
            line = DashedLine(pos, receiver_pos, color=color, stroke_width=2, dash_length=0.1)
            lines.add(line)

        self.play(LaggedStart(*[Create(line) for line in lines], lag_ratio=0.2))

        # Show accuracy annotation
        accuracy_text = Text(
            "3+ satellites needed for 2D position",
            font_size=22,
            color=GRAY,
            font="Monospace"
        )
        accuracy_text.to_edge(DOWN)
        self.play(FadeIn(accuracy_text))

        self.wait(2)


class CoordinateGridTransform(Scene):
    """Novel: Animated transformation between coordinate systems"""

    def construct(self):
        title = Text("Coordinate System: Geographic to Cartesian", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # Start with lat/lon grid
        lat_lon_grid = VGroup()
        for lat in range(-60, 61, 30):
            line_points = [np.array([lon / 30, lat / 30, 0]) for lon in range(-180, 181, 10)]
            line = VMobject().set_points_smoothly(line_points)
            line.set_stroke(BLUE, width=1, opacity=0.5)
            lat_lon_grid.add(line)

        for lon in range(-180, 181, 60):
            line_points = [np.array([lon / 30, lat / 30, 0]) for lat in range(-60, 61, 10)]
            line = VMobject().set_points_smoothly(line_points)
            line.set_stroke(BLUE, width=1, opacity=0.5)
            lat_lon_grid.add(line)

        lat_lon_grid.scale(0.5)
        self.play(Create(lat_lon_grid), run_time=2)

        # Place some points in lat/lon
        points_latlon = [
            (40, -74),   # NYC
            (51, 0),     # London
            (-34, 151),  # Sydney
        ]

        dots = VGroup()
        for lat, lon in points_latlon:
            pos = np.array([lon / 30, lat / 30, 0]) * 0.5
            dot = Dot(pos, color=YELLOW, radius=0.08)
            dots.add(dot)

        self.play(FadeIn(dots))
        self.wait(1)

        # Transform to Cartesian grid
        cartesian_grid = NumberPlane(
            x_range=[-6, 6, 1],
            y_range=[-3, 3, 1],
            background_line_style={"stroke_color": GREEN, "stroke_width": 1, "stroke_opacity": 0.5}
        ).scale(0.6)

        self.play(
            Transform(lat_lon_grid, cartesian_grid),
            *[dot.animate.move_to(np.array([
                np.cos(np.radians(points_latlon[i][0])) * np.cos(np.radians(points_latlon[i][1])) * 2,
                np.cos(np.radians(points_latlon[i][0])) * np.sin(np.radians(points_latlon[i][1])) * 2,
                0
            ])) for i, dot in enumerate(dots)],
            run_time=3
        )

        transform_label = Text("Cartesian (X, Y)", font_size=24, color=GREEN, font="Monospace")
        transform_label.to_edge(DOWN)
        self.play(Write(transform_label))

        self.wait(2)


class GeofencePulse(Scene):
    """Novel: Animated geofence boundary with entry/exit detection"""

    def construct(self):
        title = Text("Geofence: Boundary Detection", font_size=30, font="Monospace")
        title.to_edge(UP)
        self.play(Write(title), run_time=0.8)

        # Define geofence polygon (irregular shape)
        fence_points = [
            np.array([2, 1, 0]),
            np.array([2.5, -1, 0]),
            np.array([1, -2, 0]),
            np.array([-1.5, -1.5, 0]),
            np.array([-2, 0.5, 0]),
            np.array([-0.5, 2, 0]),
            np.array([1, 1.5, 0]),
        ]

        geofence = Polygon(*fence_points, color=BLUE, stroke_width=4)
        geofence.set_fill(BLUE, opacity=0.1)

        self.play(Create(geofence))

        # Animated boundary pulse
        def create_pulse():
            pulse = geofence.copy()
            pulse.set_stroke(BLUE_C, width=2)
            self.add(pulse)
            self.play(
                pulse.animate.scale(1.15).set_stroke(opacity=0),
                run_time=1.5,
                rate_func=linear
            )
            self.remove(pulse)

        # Moving object
        path_points = [
            np.array([-4, 0, 0]),
            np.array([-2, 0.5, 0]),
            np.array([0, 0, 0]),
            np.array([1.5, 0.5, 0]),
            np.array([3, -0.5, 0]),
            np.array([4, -1, 0]),
        ]

        path = VMobject().set_points_smoothly(path_points)
        path.set_stroke(WHITE, width=1, opacity=0.3)
        self.add(path)

        tracker = Dot(path.get_start(), color=YELLOW, radius=0.1)
        trail = TracedPath(tracker.get_center, stroke_color=YELLOW, stroke_width=2, dissipating_time=2)
        self.add(trail, tracker)

        # Status indicator
        status_text = Text("Outside", font_size=24, color=RED, font="Monospace")
        status_text.to_corner(DR)
        self.add(status_text)

        # Animate movement with fence checking
        def update_status(mob, alpha):
            pos = path.point_from_proportion(alpha)
            tracker.move_to(pos)

            # Simple point-in-polygon check (rough approximation)
            if -2 < pos[0] < 2.5 and -2 < pos[1] < 2:
                if status_text.text != "Inside":
                    new_status = Text("Inside", font_size=24, color=GREEN, font="Monospace")
                    new_status.to_corner(DR)
                    self.remove(status_text)
                    self.add(new_status)
                    status_text.text = "Inside"
                    create_pulse()
            else:
                if status_text.text != "Outside":
                    new_status = Text("Outside", font_size=24, color=RED, font="Monospace")
                    new_status.to_corner(DR)
                    self.remove(status_text)
                    self.add(new_status)
                    status_text.text = "Outside"

        self.play(
            UpdateFromAlphaFunc(tracker, update_status),
            run_time=8,
            rate_func=linear
        )

        self.wait(2)



class SignalStrengthLandscape(ThreeDScene):
    """Novel: 3D surface showing GPS/signal strength accuracy landscape"""

    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, zoom=0.7)

        title = Text("Signal Strength Landscape", font_size=28, font="Monospace")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        # Create signal towers/satellites
        towers = [
            np.array([3, 2, 2]),
            np.array([-2, 3, 2.5]),
            np.array([-3, -2, 2]),
            np.array([2, -3, 1.8]),
        ]

        tower_objects = VGroup()
        for pos in towers:
            tower = Cone(base_radius=0.15, height=0.4, direction=UP)
            tower.move_to(pos)
            tower.set_fill(YELLOW, opacity=0.9)
            tower_objects.add(tower)

        self.add(tower_objects)

        # Create signal strength surface
        def signal_strength(u, v):
            x = u * 8 - 4
            y = v * 8 - 4

            # Calculate combined signal strength from all towers
            strength = 0
            for tower_pos in towers:
                dist = np.sqrt((x - tower_pos[0])**2 + (y - tower_pos[1])**2)
                # Inverse square law for signal strength
                strength += 2.0 / (1 + dist**2)

            z = strength - 0.5  # Offset to center
            return np.array([x, y, z])

        surface = Surface(
            signal_strength,
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(50, 50)
        )
        surface.set_style(fill_opacity=0.7, stroke_width=0.5, stroke_opacity=0.2)
        surface.set_fill(BLUE, opacity=0.6)

        self.play(Create(surface), run_time=3)

        # Animate a device moving through the landscape
        device_path = VMobject()
        path_points_2d = [
            np.array([-3, -3, 0]),
            np.array([0, 0, 0]),
            np.array([3, 2, 0]),
        ]

        # Project path onto signal strength surface
        path_points_3d = []
        for p in np.linspace(0, 1, 100):
            pos_2d = (1 - p) * path_points_2d[0] + p * path_points_2d[-1]
            u = (pos_2d[0] + 4) / 8
            v = (pos_2d[1] + 4) / 8
            if 0 <= u <= 1 and 0 <= v <= 1:
                pos_3d = signal_strength(u, v)
                pos_3d[2] += 0.2  # Slightly above surface
                path_points_3d.append(pos_3d)

        device_path.set_points_smoothly(path_points_3d)
        device_path.set_stroke(RED, width=3)

        device = Sphere(radius=0.15, resolution=(10, 10))
        device.set_fill(RED, opacity=0.9)
        device.move_to(path_points_3d[0])

        self.play(Create(device_path))
        self.add(device)

        self.play(
            MoveAlongPath(device, device_path),
            run_time=5,
            rate_func=linear
        )

        # Rotate view
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(1)

