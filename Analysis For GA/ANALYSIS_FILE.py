import time

from GeneticAlgorithms import Genetic


def GA_analysis_per_square(N, max_generations, population_size, mutation_rate=0.01, crossover_rate=0.8, number_of_runs=5,
                           use_heuristic=False):
    analysis_per_square = []
    for x in range(N):
        analysis_per_square_row = []
        for y in range(N):
            genetic_algorithm = Genetic()
            genetic_algorithm.N = N
            genetic_algorithm.max_generations = max_generations
            genetic_algorithm.population_size = population_size
            genetic_algorithm.mutation_rate = mutation_rate
            genetic_algorithm.crossover_rate = crossover_rate
            genetic_algorithm.start_position = (x, y)
            count_solution_per_square = 0
            count_the_first_generation_tour_average = 0
            for i in range(number_of_runs):
                number_solutions_per_generation, fitness_values_per_generation = genetic_algorithm.run_genetic_algorithm_ANALYSIS(
                    use_heuristic=use_heuristic)
                # print(number_solutions_per_generation)
                count_solution_per_square += len(number_solutions_per_generation)
                # print(count_solution_per_square)
                if number_solutions_per_generation:
                    count_the_first_generation_tour_average += number_solutions_per_generation[0][0]
            analysis_per_square_row.append(
                (count_the_first_generation_tour_average // number_of_runs, count_solution_per_square))
        analysis_per_square.append(analysis_per_square_row)
        # print(analysis_per_square)

    return analysis_per_square

# random.seed(20)
# N = 8
# max_generations = 50
# population_size = 50
# start_time = time.time()
# analysis_list = GA_analysis_per_square(N, max_generations, population_size)
# end_time = time.time()
# runtime = end_time - start_time
# print(f'The run time was: {runtime} Sec')
# for i in range(N):
#     print(analysis_list[:][i])
