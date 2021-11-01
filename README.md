# Description ![alt text](https://github.com/ArijusGrotuzas/AI_Evolving_Creatures/blob/main/Bunny/Bunny3.png?raw=true)![alt text](https://github.com/ArijusGrotuzas/AI_Evolving_Creatures/blob/main/Wolf/Wolf.png?raw=true)

The mini-project features an evolving creatures simulation using a genetic algorithm, and A* path finding. The simulation involves two types of agents, a predator, and a prey agent respectively. The environment features accessible and obstacle tiles, where the size is determined by a 20 x 20 grid. The simulation ends once all of the prey agents reach maximum fitness and make the predator agent die of starvation, or when the predator agent consumes all the preys.

# Contents
- [A*](#A*)
- [Genetic-algorithm](#Genetic-algorithm)

## A*

`A* pathfinding algorithm for moving the predator agent:`

The A* pathfinding algorithm is an informed search algorithm, meaning it doesnot check every single possible path, but instead always moves in the right directionwhich makes this approach a lot more efficient. The goal of the algorithm is to findthe shortest path from the start node to the goal node in a graph by using the edgesthat connect the nodes.

![alt text](https://github.com/ArijusGrotuzas/AI_Evolving_Creatures/blob/main/Examples/AI%20example.gif?raw=true)

## Genetic algorithm

`Genetic algorithm for evolving the prey agents, so that they can become better at avoiding the predator:`

`GA` generates new states by combining two parent states,rather than modifying an existing state, which is the case with many optimizationalgorithms. The algorithm takes a population of candidates that serve as a potentialsolutions to a search or an optimization problem and evolves them to better solutionsuntil a most optimal solution is found or a certain amount of time has elapsed

![alt text](https://github.com/ArijusGrotuzas/AI_Evolving_Creatures/blob/main/Examples/AI%20example4.gif?raw=true)
