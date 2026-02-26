import copy
import math
import random
from typing import Callable, Dict, List, Sequence, Tuple

City = Tuple[float, float]
Route = List[City]
VehicleRoutes = List[List[int]]


default_problems = {
    5: [(733, 251), (706, 87), (546, 97), (562, 49), (576, 253)],
    10: [(470, 169), (602, 202), (754, 239), (476, 233), (468, 301), (522, 29), (597, 171), (487, 325), (746, 232), (558, 136)],
    12: [(728, 67), (560, 160), (602, 312), (712, 148), (535, 340), (720, 354), (568, 300), (629, 260), (539, 46), (634, 343), (491, 135), (768, 161)],
    15: [(512, 317), (741, 72), (552, 50), (772, 346), (637, 12), (589, 131), (732, 165), (605, 15), (730, 38), (576, 216), (589, 381), (711, 387), (563, 228), (494, 22), (787, 288)],
}


def generate_random_population(cities_location: List[City], population_size: int) -> List[Route]:
    return [random.sample(cities_location, len(cities_location)) for _ in range(population_size)]


def calculate_distance(point1: City, point2: City) -> float:
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_fitness(path: Route) -> float:
    distance = 0.0
    n = len(path)
    for i in range(n):
        distance += calculate_distance(path[i], path[(i + 1) % n])
    return distance


def order_crossover(parent1: Route, parent2: Route) -> Route:
    length = len(parent1)
    start_index = random.randint(0, length - 2)
    end_index = random.randint(start_index + 1, length - 1)

    child = [None] * length
    child[start_index : end_index + 1] = parent1[start_index : end_index + 1]

    p2_idx = 0
    for i in range(length):
        if child[i] is not None:
            continue
        while parent2[p2_idx] in child:
            p2_idx += 1
        child[i] = parent2[p2_idx]

    return child


def pmx_crossover(parent1: Route, parent2: Route) -> Route:
    length = len(parent1)
    start_index = random.randint(0, length - 2)
    end_index = random.randint(start_index + 1, length - 1)

    child = [None] * length
    child[start_index : end_index + 1] = parent1[start_index : end_index + 1]

    mapping = {parent2[i]: parent1[i] for i in range(start_index, end_index + 1)}

    for i in range(length):
        if start_index <= i <= end_index:
            continue
        candidate = parent2[i]
        while candidate in child:
            candidate = mapping.get(candidate, candidate)
            if candidate not in mapping:
                break
        if candidate in child:
            # fallback to the first unused city to guarantee feasibility
            unused = [city for city in parent2 if city not in child]
            candidate = unused[0]
        child[i] = candidate

    return child


def mutate(solution: Route, mutation_probability: float, mutation_intensity: int = 1) -> Route:
    mutated_solution = copy.deepcopy(solution)
    if len(mutated_solution) < 2:
        return mutated_solution

    for _ in range(max(1, mutation_intensity)):
        if random.random() >= mutation_probability:
            continue

        operation = random.choice(("swap", "inversion"))
        i, j = sorted(random.sample(range(len(mutated_solution)), 2))

        if operation == "swap":
            mutated_solution[i], mutated_solution[j] = mutated_solution[j], mutated_solution[i]
        else:
            mutated_solution[i : j + 1] = list(reversed(mutated_solution[i : j + 1]))

    return mutated_solution


def sort_population(population: List[Route], fitness: List[float]) -> Tuple[List[Route], List[float]]:
    combined_lists = list(zip(population, fitness))
    sorted_combined_lists = sorted(combined_lists, key=lambda x: x[1])
    sorted_population, sorted_fitness = zip(*sorted_combined_lists)
    return list(sorted_population), list(sorted_fitness)


def tournament_selection(population: List[Route], fitness: List[float], k: int = 5) -> Route:
    selected_indices = random.sample(range(len(population)), k=min(k, len(population)))
    best_index = min(selected_indices, key=lambda i: fitness[i])
    return population[best_index]


def roulette_selection(population: List[Route], fitness: List[float]) -> Route:
    inv = [1.0 / f if f > 0 else 1.0 for f in fitness]
    return random.choices(population, weights=inv, k=1)[0]


def nearest_neighbour_tour(cities: List[City]) -> Route:
    unvisited = cities[:]
    current = random.choice(unvisited)
    tour = [current]
    unvisited.remove(current)

    while unvisited:
        next_city = min(unvisited, key=lambda c: (c[0] - current[0]) ** 2 + (c[1] - current[1]) ** 2)
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return tour


def generate_nearest_neighbour_population(cities: List[City], size: int) -> List[Route]:
    return [nearest_neighbour_tour(cities[:]) for _ in range(size)]


