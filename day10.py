import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day10_input.txt')
lines = input.readlines()
input.close()

# Create a map of the pipes and what nodes they connect to, and locate the Start node
# There's no point tracking pipe connections if they don't connect to each other
map = {}
start = None
width = len(lines[0]) - 1
height = len(lines)
for row in range(len(lines)):
    for column in range(len(lines[row]) - 1):

        if lines[row][column] == '|' and row > 0 and row < height - 1 and lines[row - 1][column] in '|F7S' and lines[row + 1][column] in '|JLS':
            map[(row, column)] = [(row - 1, column), (row + 1, column)]

        elif lines[row][column] == '-' and column > 0 and column < width - 1 and lines[row][column - 1] in '-FLS' and lines[row][column + 1] in '-7JS':
            map[(row, column)] = [(row, column - 1), (row, column + 1)]

        elif lines[row][column] == 'L' and row > 0 and column < width - 1 and lines[row - 1][column] in '|F7S' and lines[row][column + 1] in '-7JS':
            map[(row, column)] = [(row - 1, column), (row, column + 1)]

        elif lines[row][column] == 'J' and row > 0 and column > 0 and lines[row - 1][column] in '|F7S' and lines[row][column - 1] in '-FLS':
            map[(row, column)] = [(row - 1, column), (row, column - 1)]

        elif lines[row][column] == '7' and column > 0 and row < height - 1 and lines[row][column - 1] in '-FLS' and lines[row + 1][column] in '|JLS':
            map[(row, column)] = [(row, column - 1), (row + 1, column)]   

        elif lines[row][column] == 'F' and row < height - 1 and column < width - 1 and lines[row + 1][column] in '|JLS' and lines[row][column + 1] in '-7JS':
            map[(row, column)] = [(row + 1, column), (row, column + 1)]

        elif lines[row][column] == 'S':
            start = (row, column)

# Check the 4 nodes that are adjacent to the Start and connect them to the Start in the map.
# Manual inspection found that the Start only ever has two pipes connecting to it.
map[start] = []

above = (start[0] - 1, start[1])
if above in map and start in map[above]:
    map[start].append(above)

below = (start[0] + 1, start[1])
if below in map and start in map[below]:
    map[start].append(below)

left = (start[0], start[1] - 1)
if left in map and start in map[left]:
    map[start].append(left)

right = (start[0], start[1] + 1)
if right in map and start in map[right]:
    map[start].append(right)

# Function that searches for a loop and tracks blocked half-steps for pt. 2
def calculate_loop(starting_node):
    
    current_node = starting_node
    visited_nodes = []
    blocked_half_steps = set()

    while True:

        # Get the connected nodes to our current one, make sure we're going in the right direction around the loop
        connected_nodes = map[current_node]
        if current_node == starting_node:
            next_node = connected_nodes[0]
        else:
            if connected_nodes[0] != visited_nodes[-1]:
                next_node = connected_nodes[0] 
            else:
                next_node = connected_nodes[1]

        # Track the blocked half-steps for pt. 2
        blocked_half_steps.add(((current_node[0] + next_node[0]) / 2, (current_node[1] + next_node[1]) / 2))

        # Move to the next node
        visited_nodes.append(current_node)
        current_node = next_node

        # If we find the starting_node then we've found the loop
        if current_node == starting_node:
            return set(visited_nodes), blocked_half_steps

loop, blocked_half_steps = calculate_loop(start)
print("The number of steps to the farthest point in the loop from the start is:", len(loop) // 2)

# Calculate the loop's boundaries, nothing outside these boundaries could be contained within the loop
loop_top = height
loop_bottom = 0 
loop_right = 0
loop_left = width
for node in loop:
    loop_top = min(loop_top, node[0])
    loop_bottom = max(loop_bottom, node[0])
    loop_right = max(loop_right, node[1])
    loop_left = min(loop_left, node[1])

# Find all tiles that could potentially be contained within the loop
potential_insiders = set()
for row in range(loop_top, loop_bottom + 1):
    for column in range(loop_left, loop_right + 1):
        if (row, column) not in loop:
            potential_insiders.add((row, column))

# Track the tiles as they end up being categorized as inside or outside
insiders = set()
outsiders = set()

# Iterate until we have classified every node that might be contained by the loop
while len(potential_insiders) > 0:

    # Grab a random node from the candidates (without removing it from the set) and add it to the queue
    outside = False
    starting_node = potential_insiders.pop()
    potential_insiders.add(starting_node)
    queue = set()
    visited = set()
    queue.add(starting_node)

    # From the candidate, keep exploring until we run out of paths, or find an exit to the outside
    while len(queue) > 0 and not outside:

        # Mark the current node as visited so we know not to check it again
        current_node = queue.pop()
        visited.add(current_node)

        # If we connect to a node that we know is connected to the outside, we know we are also connected to the outside
        if current_node in outsiders:
            outside = True
            break

        # Calculate the 4 neighbors in each direction
        neighbors = [(current_node[0] - 0.5, current_node[1]), (current_node[0] + 0.5, current_node[1]), (current_node[0], current_node[1] - 0.5), (current_node[0], current_node[1] + 0.5)]
        for neighbor in neighbors:

            # Find the neighbors that are valid places to continue searching from
            if neighbor not in loop and neighbor not in blocked_half_steps and neighbor not in visited:

                # If we found a neighbor that is on or out of the boundary, we've reached the "outside"
                if neighbor[0] <= loop_top or neighbor[0] >= loop_bottom or neighbor[1] <= loop_left or neighbor[1] >= loop_right:
                    outside = True
                    break

                # Otherwise we add the neighbor to the queue to continue searching
                queue.add(neighbor)

    # Use set operators to move the now-classified nodes from potential_insiders to insiders / outsiders correctly
    if not outside:
        insiders = insiders.union(potential_insiders.intersection(visited))
    else:
        outsiders = outsiders.union(potential_insiders.intersection(visited))

    # Remove the now-classified nodes from potential_insiders now that they've been checked
    potential_insiders = potential_insiders.difference(visited)

print("The number of tiles that are enclosed by the loop is:", len(insiders))
    