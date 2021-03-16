import random
import string


class individual:
    def __init__(self, size, max_val):
        self.chromosome = self.rand_chromosome(size, max_val)
        self.fitness = self.asses_fitness(self.chromosome)
        self.name = self.rand_name(size)

    @staticmethod
    def rand_chromosome(size, max_val):
        return [random.randint(1, max_val) for _ in range(size)]

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
    def __init__(self, size):
        self.individuals = self.random_individuals(size)
        self.generation_age = 0

    @staticmethod
    def random_individuals(size):
        return [individual(3, 10) for _ in range(size)]


def get_most_fit(populous):
    most_fit = populous.individuals[0]

    for i in populous.individuals:
        if i.fitness > most_fit.fitness:
            most_fit = i

    return most_fit


def main():
    pop = population(10)

    for i in pop.individuals:
        print(i.name)
        print(i.fitness)
        print("\n")

    print("\nmost fit: ")
    maximus_fitnesus = get_most_fit(pop)
    print(maximus_fitnesus.name)

    del pop


if __name__ == '__main__':
    main()
