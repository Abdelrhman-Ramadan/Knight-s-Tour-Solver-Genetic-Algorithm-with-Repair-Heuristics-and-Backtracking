import random


class Genetic:
    def __init__(self, N=8, population_size=50, max_generations=100, crossover_rate=0.8, mutation_rate=0.01):
        # Initialize Genetic Algorithm parameters
        self.N = N
        self.population_size = population_size
        self.max_generations = max_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.start_position = (0, 0)
        self.current_x = self.start_position[0]
        self.current_y = self.start_position[1]
        self.fitness_values = []

    def initialize_population(self):
        # Initialize the population with random chromosomes
        population = []
        for _ in range(self.population_size):
            chromosome = [random.randint(1, 8) for _ in range((self.N ** 2) - 1)]
            population.append(chromosome)
        return population

    def move_forward(self, direction):
        # Move the knight forward based on the given direction
        moves = {
            1: (2, 1),
            2: (1, 2),
            3: (-1, 2),
            4: (-2, 1),
            5: (-2, -1),
            6: (-1, -2),
            7: (1, -2),
            8: (2, -1),
        }
        self.current_x += moves[direction][0]
        self.current_y += moves[direction][1]

    def trace_back(self, direction):
        # Trace back a move for the knight
        moves = {
            1: (-2, -1),
            2: (-1, -2),
            3: (1, -2),
            4: (2, -1),
            5: (2, 1),
            6: (1, 2),
            7: (-1, 2),
            8: (-2, 1),
        }
        self.current_x += moves[direction][0]
        self.current_y += moves[direction][1]

    def evaluate_fitness_matrix(self, chromosome, use_heuristic=False):
        self.current_x = self.start_position[0]
        self.current_y = self.start_position[1]
        visited_board = [[False for _ in range(self.N)] for _ in range(self.N)]
        visited_board[self.current_x][self.current_y] = True
        num_legal_moves = 0
        for i in range(0, len(chromosome)):
            legal, chromosome[i] = self.move_matrix(chromosome[i], visited_board, use_heuristic)
            if not legal:
                return num_legal_moves
            else:
                num_legal_moves += 1
                visited_board[self.current_x][self.current_y] = True
        return num_legal_moves

    def move_matrix(self, move, board, use_heuristic=False):
        legal = False
        limit = 0
        while not legal and limit < 8:
            self.move_forward(move)
            legal = self.is_valid_move(self.current_x, self.current_y, board)
            if not legal:
                self.trace_back(move)
                if use_heuristic:
                    heuristic_moves = self.get_next_moves(self.current_x, self.current_y, board)
                    best_move = self.get_first_non_zero_element(heuristic_moves)
                    if best_move is None:
                        return legal, move
                    else:
                        move = best_move
                else:
                    move = (move % 8) + 1
            limit += 1
        return legal, move

    @staticmethod
    def get_first_non_zero_element(my_list):
        if not my_list:
            return None

        new_list = [tbl[1] for tbl in my_list]
        first_non_zero_index = next((index for index, value in enumerate(new_list) if value != 0), None)

        if first_non_zero_index is None:
            return my_list[0][0]
        elif first_non_zero_index == 0:
            return my_list[0][0]
        else:
            return my_list[first_non_zero_index][0]

    def is_valid_move(self, x, y, board):
        legal = False
        if 0 <= x < self.N and 0 <= y < self.N:
            legal = True
            if board[x][y]:
                legal = False
        return legal

    def get_next_moves(self, x, y, board):
        next_moves = []
        moves = (
            (2, 1),
            (1, 2),
            (-1, 2),
            (-2, 1),
            (-2, -1),
            (-1, -2),
            (1, -2),
            (2, -1)
        )
        for move in moves:
            next_x, next_y = x + move[0], y + move[1]
            if self.is_valid_move(next_x, next_y, board):
                count = sum(1 for m in moves if self.is_valid_move(next_x + m[0], next_y + m[1], board))
                next_moves.append((moves.index(move) + 1, count))
        return sorted(next_moves, key=lambda index: index[1])

    def select_parents(self, population, use_heuristic=False):
        for i in range(self.population_size):
            self.fitness_values.append(self.evaluate_fitness_matrix(population[i], use_heuristic))
        total_fitness = sum(self.fitness_values)
        probabilities = [fitness / total_fitness for fitness in self.fitness_values]
        parents = random.choices(population, weights=probabilities, k=self.population_size)
        return parents

    def crossover(self, parent1, parent2):
        if random.random() > self.crossover_rate:
            return random.choice([parent1, parent2])
        crossover_point = random.randint(1, self.N * self.N - 1)
        offspring = parent1[:crossover_point] + parent2[crossover_point:]
        return offspring

    def mutation_flip(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                individual[i] = random.randint(1, 8)
        return individual

    def run_genetic_algorithm(self, use_heuristic=False):
        # Run the Genetic Algorithm for finding a solution
        population = self.initialize_population()
        for generation in range(self.max_generations):
            self.fitness_values = []
            parents = self.select_parents(population, use_heuristic)
            offspring = []
            for i in range(0, self.population_size, 2):
                parent1 = parents[i]
                parent2 = parents[i + 1]
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                offspring.extend([self.mutation_flip(child1), self.mutation_flip(child2)])
            population = offspring
            self.fitness_values = []

            for chromosome in population:
                value = self.evaluate_fitness_matrix(chromosome, use_heuristic)
                self.fitness_values.append(value)
            best_fitness = max(self.fitness_values)
            max_index = self.fitness_values.index(best_fitness)
            print(f'Fittest Chromosome: {population[max_index]}')
            print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")
            if best_fitness == self.N * self.N - 1:

                return (population[max_index], generation + 1, best_fitness, self.decode_best_chromosome(
                    population[max_index]))

    def run_genetic_algorithm_ANALYSIS(self, use_heuristic=False):
        # Run the Genetic Algorithm for finding a solution
        population = self.initialize_population()
        fitness_values_per_generation = []
        number_solutions_per_generation = []

        for generation in range(self.max_generations):
            self.fitness_values = []
            parents = self.select_parents(population, use_heuristic)
            offspring = []
            for i in range(0, self.population_size, 2):
                parent1 = parents[i]
                parent2 = parents[i + 1]
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                offspring.extend([self.mutation_flip(child1), self.mutation_flip(child2)])

            population = offspring
            self.fitness_values = []

            for chromosome in population:
                value = self.evaluate_fitness_matrix(chromosome, use_heuristic)
                self.fitness_values.append(value)

            fitness_values_per_generation.append((generation + 1, self.fitness_values))

            for i, fitness in enumerate(self.fitness_values):
                if fitness == self.N * self.N - 1:
                    number_solutions_per_generation.append((generation + 1, fitness))

        return number_solutions_per_generation, fitness_values_per_generation

    def decode_best_chromosome(self, chromosome):
        self.current_x = self.start_position[0]
        self.current_y = self.start_position[1]
        path = [(self.current_x, self.current_y)]
        for gene in chromosome:
            self.move_forward(gene)
            path.append((self.current_x, self.current_y))
        return path
