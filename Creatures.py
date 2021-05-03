import random
import string


class individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.asses_fitness(self.chromosome)
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


class population:
    def __init__(self, size, chromo_size, max_value):
        self.individuals = self.random_individuals(size, chromo_size, max_value)
        self.generation_age = 0

    @staticmethod
    def random_individuals(size, chromo_size, max_value):
        return [individual([random.randint(1, max_value) for _ in range(chromo_size)]) for _ in range(size)]


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
    for i in range(offspring_number):
        first_parent = random_selection(pop)
        second_parent = random_selection(pop)
        child = reproduce(first_parent, second_parent)
        chance = random.uniform(0, 1)
        if chance < mutation_probability:
            mutate(child, 10)
        new_pop.individuals.append(child)

    return new_pop


def main():
    pop = population(10, 3, 10)
    print("Old generation: \n")
    for i in pop.individuals:
        print(i.name)
        print(i.fitness)
        print("\n")

    print("\n \nNew generation: \n")
    new_pop = genetic_algorithm(pop, 5)
    for i in new_pop.individuals:
        print(i.name)
        print(i.fitness)
        print("\n")


if __name__ == '__main__':
    main()
