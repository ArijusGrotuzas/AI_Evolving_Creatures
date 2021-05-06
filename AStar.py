
class Node:

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(landscape, start, end):
    # Creating a start node
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0

    # Creating a goal node
    goalNode = Node(None, end)
    goalNode.g = goalNode.h = goalNode.f = 0

    openSet = []
    closedSet = []

    # Adding the start node to the open set
    openSet.append(startNode)

    # Looping until the open set contains nodes
    while len(openSet) > 0:

        # Get the current node
        currentNode = openSet[0]
        currentIndex = 0
        for index, item in enumerate(openSet):
            if item.f < currentNode.f:
                currentNode = item
                currentIndex = index

        # Removing the current node from the open set and adding it into the closed set
        openSet.pop(currentIndex)
        closedSet.append(currentNode)

        # Goal node has been found
        if currentNode == goalNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # returning the path from the goal node to the starting node

        children = []
        # Defining in which directions children can be in (in this case, up, right, down, left, and diagonally)
        for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])

            if nodePosition[0] > (len(landscape) - 1) or nodePosition[0] < 0 or nodePosition[1] > (
                    len(landscape[len(landscape) - 1]) - 1) or nodePosition[1] < 0:
                continue

            # Making sure it contains no obstacles
            if landscape[nodePosition[0]][nodePosition[1]] != 0:
                continue

            # Create new node
            newNode = Node(currentNode, nodePosition)
            children.append(newNode)

        for child in children:

            for closed_child in closedSet:
                if child == closed_child:
                    continue

            # F G and H scores
            child.g = currentNode.g + 1
            child.h = ((child.position[0] - goalNode.position[0]) ** 2) + (
                        (child.position[1] - goalNode.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for openNode in openSet:
                if child == openNode and child.g > openNode.g:
                    continue

            # Add the child to the open list
            openSet.append(child)


def main():
    # 1 = obstacle, 0 = walkable node
    landscape = [[0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0],
                 [0, 1, 1, 0, 0],
                 [0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0], ]

    # landscape2 = create_landscape(50, 0.45, 0.1)

    start = (0, 0)
    end = (4, 4)

    path = astar(landscape, start, end)
    print(path)


if __name__ == '__main__':
    main()
