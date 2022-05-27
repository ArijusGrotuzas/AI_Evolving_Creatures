# Description ![alt text](https://github.com/ArijusGrotuzas/AI_Evolving_Creatures/blob/main/Bunny/Bunny3.png?raw=true)![alt text](https://github.com/ArijusGrotuzas/AI_Evolving_Creatures/blob/main/Wolf/Wolf.png?raw=true)

The mini-project features an evolving creature simulation using a genetic algorithm and A* path-finding algorithm. The simulation involves two agents, a predator, and a prey agent. The environment features obstacle tiles and traversable tiles. The size of the tiles is determined by a 20 x 20 grid. The simulation ends once prey agents reach maximum fitness and make the predator agent die of starvation or when the predator agent consumes all the prey.

## Contents
- [A*](#A-star)
- [Genetic-algorithm](#Genetic-algorithm)

## A star

`A* pathfinding algorithm for moving the predator agent:`

The A* pathfinding algorithm is an informed search algorithm, meaning it does not check every possible path, but instead always moves in the right direction, which makes it more efficient. The aim is to find the shortest path from the start node to the goal node in a graph by using the edges that connect the nodes.

![alt text](https://github.com/ArijusGrotuzas/AI_Evolving_Creatures/blob/main/Examples/AI%20example.gif?raw=true)

## Genetic algorithm

`Genetic algorithm for evolving the prey agents, so that they can become better at avoiding the predator:`

GA generates new states by combining two-parent states, rather than modifying an existing state, which is the case with many optimization algorithms. The algorithm takes a population of candidates that serve as a potential solution to a search or an optimization problem and evolves them into better solutions until the most optimal solution is found or a certain amount of time has elapsed.

![alt text](https://github.com/ArijusGrotuzas/AI_Evolving_Creatures/blob/main/Examples/AI%20example4.gif?raw=true)
