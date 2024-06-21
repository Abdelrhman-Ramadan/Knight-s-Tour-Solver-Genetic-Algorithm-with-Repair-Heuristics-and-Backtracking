import statistics as sta
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from GeneticAlgorithms import Genetic
# random.seed(20)
genetic_algorithm = Genetic()
genetic_algorithm.N = 8
genetic_algorithm.max_generations = 2500
genetic_algorithm.population_size = 1000
genetic_algorithm.crossover_rate = 0.95
genetic_algorithm.mutation_rate = 0.005
number_solutions_per_generation , fitness_values_per_generation = genetic_algorithm.run_genetic_algorithm_ANALYSIS(use_heuristic=True)
generations = []
average_fitness = []
for i in range(len(fitness_values_per_generation)):
    generations.append(fitness_values_per_generation[i][0])
    average_fitness.append(sta.mean(fitness_values_per_generation[i][1]))

# Sample data
x = np.array(generations)
y = np.array(average_fitness)

# Generate a smooth curve using cubic spline interpolation
spl = make_interp_spline(x, y, k=3)
x_smooth = np.linspace(x.min(), x.max(), 1000)
y_smooth = spl(x_smooth)

# Plotting the smooth curve
plt.plot(x_smooth, y_smooth, label='Progression of Fitness', color='blue')
plt.yscale('log')  # Set logarithmic scale for the y-axis


# Adding labels to the plot
plt.xlabel('Generation')
plt.ylabel('Average Fitness')
plt.title('Progression of Fitness over time')
plt.legend()

# Display the plot
plt.show()