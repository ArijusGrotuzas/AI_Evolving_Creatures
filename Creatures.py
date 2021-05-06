from AStar import *
import math
import numpy as np
import random
import string


# Function for calculating magnitude of a vector
def magnituted(vector_2d):
    (x, y) = vector_2d
    mag = math.sqrt(pow(x, 2) + pow(y, 2))
    return mag


# Function to subtract twp tuples
def difference(a, b):
    diff = tuple(map(lambda i, j: i - j, a, b))
    return diff


# Class for the predator agent
class predator:
    def __init__(self, starting_pos):
        self.pos = starting_pos
        self.new_pos = starting_pos
        self.positions_diff = difference(self.pos, self.new_pos)
        self.target = None
        self.path = []
        self.hunger = 1

    def find_closest_target(self, prey):
        target = None
        smallest_dist = 10000

        for p in prey:
            for i in p.individuals:
                diff = difference(i.pos, self.pos)
                dist = magnituted(diff)
                if dist < smallest_dist:
                    smallest_dist = dist
                    target = i.pos

        self.target = target

    def posfloat_to_int(self):
        self.pos = (int(self.pos[0]), int(self.pos[1]))

    def calculate_target_path(self, landscape):
        self.path = astar(landscape, self.pos, self.target)

    def set_position_diff(self):
        self.positions_diff = difference(self.new_pos, self.pos)


class individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome  # Chromosome is an array of values for different attributes of individual
        # [0] - color, [1] - speed, [2] - vision
        self.fitness = self.asses_fitness(self.chromosome)
        self.parent_pos = (0, 0)
        self.pos = (0, 0)
        self.new_pos = (0, 0)
        self.positions_diff = (0, 0)
        self.name = self.rand_name(3)

    @staticmethod
    def asses_fitness(arr):
        fitness = 0
        for i in arr:
            fitness += i

        return fitness

    @staticmethod
    def rand_name(size):
        name = ''.join(random.choice(string.ascii_letters) for _ in range(size))
        return name

    def move_random(self, land):
        land_size = len(land)
        spawned = False
        iterations = 0

        while not spawned and iterations < 1000:
            x_dir = random.randint(-1, 1)
            z_dir = random.randint(-1, 1)

            new_pos = (self.pos[0] + x_dir, self.pos[1] + z_dir)

            if -1 < new_pos[0] < land_size and -1 < new_pos[1] < land_size:
                if land[new_pos[0]][new_pos[1]] != 1:
                    spawned = True
                    self.new_pos = new_pos
                    self.positions_diff = difference(new_pos, self.pos)
                else:
                    self.positions_diff = (0, 0)
            else:
                self.positions_diff = (0, 0)

            iterations += 1

    def new_random_pos(self, land):
        land_size = len(land)
        spawned = False

        while not spawned:
            x_pos = random.randint(0, land_size)
            z_pos = random.randint(0, land_size)

            if -1 < x_pos < land_size and -1 < z_pos < land_size:
                if land[x_pos][z_pos] != 1:
                    spawned = True
                    self.pos = (x_pos, z_pos)
                    self.new_pos = (x_pos, z_pos)

    def spawn_near_parent(self, land):
        spawned = False
        self.parent_pos = (int(self.parent_pos[0]), int(self.parent_pos[1]))
        for i in range(self.parent_pos[0] - 3, self.parent_pos[0] + 3):
            for j in range(self.parent_pos[1] - 3, self.parent_pos[1] + 3):
                try:
                    if land[i][j] != 1:
                        self.pos = (i, j)
                        self.new_pos = (i, j)
                        spawned = True
                except IndexError:
                    continue

        if not spawned:
            self.new_random_pos(land)

    def predator_in_sight(self, predator_pos):
        diff = difference(predator_pos, self.pos)
        dist = magnituted(diff)
        if dist < self.chromosome[2]:
            return True
        else:
            return False

    def run(self, predator_pos, land):
        furthest_pos = self.pos
        furthest_dist = 0

        for i in range(self.pos[0] - self.chromosome[1], self.pos[0] + self.chromosome[1]):
            for j in range(self.pos[1] - self.chromosome[1], self.pos[1] + self.chromosome[1]):
                try:
                    if min(i, j) < 0:
                        continue
                    if land[i][j] != 1:
                        diff = difference(predator_pos, (i, j))
                        dist = magnituted(diff)
                        if dist > furthest_dist:
                            furthest_pos = (i, j)
                            furthest_dist = dist
                except IndexError:
                    continue

        self.new_pos = furthest_pos
        self.positions_diff = difference(self.new_pos, self.pos)


class population:
    def __init__(self, size, chromo_size, max_value):
        self.individuals = self.random_individuals(size, chromo_size, max_value)
        self.generation_age = 0

    @staticmethod
    def random_individuals(size, chromo_size, max_value):
        return [individual([random.randint(0, max_value) for _ in range(chromo_size)]) for _ in range(size)]

    def get_average_fitness(self):
        total_fitness = 0
        for i in self.individuals:
            total_fitness += i.fitness

        avg_fitness = total_fitness / len(self.individuals)
        return avg_fitness


def get_most_fit(populous):
    most_fit = populous.individuals[0]

    for i in populous.individuals:
        if i.fitness > most_fit.fitness:
            most_fit = i

    return most_fit


def mutate(singula, max_val):
    singula.chromosome[random.randint(0, len(singula.chromosome) - 1)] = random.randint(-2, max_val)


def reproduce(parent_one, parent_two):
    n = len(parent_one.chromosome)
    c = (random.randint(1, n - 1))
    offspring = individual(parent_one.chromosome[0:c] + parent_two.chromosome[c:n])
    return offspring


def random_selection(pop):
    total_fitness = sum(indi.fitness for indi in pop.individuals)
    threshold = random.uniform(0, total_fitness)
    current = 0
    for indi in pop.individuals:
        current += indi.fitness
        if current > threshold:
            return indi
    return pop.individuals[0]


def genetic_algorithm(pop, offset):
    # Probability that an individual will mutate
    mutation_probability = 0.05

    # Getting a random number of a new generation's size
    offspring_number = random.randint(len(pop.individuals) - offset, len(pop.individuals) + offset)

    # Creating a new population object, with empty individuals list, so that we can append children to it
    new_pop = population(0, 0, 0)

    # Increasing the generation number
    new_pop.generation_age = pop.generation_age + 1

    # Spawning a number of children based on what the size of this generation should be
    for i in range( offspring_number):
        first_parent = random_selection(pop)
        second_parent = random_selection(pop)
        child = reproduce(first_parent, second_parent)
        chance = random.uniform(0, 1)
        if chance < mutation_probability:
            mutate(child, 4)
        child.parent_pos = first_parent.pos
        new_pop.individuals.append(child)

    return new_pop
