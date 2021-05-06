from Creatures import *
from Landscape import *
import pygame
import os

"""Initializing sprites to draw for the game"""
ground_tile = pygame.image.load(os.path.join("Tiles", "Ground.png"))
water_tile = pygame.image.load(os.path.join("Tiles", "Water.png"))
tree = pygame.image.load(os.path.join("Tiles", "Tree.png"))
wolf = pygame.image.load(os.path.join("Wolf", "Wolf.png"))

bunny = []
for i in range(4):
    img = pygame.image.load(os.path.join("Bunny", "Bunny" + str(i) + ".png"))
    bunny.append(img)

"""Initializing size of the window and the screen"""
window_size = 640
land_size = 20
random_threshold = random.uniform(0.37, 0.5)
land = create_landscape(land_size, random_threshold, 0.1, 0.85)

"""Copying the landscapes for the prey and predator agents"""
land_copy_predator = copy_landscape(land)
land_copy_bunnies = copy_landscape(land)

"""Creating the window and giving a name"""
pygame.init()
window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Evolving creatures")


# A function for drawing a landscape
def draw_landscape():
    for i in range(land_size):
        for j in range(land_size):
            if land[i][j] == 1:
                window.blit(water_tile, (i * 32, j * 32))
            elif land[i][j] == 0:
                window.blit(ground_tile, (i * 32, j * 32))
            elif land[i][j] == 2:
                window.blit(ground_tile, (i * 32, j * 32))
                window.blit(tree, (i * 32, j * 32))


def remove_based_on_pos(populations, pos):
    for p in populations:
        for i in reversed(range(len(p.individuals))):
            if p.individuals[i].pos == pos:
                p.individuals.pop(i)


def find_not_empty_population(populations):
    for p in reversed(populations):
        if len(p.individuals) > 0:
            return p


# A list for storing all populations
all_populations = []

# Create initial population of creatures and attach it to a list of all populations
pop = population(10, 3, 4)
all_populations.append(pop)

# Spawning initial individuals
for indi in pop.individuals:
    spawned = False
    while spawned is False:
        position_x = random.randint(0, land_size - 1)
        position_z = random.randint(0, land_size - 1)

        if land[position_x][position_z] != 1 and land[position_x][position_z] != 2:
            indi.pos = (position_x, position_z)
            indi.new_pos = (position_x, position_z)
            spawned = True

# Create a predator
hunter = predator((0, 0))
hunter.find_closest_target(all_populations)
hunter.calculate_target_path(land_copy_predator)

# Getting a landscape that features all bunny locations
land_copy_bunnies = land_w_bunnies(land_copy_predator, all_populations)

# A variable for controlling wether the game should animate onjects moving or create new positions for them
state = "turn"

# Main game loop
animate_iterations = 0
turn_iterations = 0
generations = 1
run = True
while run:
    window.fill((0, 0, 0))
    draw_landscape()

    # If turn state is active it calculates new positions for all the agents to move to
    if state == "turn":

        if hunter.hunger < 0:
            run = False
            print("Wolf died of starvation. Bunnies Won!")

        # If n amount of turns have been made spawn a new generation
        if turn_iterations == 15:
            new_pop = 0
            if len(all_populations[-1].individuals) < 1:
                new_pop = genetic_algorithm(find_not_empty_population(all_populations), 2)
            else:
                new_pop = genetic_algorithm(all_populations[-1], 2)

            for i in new_pop.individuals:
                i.spawn_near_parent(land_copy_bunnies)
                land_copy_bunnies = land_w_bunnies(land_copy_predator, all_populations)
            if len(new_pop.individuals) != 0:
                generations += 1
                print("Generation " + str(generations) + " was born! Average fitness: " + str(
                    new_pop.get_average_fitness()) + ". Number of individuals: " + str(len(new_pop.individuals)))
                print("\n", "~ Wolf's hunger: " + str(hunter.hunger) + " ~", "\n")
            all_populations.append(new_pop)
            turn_iterations = 0

        # Find closest target at each point in time, and move predator closer each time to it
        hunter.posfloat_to_int()
        hunter.find_closest_target(all_populations)
        hunter.calculate_target_path(land_copy_predator)
        try:
            hunter.new_pos = hunter.path[1]
            hunter.set_position_diff()
        except IndexError:
            hunter.new_pos = hunter.path[0]
            hunter.set_position_diff()

        # Check if the predator is close to the prey, if so remove the prey
        diff = difference(hunter.new_pos, hunter.target)
        dist = magnituted(diff)
        if dist < 1:
            remove_based_on_pos(all_populations, hunter.target)
            if hunter.hunger + 0.05 > 1:
                hunter.hunger += 1 - hunter.hunger
            else:
                hunter.hunger += 0.05
        else:
            hunter.hunger -= 0.01

        # Loop through all existing populations and draw each bunny
        for pop in all_populations:
            for i in pop.individuals:
                i.pos = (int(i.pos[0]), int(i.pos[1]))
                if i.predator_in_sight(hunter.new_pos):
                    i.run(hunter.new_pos, land_copy_bunnies)
                else:
                    i.move_random(land_copy_bunnies)
                land_copy_bunnies = land_w_bunnies(land_copy_predator, all_populations)

        state = "animate"
        turn_iterations += 1
    else:  # If animate state is active, then we smoothly animate the agents moving
        # Loop through all existing populations and draw each bunny
        for pop in all_populations:
            for i in pop.individuals:
                x_diff = i.positions_diff[0]
                y_diff = i.positions_diff[1]

                move_x_by = x_diff / 10
                move_y_by = y_diff / 10

                i.pos = (round(i.pos[0] + move_x_by, 1), round(i.pos[1] + move_y_by, 1))

        hunter_x_diff = hunter.positions_diff[0]
        hunter_y_diff = hunter.positions_diff[1]

        move_x_by = hunter_x_diff / 10
        move_y_by = hunter_y_diff / 10

        hunter.pos = (round(hunter.pos[0] + move_x_by, 1), round(hunter.pos[1] + move_y_by, 1))

        animate_iterations += 1

        if animate_iterations >= 10:
            state = "turn"
            animate_iterations = 0

    for pop in all_populations:
        for i in pop.individuals:
            window.blit(bunny[i.chromosome[0] - 1], (i.pos[0] * 32.0, i.pos[1] * 32.0))

    pygame.draw.rect(window, (230, 0, 0), pygame.Rect((hunter.pos[0] * 32), (hunter.pos[1] * 32) - 5, 32, 5))
    pygame.draw.rect(window, (0, 230, 0), pygame.Rect((hunter.pos[0] * 32), (hunter.pos[1] * 32) - 5, hunter.hunger * 32, 5))
    window.blit(wolf, (hunter.pos[0] * 32, hunter.pos[1] * 32))

    # Check if the user has pressed exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.time.delay(30)

    pygame.display.update()