def convex_hull(points: List[City]) -> List[City]:
    points = sorted(points)

    def cross(o: City, a: City, b: City):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: List[City] = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper: List[City] = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def convex_hull_tour(cities: List[City]) -> Route:
    hull = convex_hull(cities[:])
    remaining = [c for c in cities if c not in hull]
    tour = hull[:]

    while remaining:
        city = remaining.pop()
        best_pos = 0
        best_increase = float("inf")

        for i in range(len(tour)):
            a = tour[i]
            b = tour[(i + 1) % len(tour)]
            increase = calculate_distance(a, city) + calculate_distance(city, b) - calculate_distance(a, b)

            if increase < best_increase:
                best_increase = increase
                best_pos = i + 1

        tour.insert(best_pos, city)

    return tour


def generate_convex_hull_population(cities: List[City], size: int) -> List[Route]:
    return [convex_hull_tour(cities[:]) for _ in range(size)]


def evolve_population(
    population: List[Route],
    mutation_probability: float,
    mutation_intensity: int = 1,
    elitism_size: int = 1,
    selection_method: str = "tournament",
    crossover_method: str = "ox",
    tournament_size: int = 5,
) -> Tuple[List[Route], List[float], float, Route]:
    fitness = [calculate_fitness(individual) for individual in population]
    population, fitness = sort_population(population, fitness)

    selector: Callable[[List[Route], List[float]], Route]
    if selection_method == "roulette":
        selector = roulette_selection
    else:
        selector = lambda pop, fit: tournament_selection(pop, fit, k=tournament_size)

    if crossover_method == "pmx":
        crossover = pmx_crossover
    else:
        crossover = order_crossover

    new_population = population[:elitism_size]

    while len(new_population) < len(population):
        parent1 = selector(population, fitness)
        parent2 = selector(population, fitness)
        child = crossover(parent1, parent2)
        child = mutate(child, mutation_probability, mutation_intensity=mutation_intensity)
        new_population.append(child)

    best_fitness = fitness[0]
    best_route = population[0]
    return new_population, fitness, best_fitness, best_route


def run_ga_experiment(
    cities_locations: List[City],
    population_size: int = 100,
    n_generations: int = 200,
    mutation_probability: float = 0.3,
    mutation_intensity: int = 1,
    selection_method: str = "tournament",
    crossover_method: str = "ox",
    tournament_size: int = 5,
    elitism_size: int = 1,
) -> Dict[str, object]:
    population = generate_random_population(cities_locations, population_size)

    best_fitness_history: List[float] = []
    best_solution_history: List[Route] = []

    for _ in range(n_generations):
        population, _, best_fitness, best_solution = evolve_population(
            population=population,
            mutation_probability=mutation_probability,
            mutation_intensity=mutation_intensity,
            elitism_size=elitism_size,
            selection_method=selection_method,
            crossover_method=crossover_method,
            tournament_size=tournament_size,
        )
        best_fitness_history.append(best_fitness)
        best_solution_history.append(best_solution)

    return {
        "best_fitness": best_fitness_history[-1],
        "best_solution": best_solution_history[-1],
        "fitness_history": best_fitness_history,
        "config": {
            "population_size": population_size,
            "n_generations": n_generations,
            "mutation_probability": mutation_probability,
            "mutation_intensity": mutation_intensity,
            "selection_method": selection_method,
            "crossover_method": crossover_method,
            "tournament_size": tournament_size,
            "elitism_size": elitism_size,
        },
    }


def build_distance_matrix(cities: Sequence[City]) -> List[List[float]]:
    matrix: List[List[float]] = []
    for i in range(len(cities)):
        row = []
        for j in range(len(cities)):
            row.append(calculate_distance(cities[i], cities[j]))
        matrix.append(row)
    return matrix


def generate_random_vrp_population(
    n_customers: int,
    n_vehicles: int,
    population_size: int,
) -> List[VehicleRoutes]:
    population: List[VehicleRoutes] = []
    customers = list(range(1, n_customers + 1))

    for _ in range(population_size):
        shuffled = customers[:]
        random.shuffle(shuffled)
        routes = [[] for _ in range(n_vehicles)]
        for i, customer in enumerate(shuffled):
            routes[i % n_vehicles].append(customer)

        random.shuffle(routes)
        population.append(routes)

    return population


