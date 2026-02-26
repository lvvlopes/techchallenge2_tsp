"""Demo for Projeto 2 item 1.2 (restrições realistas no VRP com GA)."""

from genetic_algorithm import default_problems, run_vrp_ga_experiment


def main():
    # índice 0 é o depósito
    cities = [(0, 0)] + default_problems[10]

    # demanda por ponto (0 no depósito)
    demands = [0, 1, 2, 1, 3, 2, 1, 2, 1, 3, 2]

    # prioridade por entrega (0 no depósito)
    priorities = [0, 5, 1, 3, 4, 2, 5, 1, 2, 4, 3]

    # restrições dos veículos
    vehicle_capacities = [8, 8, 8]
    vehicle_max_distances = [1300, 1300, 1300]

    result = run_vrp_ga_experiment(
        cities_locations=cities,
        demands=demands,
        priorities=priorities,
        vehicle_capacities=vehicle_capacities,
        vehicle_max_distances=vehicle_max_distances,
        population_size=80,
        n_generations=120,
        mutation_probability=0.25,
    )

    print("Best fitness:", round(result["best_fitness"], 2))
    print("Best routes (vehicle -> customers):")
    for i, route in enumerate(result["best_solution"], start=1):
        print(f"  Veículo {i}: {route}")


if __name__ == "__main__":
    main()
