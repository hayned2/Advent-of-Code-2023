import os
import heapq

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day17_input.txt')
lines = input.readlines()
input.close()

height = len(lines)
width = len(lines[0].strip())
heat_map = {}

# Convert to a map of integers
for index, row in enumerate(lines):
    map_row = {}
    for index2, value in enumerate(row.strip()):
        map_row[index2] = int(value)
    heat_map[index] = map_row
    
# Converts from a direction to the correspnding movement in coordinates
directions_to_deltas = {
    'L': (0, -1),
    'R': (0, 1),
    'U': (-1, 0),
    'D': (1, 0),
}

# Quick lookup for opposite directions
opposite_directions = {
    'R': 'L',
    'L': 'R',
    'U': 'D',
    'D': 'U',
    'N': 'N'
}

# Ultra is False for pt. 1, True for pt. 2
def find_path(ultra):

    # Start with the top-left corner
    open_set = [(0, (0,0), 'N')]
    closed = set()

    # Iterate until we have nowhere left to check (shouldn't happen)
    while len(open_set) > 0:

        # Introducing heap priority queues. Efficient data structure for popping off the smallest values from a list
        # Grab the next unexplored node with the lowest current heat value
        current_node = heapq.heappop(open_set)
        current_heat, current_pos, prev_directions = current_node

        # Make sure we haven't seen this state already
        if (current_pos, prev_directions) in closed:
            continue
        closed.add((current_pos, prev_directions))
        
        # We've reached the end! Make sure we can stop for pt. 2
        if current_pos == (height - 1, width - 1):
            if not ultra:
                print("The coolest path for the normal crucible has a heat value of:", current_heat)
                return
            elif len(prev_directions) >= 4:
                print("The coolest path for the ultra crucible has a heat value of:", current_heat)
                return

        # Go over each of the four directions, skipping invalid moves
        for dir in 'LDUR':

            new_position = (current_pos[0] + directions_to_deltas[dir][0], current_pos[1] + directions_to_deltas[dir][1])

            # If the move takes us out of bounds, skip
            if new_position[0] < 0 or new_position[1] < 0 or new_position[0] >= height or new_position[1] >= width:
                continue

            # If it's pt. 2 and we haven't taken 4 steps in one direction yet and we're trying to turn, skip
            if ultra and prev_directions[-1] != 'N' and dir != prev_directions[-1] and len(prev_directions) < 4:
                continue

            # If we're trying to go straight and exceed our limit, skip
            if dir == prev_directions[-1] and len(prev_directions) == (10 if ultra else 3):
                continue

            # If we're trying to do a 180 turn, skip
            if dir == opposite_directions[prev_directions[-1]]:
                continue

            # Track the last set of matching directions
            if dir == prev_directions[-1]:
                new_directions = prev_directions + dir
            else:
                new_directions = dir

            if (new_position, new_directions) in closed:
                continue

            new_heat = current_heat + heat_map[new_position[0]][new_position[1]]
            heapq.heappush(open_set, (new_heat, new_position, new_directions))

find_path(False)
find_path(True)