def calculate_vrp_fitness(
    routes: VehicleRoutes,
    distance_matrix: List[List[float]],
    demands: Sequence[float],
    priorities: Sequence[float],
    vehicle_capacities: Sequence[float],
    vehicle_max_distances: Sequence[float],
    depot_index: int = 0,
    capacity_penalty_weight: float = 1000.0,
    autonomy_penalty_weight: float = 1000.0,
    priority_penalty_weight: float = 2.0,
) -> float:
    total_distance = 0.0
    capacity_penalty = 0.0
    autonomy_penalty = 0.0
    priority_penalty = 0.0

    for vehicle_idx, route in enumerate(routes):
        current = depot_index
        route_distance = 0.0
        route_load = 0.0
        route_priority = 0.0

        for customer in route:
            route_distance += distance_matrix[current][customer]
            route_load += demands[customer]
            route_priority += priorities[customer]
            current = customer

        route_distance += distance_matrix[current][depot_index]
        total_distance += route_distance

        if route_load > vehicle_capacities[vehicle_idx]:
            capacity_penalty += route_load - vehicle_capacities[vehicle_idx]

        if route_distance > vehicle_max_distances[vehicle_idx]:
            autonomy_penalty += route_distance - vehicle_max_distances[vehicle_idx]

        # prioridade maior = rota deveria ser mais curta
        if route:
            avg_priority = route_priority / len(route)
            priority_penalty += avg_priority * route_distance

    return (
        total_distance
        + (capacity_penalty_weight * capacity_penalty)
        + (autonomy_penalty_weight * autonomy_penalty)
        + (priority_penalty_weight * priority_penalty / max(1, sum(len(r) for r in routes)))
    )


def crossover_vrp(parent1: VehicleRoutes, parent2: VehicleRoutes) -> VehicleRoutes:
    flat1 = [c for route in parent1 for c in route]
    flat2 = [c for route in parent2 for c in route]
    lengths = [len(route) for route in parent1]

    child_flat = order_crossover(flat1, flat2)
    child: VehicleRoutes = []
    start = 0
    for route_len in lengths:
        child.append(child_flat[start : start + route_len])
        start += route_len

    return child


def mutate_vrp(routes: VehicleRoutes, mutation_probability: float) -> VehicleRoutes:
    mutated = copy.deepcopy(routes)

    if random.random() >= mutation_probability:
        return mutated

    non_empty = [idx for idx, route in enumerate(mutated) if route]
    if not non_empty:
        return mutated

    # 50% troca entre veículos, 50% inversão dentro da rota
    if random.random() < 0.5 and len(non_empty) > 1:
        v1, v2 = random.sample(non_empty, 2)
        i = random.randrange(len(mutated[v1]))
        j = random.randrange(len(mutated[v2]))
        mutated[v1][i], mutated[v2][j] = mutated[v2][j], mutated[v1][i]
    else:
        v = random.choice(non_empty)
        if len(mutated[v]) >= 2:
            i, j = sorted(random.sample(range(len(mutated[v])), 2))
            mutated[v][i : j + 1] = list(reversed(mutated[v][i : j + 1]))

    return mutated


def run_vrp_ga_experiment(
    cities_locations: Sequence[City],
    demands: Sequence[float],
    priorities: Sequence[float],
    vehicle_capacities: Sequence[float],
    vehicle_max_distances: Sequence[float],
    population_size: int = 120,
    n_generations: int = 200,
    mutation_probability: float = 0.2,
    elitism_size: int = 2,
) -> Dict[str, object]:
    n_vehicles = len(vehicle_capacities)
    n_customers = len(cities_locations) - 1  # 0 é depósito

    distance_matrix = build_distance_matrix(cities_locations)
    population = generate_random_vrp_population(n_customers, n_vehicles, population_size)

    best_fitness_history: List[float] = []
    best_solution = population[0]
    best_fitness = float("inf")

    for _ in range(n_generations):
        scored = [
            (
                individual,
                calculate_vrp_fitness(
                    individual,
                    distance_matrix,
                    demands,
                    priorities,
                    vehicle_capacities,
                    vehicle_max_distances,
                ),
            )
            for individual in population
        ]
        scored.sort(key=lambda x: x[1])

        if scored[0][1] < best_fitness:
            best_solution, best_fitness = scored[0]

        best_fitness_history.append(scored[0][1])
        ordered_population = [item[0] for item in scored]
        ordered_fitness = [item[1] for item in scored]

        new_population: List[VehicleRoutes] = ordered_population[:elitism_size]

        while len(new_population) < population_size:
            p1 = tournament_selection(ordered_population, ordered_fitness, k=5)
            p2 = tournament_selection(ordered_population, ordered_fitness, k=5)
            child = crossover_vrp(p1, p2)
            child = mutate_vrp(child, mutation_probability)
            new_population.append(child)

        population = new_population

    return {
        "best_fitness": best_fitness,
        "best_solution": best_solution,
        "fitness_history": best_fitness_history,
        "config": {
            "population_size": population_size,
            "n_generations": n_generations,
            "mutation_probability": mutation_probability,
            "vehicle_capacities": list(vehicle_capacities),
            "vehicle_max_distances": list(vehicle_max_distances),
        },
    }


if __name__ == "__main__":
    N_CITIES = 10
    cities_locations = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(N_CITIES)]

    result = run_ga_experiment(
        cities_locations,
        population_size=100,
        n_generations=100,
        mutation_probability=0.3,
        mutation_intensity=2,
        selection_method="tournament",
        crossover_method="ox",
    )

    print("Best fitness:", round(result["best_fitness"], 2))
