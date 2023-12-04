import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day3_input.txt')

# Variables for tracking numbers and totals as we find them
current_number = ''
current_number_start = None
part_number_sum = 0
gear_ratios_sum = 0

# Track the locations of gears when we find them
gears = {}

# Read the input so we can calculate the size of the grid
lines = input.readlines()
width = len(lines[0]) - 1
height = len(lines)

# Iterate over the grid
for x in range(height):
    for y in range(width):

        # If we find a number, track it
        if lines[x][y].isdigit():
            if current_number == '':
                current_number_start = y
            current_number += lines[x][y]

        # If we reach the end of a line or find a non-digit then we want to search for adjacent symbols
        if not lines[x][y].isdigit() or y + 1 == width:

            # ... if we are currently tracking a number, that is
            if current_number != '':

                # Get the bounding box surrounding our tracked number and iterate over it
                column_range = range(max(current_number_start - 1, 0), y + 1)
                row_range = range(max(x - 1, 0), min(x + 2, height))
                is_part_number = False
                for y2 in column_range:
                    if is_part_number:
                        break
                    for x2 in row_range:
                        # Look for adjacent symbols...
                        if lines[x2][y2] not in '0123456789.':
                            is_part_number = True
                            # If we found a symbol, check if it's a gear. If it is, add the tracked number to this gear's dictionary list
                            if lines[x2][y2] == '*':
                                if (x2, y2) not in gears:
                                    gears[(x2, y2)] = [current_number]
                                else:
                                    gears[(x2, y2)].append(current_number)
                
                # Increment the sum for pt. 1 if it's a part number
                if is_part_number:
                    part_number_sum += int(current_number)

                # Reset our tracked number data
                current_number = ''
                current_number_start = None

# Look for gears that have exactly 2 adjacent numbers and calculate the gear ratios for pt. 2
for gear in gears:
    if len(gears[gear]) == 2:
        gear_ratios_sum += int(gears[gear][0]) * int(gears[gear][1])

print("The sum of the part numbers is:", part_number_sum)
print("The sum of the gear rations is:", gear_ratios_sum)