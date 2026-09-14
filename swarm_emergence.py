from manim import *
import numpy as np


class BoidsFlocking(Scene):
    """Classic Boids algorithm: separation, alignment, cohesion"""

    def construct(self):
        title = Text("Boids: Flocking Birds", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Create boids
        n_boids = 25
        boids = VGroup()

        for _ in range(n_boids):
            pos = np.array([
                np.random.uniform(-5, 5),
                np.random.uniform(-2.5, 2.5),
                0
            ])
            vel = np.array([
                np.random.uniform(-1, 1),
                np.random.uniform(-1, 1),
                0
            ])

            boid = Triangle().scale(0.12).set_fill(BLUE, opacity=0.9).set_stroke(WHITE, width=1)
            boid.rotate(PI/2)
            boid.move_to(pos)
            boid.velocity = vel
            boid.last_angle = PI/2
            boids.add(boid)

        self.add(boids)

        # Simulation parameters
        separation_dist = 0.7
        alignment_dist = 2.0
        cohesion_dist = 2.5
        max_speed = 1.5
        max_force = 0.3

        def limit_vector(vec, max_val):
            mag = np.linalg.norm(vec[:2])
            if mag > max_val and mag > 0:
                return (vec / mag) * max_val
            return vec

        def update_boids(dt):
            for i, boid in enumerate(boids):
                separation = np.array([0., 0., 0.])
                alignment = np.array([0., 0., 0.])
                cohesion = np.array([0., 0., 0.])

                sep_count = 0
                align_count = 0
                coh_count = 0

                for j, other in enumerate(boids):
                    if i == j:
                        continue

                    diff = boid.get_center() - other.get_center()
                    dist = np.linalg.norm(diff[:2])

                    if dist < separation_dist and dist > 0.01:
                        separation += diff / dist
                        sep_count += 1

                    if dist < alignment_dist:
                        alignment += other.velocity
                        align_count += 1

                    if dist < cohesion_dist:
                        cohesion += other.get_center()
                        coh_count += 1

                # Calculate steering forces
                if sep_count > 0:
                    separation /= sep_count
                    separation = limit_vector(separation, max_force) * 2.0

                if align_count > 0:
                    alignment /= align_count
                    alignment = limit_vector(alignment - boid.velocity, max_force) * 1.0

                if coh_count > 0:
                    cohesion /= coh_count
                    cohesion = cohesion - boid.get_center()
                    cohesion = limit_vector(cohesion, max_force) * 0.8

                # Apply forces
                acceleration = separation + alignment + cohesion
                boid.velocity += acceleration * 0.5
                boid.velocity = limit_vector(boid.velocity, max_speed)

                # Update position
                new_pos = boid.get_center() + boid.velocity * 0.05

                # Wrap around edges
                if new_pos[0] > 6:
                    new_pos[0] = -6
                elif new_pos[0] < -6:
                    new_pos[0] = 6
                if new_pos[1] > 3:
                    new_pos[1] = -3
                elif new_pos[1] < -3:
                    new_pos[1] = 3

                boid.move_to(new_pos)

                # Point in direction of movement
                if np.linalg.norm(boid.velocity[:2]) > 0.1:
                    target_angle = np.arctan2(boid.velocity[1], boid.velocity[0]) + PI/2
                    angle_diff = target_angle - boid.last_angle
                    boid.rotate(angle_diff)
                    boid.last_angle = target_angle

        # Run simulation manually with many small time steps
        for frame in range(300):  # 300 frames at 15fps = 20 seconds
            update_boids(1/15)
            self.wait(1/15)

        # Add description
        desc = Text(
            "Each bird follows 3 rules: stay apart from neighbors,\n"
            "fly in the same direction as neighbors,\n"
            "and move toward the group center",
            font_size=18,
            font="Monospace",
            color=GRAY
        ).to_edge(DOWN)
        self.play(FadeIn(desc))
        self.wait(2)


class AntColonyPheromone(Scene):
    """Ant colony with pheromone trail emergence"""

    def construct(self):
        title = Text("Ant Colony: Finding Food", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Nest and food locations
        nest = Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).shift(LEFT * 4 + DOWN * 0.5)
        food = Circle(radius=0.3, color=GREEN, fill_opacity=0.8).shift(RIGHT * 4 + UP * 0.5)
        nest_label = Text("Nest", font_size=16, font="Monospace").next_to(nest, DOWN, buff=0.1)
        food_label = Text("Food", font_size=16, font="Monospace").next_to(food, UP, buff=0.1)
        self.add(nest, food, nest_label, food_label)

        # Pheromone grid
        grid_size = 20
        pheromone = np.zeros((grid_size, grid_size))
        pheromone_cells = []

        for i in range(grid_size):
            for j in range(grid_size):
                x = (i - grid_size/2) * 0.5
                y = (j - grid_size/2) * 0.35
                cell = Square(side_length=0.45, stroke_width=0)
                cell.move_to(np.array([x, y, 0]))
                cell.set_fill(YELLOW, opacity=0)
                cell.grid_i = i
                cell.grid_j = j
                pheromone_cells.append(cell)
                self.add(cell)

        # Ants
        n_ants = 12
        ants = []
        for _ in range(n_ants):
            ant = Dot(nest.get_center(), radius=0.08, color=RED)
            ant.has_food = False
            ant.direction = np.random.uniform(-PI, PI)
            ants.append(ant)
            self.add(ant)

        def update_ants():
            nonlocal pheromone

            # Evaporate pheromone
            pheromone *= 0.97

            for ant in ants:
                pos = ant.get_center()

                # Determine target
                if not ant.has_food:
                    target = food.get_center()
                else:
                    target = nest.get_center()

                # Move toward target with randomness
                to_target = target - pos
                if np.linalg.norm(to_target[:2]) > 0.1:
                    to_target = to_target / np.linalg.norm(to_target[:2])

                # Random walk component
                ant.direction += np.random.uniform(-0.4, 0.4)
                random_move = np.array([np.cos(ant.direction), np.sin(ant.direction), 0])

                # Blend toward target and random
                direction = 0.6 * to_target + 0.4 * random_move
                direction = direction / (np.linalg.norm(direction[:2]) + 0.001)

                new_pos = pos + direction * 0.15

                # Bounds
                new_pos[0] = np.clip(new_pos[0], -5.5, 5.5)
                new_pos[1] = np.clip(new_pos[1], -3, 3)

                ant.move_to(new_pos)

                # Check if reached food
                if not ant.has_food and np.linalg.norm(new_pos - food.get_center()) < 0.4:
                    ant.has_food = True
                    ant.set_color(ORANGE)

                # Check if returned to nest
                elif ant.has_food and np.linalg.norm(new_pos - nest.get_center()) < 0.4:
                    ant.has_food = False
                    ant.set_color(RED)

                # Deposit pheromone if carrying food
                if ant.has_food:
                    gi = int((new_pos[0] + 5) / 0.5)
                    gj = int((new_pos[1] + 3.5) / 0.35)
                    if 0 <= gi < grid_size and 0 <= gj < grid_size:
                        pheromone[gi, gj] = min(pheromone[gi, gj] + 0.5, 1.0)

            # Update pheromone visualization
            for cell in pheromone_cells:
                i, j = cell.grid_i, cell.grid_j
                opacity = pheromone[i, j]
                cell.set_fill(YELLOW, opacity=opacity * 0.7)

        # Run simulation
        for frame in range(400):  # 400 frames
            update_ants()
            self.wait(1/15)

        # Add description
        desc = Text(
            "Ants leave a chemical trail when carrying food.\n"
            "Other ants follow these trails, creating the\n"
            "shortest path between nest and food",
            font_size=18,
            font="Monospace",
            color=GRAY
        ).to_edge(DOWN)
        self.play(FadeIn(desc))
        self.wait(2)


class SelfOrganizingPattern(Scene):
    """Agents self-organize into hexagonal pattern"""

    def construct(self):
        title = Text("Self-Organization: Hexagon Grid", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Create agents
        n_agents = 35
        agents = []

        for _ in range(n_agents):
            pos = np.array([
                np.random.uniform(-4, 4),
                np.random.uniform(-2, 2),
                0
            ])
            agent = Dot(pos, radius=0.1, color=BLUE)
            agent.velocity = np.array([0., 0., 0.])
            agents.append(agent)
            self.add(agent)

        # Target spacing
        target_spacing = 0.9

        def update_pattern():
            for i, agent in enumerate(agents):
                force = np.array([0., 0., 0.])

                for j, other in enumerate(agents):
                    if i == j:
                        continue

                    diff = agent.get_center() - other.get_center()
                    dist = np.linalg.norm(diff[:2])

                    if dist < 0.01:
                        diff = np.random.rand(3) * 0.1
                        dist = np.linalg.norm(diff[:2])

                    # Spring-like force
                    if dist < target_spacing * 1.8:
                        if dist < target_spacing * 0.8:
                            # Strong repulsion when too close
                            force += (diff / dist) * 0.2 * (target_spacing / (dist + 0.1))
                        elif dist > target_spacing * 1.2:
                            # Gentle attraction when too far
                            force -= (diff / dist) * 0.1

                # Apply force with damping
                agent.velocity += force * 0.3
                agent.velocity *= 0.8  # Strong damping

                # Limit velocity
                speed = np.linalg.norm(agent.velocity[:2])
                if speed > 0.5:
                    agent.velocity = (agent.velocity / speed) * 0.5

                # Update position
                new_pos = agent.get_center() + agent.velocity * 0.1

                # Soft boundaries
                if abs(new_pos[0]) > 4.5:
                    agent.velocity[0] *= -0.7
                    new_pos[0] = np.clip(new_pos[0], -4.5, 4.5)
                if abs(new_pos[1]) > 2.5:
                    agent.velocity[1] *= -0.7
                    new_pos[1] = np.clip(new_pos[1], -2.5, 2.5)

                agent.move_to(new_pos)

                # Color by neighbors
                neighbors = sum(1 for o in agents if i != agents.index(o) and
                              0.7 < np.linalg.norm(agent.get_center() - o.get_center()) < 1.1)

                if neighbors == 6:
                    agent.set_color(GREEN)
                elif neighbors > 6:
                    agent.set_color(RED)
                elif neighbors < 4:
                    agent.set_color(BLUE)
                else:
                    agent.set_color(YELLOW)

        # Run simulation
        for frame in range(400):
            update_pattern()
            self.wait(1/15)

        # Add description
        desc = Text(
            "Dots push apart when too close and pull together\n"
            "when too far. They settle into a honeycomb pattern\n"
            "where each dot has exactly 6 neighbors (green)",
            font_size=18,
            font="Monospace",
            color=GRAY
        ).to_edge(DOWN)
        self.play(FadeIn(desc))
        self.wait(2)


class ConsensusEmergence(Scene):
    """Swarm consensus decision-making"""

    def construct(self):
        title = Text("Consensus: Group Decision", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Two options
        option_a = Square(side_length=0.6, color=RED, fill_opacity=0.4).shift(LEFT * 4)
        option_b = Square(side_length=0.6, color=BLUE, fill_opacity=0.4).shift(RIGHT * 4)
        label_a = Text("Option A", font_size=18, font="Monospace").next_to(option_a, UP)
        label_b = Text("Option B", font_size=18, font="Monospace").next_to(option_b, UP)
        self.add(option_a, option_b, label_a, label_b)

        # Agents
        n_agents = 40
        agents = []

        for i in range(n_agents):
            pos = np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0])
            agent = Dot(pos, radius=0.08)

            # Random initial preference
            if np.random.random() < 0.5:
                agent.preference = 0
                agent.set_color(RED)
            else:
                agent.preference = 1
                agent.set_color(BLUE)

            agent.certainty = np.random.uniform(0.3, 0.8)
            agents.append(agent)
            self.add(agent)

        # Counter
        counter_text = Text("Red: 20  Blue: 20", font_size=20, font="Monospace")
        counter_text.to_corner(DR)
        self.add(counter_text)

        def update_consensus():
            # Agents influence neighbors
            for agent in agents:
                neighbors = [a for a in agents if a != agent and
                           np.linalg.norm(a.get_center() - agent.get_center()) < 1.2]

                if neighbors:
                    neighbor_prefs = [n.preference for n in neighbors]
                    pct_same = sum(1 for p in neighbor_prefs if p == agent.preference) / len(neighbor_prefs)

                    # Switch if outnumbered
                    if pct_same < 0.4 and np.random.random() > agent.certainty:
                        agent.preference = 1 - agent.preference
                        agent.set_color(RED if agent.preference == 0 else BLUE)
                        agent.certainty = min(agent.certainty + 0.1, 0.95)

                # Move toward preference
                target = option_a.get_center() if agent.preference == 0 else option_b.get_center()
                direction = target - agent.get_center()
                dist = np.linalg.norm(direction[:2])

                if dist > 0.3:
                    direction = direction / dist
                    new_pos = agent.get_center() + direction * 0.08
                    agent.move_to(new_pos)

            # Update counter
            red_count = sum(1 for a in agents if a.preference == 0)
            blue_count = n_agents - red_count
            new_text = Text(f"Red: {red_count}  Blue: {blue_count}",
                          font_size=20, font="Monospace")
            new_text.to_corner(DR)
            counter_text.become(new_text)

        # Run simulation
        for frame in range(360):
            update_consensus()
            self.wait(1/15)

        # Add description
        desc = Text(
            "Agents start with random preferences. They switch\n"
            "to match their neighbors if outnumbered. Eventually\n"
            "the group reaches agreement on one option",
            font_size=18,
            font="Monospace",
            color=GRAY
        ).to_edge(DOWN)
        self.play(FadeIn(desc))
        self.wait(2)


class ComplexityMetricOverlay(Scene):
    """Real-time complexity/entropy measurement"""

    def construct(self):
        title = Text("Emergence: Order From Chaos", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Particles
        n_particles = 50
        particles = []

        for _ in range(n_particles):
            pos = np.array([np.random.uniform(-5, 5), np.random.uniform(-2.5, 2.5), 0])
            particle = Dot(pos, radius=0.06, color=WHITE)
            particle.velocity = np.random.uniform(-2, 2, 3)
            particle.velocity[2] = 0
            particles.append(particle)
            self.add(particle)

        # Order meter
        meter_bg = Rectangle(width=0.4, height=2.5, color=GRAY, fill_opacity=0.3)
        meter_bg.to_corner(UR).shift(DOWN * 0.8)
        meter_fill = Rectangle(width=0.4, height=0.1, color=RED, fill_opacity=0.9)
        meter_fill.align_to(meter_bg, DOWN).align_to(meter_bg, RIGHT)

        meter_label_chaos = Text("Chaos", font_size=14, color=RED, font="Monospace")
        meter_label_chaos.next_to(meter_bg, DOWN, buff=0.1)
        meter_label_order = Text("Order", font_size=14, color=GREEN, font="Monospace")
        meter_label_order.next_to(meter_bg, UP, buff=0.1)

        self.add(meter_bg, meter_fill, meter_label_chaos, meter_label_order)

        # Attractor
        attractor = None
        attractor_ring = None

        def calculate_order():
            positions = np.array([p.get_center()[:2] for p in particles])
            center = np.mean(positions, axis=0)
            distances = [np.linalg.norm(p - center) for p in positions]
            avg_dist = np.mean(distances)
            order = 1 - min(avg_dist / 5.0, 1.0)
            return order

        def update_particles(frame):
            nonlocal attractor, attractor_ring

            # Create attractor after 40 frames
            if frame == 40 and attractor is None:
                attractor = Dot(ORIGIN, radius=0.25, color=YELLOW, fill_opacity=0.6)
                attractor_ring = Circle(radius=0.35, color=YELLOW, stroke_width=2)
                self.add(attractor_ring, attractor)

            for particle in particles:
                # Random motion
                particle.velocity += np.random.normal(0, 0.5, 3)
                particle.velocity[2] = 0

                # Attraction to center
                if attractor is not None:
                    diff = attractor.get_center() - particle.get_center()
                    dist = np.linalg.norm(diff[:2])
                    if dist > 0.1:
                        attraction = (diff / dist) * 0.4
                        particle.velocity += attraction

                # Damping
                particle.velocity *= 0.9

                # Update position
                new_pos = particle.get_center() + particle.velocity * 0.05

                # Boundaries
                if abs(new_pos[0]) > 5.5:
                    particle.velocity[0] *= -0.7
                    new_pos[0] = np.clip(new_pos[0], -5.5, 5.5)
                if abs(new_pos[1]) > 2.8:
                    particle.velocity[1] *= -0.7
                    new_pos[1] = np.clip(new_pos[1], -2.8, 2.8)

                particle.move_to(new_pos)

            # Update meter
            order = calculate_order()
            new_height = max(order * 2.5, 0.1)
            new_fill = Rectangle(width=0.4, height=new_height, fill_opacity=0.9)
            new_fill.align_to(meter_bg, DOWN).align_to(meter_bg, RIGHT)

            if order > 0.7:
                new_fill.set_fill(GREEN)
            elif order > 0.4:
                new_fill.set_fill(YELLOW)
            else:
                new_fill.set_fill(RED)

            meter_fill.become(new_fill)

        # Run simulation
        for frame in range(280):
            update_particles(frame)
            self.wait(1/15)

        # Add description
        desc = Text(
            "Random dots start scattered (chaos). A yellow\n"
            "attractor appears and pulls them together. The\n"
            "meter shows increasing order as they cluster",
            font_size=18,
            font="Monospace",
            color=GRAY
        ).to_edge(DOWN)
        self.play(FadeIn(desc))
        self.wait(2)
