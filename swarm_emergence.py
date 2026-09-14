from manim import *
import numpy as np


class BoidsFlocking(Scene):
    """Classic Boids algorithm: separation, alignment, cohesion"""

    def construct(self):
        title = Text("Boids: Emergent Flocking from Simple Rules", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Create boids
        n_boids = 30
        boids = []

        for _ in range(n_boids):
            pos = np.array([
                np.random.uniform(-5, 5),
                np.random.uniform(-2.5, 2.5),
                0
            ])
            vel = np.array([
                np.random.uniform(-0.5, 0.5),
                np.random.uniform(-0.5, 0.5),
                0
            ])

            boid = Triangle().scale(0.1).set_fill(BLUE, opacity=0.8)
            boid.move_to(pos)
            boid.velocity = vel
            boid.current_angle = 0  # Track rotation angle
            boids.append(boid)
            self.add(boid)

        # Trail tracking
        trails = [TracedPath(boid.get_center, stroke_color=BLUE, stroke_width=1,
                           dissipating_time=1.5, stroke_opacity=0.3) for boid in boids]
        for trail in trails:
            self.add(trail)

        # Simulation parameters
        separation_dist = 0.5
        alignment_dist = 1.5
        cohesion_dist = 2.0
        max_speed = 0.3
        max_force = 0.05

        def limit_vector(vec, max_val):
            mag = np.linalg.norm(vec)
            if mag > max_val:
                return (vec / mag) * max_val
            return vec

        def update_boids(mob, dt):
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
                    dist = np.linalg.norm(diff)

                    # Separation: avoid crowding
                    if dist < separation_dist and dist > 0:
                        separation += diff / dist
                        sep_count += 1

                    # Alignment: steer towards average heading
                    if dist < alignment_dist:
                        alignment += other.velocity
                        align_count += 1

                    # Cohesion: steer towards average position
                    if dist < cohesion_dist:
                        cohesion += other.get_center()
                        coh_count += 1

                # Average and apply weights
                if sep_count > 0:
                    separation /= sep_count
                    separation = limit_vector(separation, max_force) * 1.5

                if align_count > 0:
                    alignment /= align_count
                    alignment = limit_vector(alignment - boid.velocity, max_force)

                if coh_count > 0:
                    cohesion /= coh_count
                    cohesion = cohesion - boid.get_center()
                    cohesion = limit_vector(cohesion, max_force) * 0.5

                # Apply steering forces
                acceleration = separation + alignment + cohesion
                boid.velocity += acceleration
                boid.velocity = limit_vector(boid.velocity, max_speed)

                # Update position
                new_pos = boid.get_center() + boid.velocity

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

                # Rotate to face direction
                if np.linalg.norm(boid.velocity[:2]) > 0.01:
                    angle = np.arctan2(boid.velocity[1], boid.velocity[0])
                    boid.rotate(angle - boid.current_angle)
                    boid.current_angle = angle

        dummy = Dot(ORIGIN, radius=0)
        dummy.add_updater(update_boids)
        self.add(dummy)

        self.wait(15)
        dummy.remove_updater(update_boids)


class AntColonyPheromone(Scene):
    """Ant colony with pheromone trail emergence"""

    def construct(self):
        title = Text("Ant Colony: Pheromone Trail Emergence", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Nest and food locations
        nest = Circle(radius=0.3, color=ORANGE, fill_opacity=0.8).shift(LEFT * 4)
        food = Circle(radius=0.3, color=GREEN, fill_opacity=0.8).shift(RIGHT * 4)
        self.add(nest, food)

        # Pheromone grid
        grid_size = 20
        pheromone = np.zeros((grid_size, grid_size))
        pheromone_viz = VGroup()

        for i in range(grid_size):
            for j in range(grid_size):
                x = (i - grid_size/2) * 0.5
                y = (j - grid_size/2) * 0.3
                cell = Square(side_length=0.45, stroke_width=0)
                cell.move_to(np.array([x, y, 0]))
                cell.set_fill(YELLOW, opacity=0)
                cell.grid_i = i
                cell.grid_j = j
                pheromone_viz.add(cell)

        self.add(pheromone_viz)

        # Ants
        n_ants = 15
        ants = []
        for _ in range(n_ants):
            ant = Dot(nest.get_center(), radius=0.06, color=RED)
            ant.has_food = False
            ant.target = food.get_center()
            ants.append(ant)
            self.add(ant)

        def update_ants(mob, dt):
            nonlocal pheromone

            # Evaporate pheromone
            pheromone *= 0.995

            for ant in ants:
                pos = ant.get_center()

                # Random walk with pheromone bias
                if not ant.has_food:
                    direction = ant.target - pos
                else:
                    direction = nest.get_center() - pos

                direction += np.random.normal(0, 0.5, 3)
                direction[2] = 0

                if np.linalg.norm(direction) > 0:
                    direction = direction / np.linalg.norm(direction) * 0.05

                new_pos = pos + direction

                # Bounds
                new_pos[0] = np.clip(new_pos[0], -5, 5)
                new_pos[1] = np.clip(new_pos[1], -2.5, 2.5)

                ant.move_to(new_pos)

                # Check if reached food
                if not ant.has_food and np.linalg.norm(new_pos - food.get_center()) < 0.4:
                    ant.has_food = True
                    ant.set_color(ORANGE)
                    ant.target = nest.get_center()
                    # Deposit pheromone
                    gi = int((new_pos[0] + 5) / 0.5)
                    gj = int((new_pos[1] + 2.5) / 0.3)
                    if 0 <= gi < grid_size and 0 <= gj < grid_size:
                        pheromone[gi, gj] = min(pheromone[gi, gj] + 0.8, 1.0)

                # Check if returned to nest
                elif ant.has_food and np.linalg.norm(new_pos - nest.get_center()) < 0.4:
                    ant.has_food = False
                    ant.set_color(RED)
                    ant.target = food.get_center()

                # Deposit pheromone if carrying food
                if ant.has_food:
                    gi = int((new_pos[0] + 5) / 0.5)
                    gj = int((new_pos[1] + 2.5) / 0.3)
                    if 0 <= gi < grid_size and 0 <= gj < grid_size:
                        pheromone[gi, gj] = min(pheromone[gi, gj] + 0.3, 1.0)

            # Update pheromone visualization
            for cell in pheromone_viz:
                i, j = cell.grid_i, cell.grid_j
                opacity = pheromone[i, j]
                cell.set_fill(YELLOW, opacity=opacity * 0.6)

        dummy = Dot(ORIGIN, radius=0)
        dummy.add_updater(update_ants)
        self.add(dummy)

        self.wait(20)
        dummy.remove_updater(update_ants)


class SelfOrganizingPattern(Scene):
    """Novel: Agents self-organize into hexagonal pattern"""

    def construct(self):
        title = Text("Self-Organizing Hexagonal Lattice", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Create agents with random positions
        n_agents = 40
        agents = []

        for _ in range(n_agents):
            pos = np.array([
                np.random.uniform(-4, 4),
                np.random.uniform(-2, 2),
                0
            ])
            agent = Dot(pos, radius=0.08, color=BLUE)
            agent.velocity = np.random.uniform(-0.2, 0.2, 3)
            agent.velocity[2] = 0
            agents.append(agent)
            self.add(agent)

        # Target hexagonal spacing
        target_spacing = 0.8

        def update_pattern(mob, dt):
            for i, agent in enumerate(agents):
                force = np.array([0., 0., 0.])

                for j, other in enumerate(agents):
                    if i == j:
                        continue

                    diff = agent.get_center() - other.get_center()
                    dist = np.linalg.norm(diff)

                    if dist < 0.01:
                        continue

                    # Spring-like force (Lennard-Jones potential)
                    if dist < target_spacing * 1.5:
                        # Repulsion at short range
                        if dist < target_spacing * 0.7:
                            force += (diff / dist) * 0.02
                        # Attraction at medium range
                        elif dist > target_spacing * 1.1:
                            force -= (diff / dist) * 0.01
                        # Optimal spacing - minimal force
                        else:
                            force += (diff / dist) * 0.001

                # Apply force with damping
                agent.velocity += force
                agent.velocity *= 0.95  # Damping

                # Limit velocity
                speed = np.linalg.norm(agent.velocity)
                if speed > 0.2:
                    agent.velocity = (agent.velocity / speed) * 0.2

                # Update position
                new_pos = agent.get_center() + agent.velocity

                # Soft boundaries
                if abs(new_pos[0]) > 4:
                    agent.velocity[0] *= -0.5
                if abs(new_pos[1]) > 2:
                    agent.velocity[1] *= -0.5

                new_pos[0] = np.clip(new_pos[0], -4.5, 4.5)
                new_pos[1] = np.clip(new_pos[1], -2.5, 2.5)

                agent.move_to(new_pos)

                # Color by local density
                neighbors = sum(1 for o in agents if i != agents.index(o) and
                              np.linalg.norm(agent.get_center() - o.get_center()) < target_spacing * 1.5)

                if neighbors == 6:
                    agent.set_color(GREEN)  # Optimal hexagonal
                elif neighbors > 6:
                    agent.set_color(RED)    # Too crowded
                else:
                    agent.set_color(BLUE)   # Too sparse

        dummy = Dot(ORIGIN, radius=0)
        dummy.add_updater(update_pattern)
        self.add(dummy)

        self.wait(18)
        dummy.remove_updater(update_pattern)


class ConsensusEmergence(Scene):
    """Novel: Swarm consensus decision-making"""

    def construct(self):
        title = Text("Consensus: Two Opinions Merge", font_size=28, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Two target locations
        target_a = Circle(radius=0.4, color=RED, fill_opacity=0.3).shift(LEFT * 3)
        target_b = Circle(radius=0.4, color=BLUE, fill_opacity=0.3).shift(RIGHT * 3)
        self.add(target_a, target_b)

        # Agents with initial opinions
        n_agents = 50
        agents = []

        for i in range(n_agents):
            pos = np.array([np.random.uniform(-1, 1), np.random.uniform(-1, 1), 0])
            agent = Dot(pos, radius=0.06)

            # Random initial opinion
            if i < n_agents // 2:
                agent.opinion = 0  # Team A
                agent.set_color(RED)
            else:
                agent.opinion = 1  # Team B
                agent.set_color(BLUE)

            agent.confidence = np.random.uniform(0.3, 1.0)
            agents.append(agent)
            self.add(agent)

        # Opinion counter
        counter_text = Text("Red: 25 | Blue: 25", font_size=20, color=WHITE, font="Monospace")
        counter_text.to_corner(DR)
        self.add(counter_text)

        def update_consensus(mob, dt):
            # Update opinions based on neighbors
            for agent in agents:
                # Find nearby agents
                neighbors = [a for a in agents if a != agent and
                           np.linalg.norm(a.get_center() - agent.get_center()) < 1.0]

                if neighbors:
                    # Count neighbor opinions
                    neighbor_opinions = [n.opinion for n in neighbors]
                    avg_opinion = np.mean(neighbor_opinions)

                    # Probabilistic opinion change based on confidence
                    if np.random.random() > agent.confidence:
                        if avg_opinion < 0.5 and agent.opinion == 1:
                            agent.opinion = 0
                            agent.set_color(RED)
                        elif avg_opinion > 0.5 and agent.opinion == 0:
                            agent.opinion = 1
                            agent.set_color(BLUE)

                # Move towards preferred target
                if agent.opinion == 0:
                    target = target_a.get_center()
                else:
                    target = target_b.get_center()

                direction = target - agent.get_center()
                if np.linalg.norm(direction) > 0.1:
                    direction = direction / np.linalg.norm(direction) * 0.03
                    new_pos = agent.get_center() + direction
                    agent.move_to(new_pos)

            # Update counter
            red_count = sum(1 for a in agents if a.opinion == 0)
            blue_count = n_agents - red_count
            new_text = Text(f"Red: {red_count} | Blue: {blue_count}",
                          font_size=20, color=WHITE, font="Monospace")
            new_text.to_corner(DR)
            self.remove(counter_text)
            self.add(new_text)
            counter_text.become(new_text)

        dummy = Dot(ORIGIN, radius=0)
        dummy.add_updater(update_consensus)
        self.add(dummy)

        self.wait(20)
        dummy.remove_updater(update_consensus)


class ComplexityMetricOverlay(Scene):
    """Novel: Real-time complexity/entropy measurement"""

    def construct(self):
        title = Text("Emergence: Order from Chaos (Entropy Measure)", font_size=26, font="Monospace")
        title.to_edge(UP)
        self.add(title)

        # Particles
        n_particles = 60
        particles = []

        for _ in range(n_particles):
            pos = np.array([np.random.uniform(-5, 5), np.random.uniform(-2, 2), 0])
            particle = Dot(pos, radius=0.05, color=WHITE)
            particle.velocity = np.random.uniform(-0.3, 0.3, 3)
            particle.velocity[2] = 0
            particles.append(particle)
            self.add(particle)

        # Entropy meter
        entropy_bar = Rectangle(width=0.3, height=2, color=GREEN, fill_opacity=0.8)
        entropy_bar.to_corner(UR).shift(DOWN * 0.5)
        entropy_label = Text("Order", font_size=16, color=WHITE, font="Monospace")
        entropy_label.next_to(entropy_bar, UP)
        self.add(entropy_bar, entropy_label)

        # Attractor (appears after some time)
        attractor = None
        time_elapsed = 0

        def calculate_entropy():
            # Calculate spatial distribution entropy
            positions = np.array([p.get_center()[:2] for p in particles])

            # Grid-based entropy
            grid_size = 10
            hist, _, _ = np.histogram2d(positions[:, 0], positions[:, 1],
                                       bins=grid_size, range=[[-5, 5], [-2, 2]])
            hist = hist.flatten()
            hist = hist / hist.sum()

            # Shannon entropy
            entropy = -np.sum(hist * np.log(hist + 1e-10))
            max_entropy = np.log(grid_size * grid_size)

            return entropy / max_entropy

        def update_particles(mob, dt):
            nonlocal attractor, time_elapsed
            time_elapsed += dt

            # Create attractor after 3 seconds
            if time_elapsed > 3 and attractor is None:
                attractor = Dot(ORIGIN, radius=0.2, color=YELLOW, fill_opacity=0.5)
                self.add(attractor)

            for particle in particles:
                # Random motion
                particle.velocity += np.random.normal(0, 0.01, 3)
                particle.velocity[2] = 0

                # Attraction to center (after attractor appears)
                if attractor is not None:
                    diff = attractor.get_center() - particle.get_center()
                    dist = np.linalg.norm(diff)
                    if dist > 0.1:
                        attraction = (diff / dist) * 0.02
                        particle.velocity += attraction

                # Damping
                particle.velocity *= 0.98

                # Update position
                new_pos = particle.get_center() + particle.velocity

                # Bounce off boundaries
                if abs(new_pos[0]) > 5:
                    particle.velocity[0] *= -0.8
                if abs(new_pos[1]) > 2:
                    particle.velocity[1] *= -0.8

                new_pos[0] = np.clip(new_pos[0], -5, 5)
                new_pos[1] = np.clip(new_pos[1], -2, 2)

                particle.move_to(new_pos)

            # Update entropy visualization
            entropy_normalized = calculate_entropy()
            order = 1 - entropy_normalized  # Order is inverse of entropy

            new_height = order * 2
            new_bar = Rectangle(width=0.3, height=new_height, color=GREEN, fill_opacity=0.8)
            new_bar.align_to(entropy_bar, DOWN).align_to(entropy_bar, RIGHT)

            # Color based on order
            if order > 0.7:
                new_bar.set_fill(GREEN)
            elif order > 0.4:
                new_bar.set_fill(YELLOW)
            else:
                new_bar.set_fill(RED)

            entropy_bar.become(new_bar)

        dummy = Dot(ORIGIN, radius=0)
        dummy.add_updater(update_particles)
        self.add(dummy)

        self.wait(16)
        dummy.remove_updater(update_particles)
