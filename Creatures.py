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


def main():
    pop = population(100, 3, 10)

    for i in pop.individuals:
        print(i.name)
        print(i.fitness)
        print("\n")

    print("\nfirst parent")
    print(pop.individuals[20].chromosome)
    print("fitness")
    print(pop.individuals[20].fitness)

    print("\nsecond parent")
    print(pop.individuals[42].chromosome)
    print("fitness")
    print(pop.individuals[42].fitness)

    child = reproduce(pop.individuals[20], pop.individuals[42])
    print("\noffspring")
    print(child.chromosome)
    print("fitness")
    print(child.fitness)

    del pop


if __name__ == '__main__':
    main()
