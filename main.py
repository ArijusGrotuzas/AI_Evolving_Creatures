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
land = create_landscape(land_size, 0.45, 0.1, 0.85)

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


# A list for storing all populations
all_populations = []

# Create initial population of creatures and attach it to a list of all populations
pop = population(4, 3, 4)
all_populations.append(pop)

# Spawning initial individuals
for indi in pop.individuals:
    spawned = False
    while spawned is False:
        position_x = random.randint(0, land_size - 1)
        position_z = random.randint(0, land_size - 1)

        if land[position_x][position_z] != 1 and land[position_x][position_z] != 2:
            indi.pos = (position_x, position_z)
            spawned = True

# Create a predator
hunter = predator((0, 0))
hunter.find_closest_target(all_populations)
hunter.calculate_target_path(land_copy_predator)

# Getting a landscape that features all bunny locations
land_copy_bunnies = land_w_bunnies(land_copy_predator, all_populations)

# Main game loop
iterations = 0
generations = 1
run = True
while run:
    window.fill((0, 0, 0))
    draw_landscape()

    if iterations == 5:
        new_pop = genetic_algorithm(all_populations[-1], 2)
        for i in new_pop.individuals:
            i.spawn_near_parent(land_copy_bunnies)
            land_copy_bunnies = land_w_bunnies(land_copy_predator, all_populations)
        if len(new_pop.individuals) != 0:
            generations += 1
            print("Generation number: " + str(generations) + " was born!")
        all_populations.append(new_pop)
        iterations = 0

    # Find closest target at each point in time, and move predator closer each time to it
    hunter.find_closest_target(all_populations)
    hunter.calculate_target_path(land_copy_predator)
    try:
        hunter.pos = hunter.path[1]
    except IndexError:
        hunter.pos = hunter.path[0]

    # Check if the predator is close to the prey, if so remove the prey
    diff = difference(hunter.pos, hunter.target)
    dist = magnituted(diff)
    if dist < 1:
        remove_based_on_pos(all_populations, hunter.target)

    # Loop through all existing populations and draw each bunny
    for pop in all_populations:
        for i in pop.individuals:
            i.move_random(land_copy_bunnies)
            land_copy_bunnies = land_w_bunnies(land_copy_predator, all_populations)
            window.blit(bunny[i.chromosome[0] - 1], (i.pos[0] * 32, i.pos[1] * 32))

    window.blit(wolf, (hunter.pos[0] * 32, hunter.pos[1] * 32))

    # Check if the user has pressed exit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    iterations += 1
    pygame.time.delay(700)

    pygame.display.update()
