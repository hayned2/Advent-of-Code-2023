import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day2_input.txt')

# Hard-coded maximum values for each color of cube in pt. 1
max_allowed_reds = 12
max_allowed_greens = 13
max_allowed_blues = 14
possible_games = 0
power_sum = 0

# Iterate over each line
for line in input:

    # Initialize the game as possible
    possible = True
    
    # Track how many of each color we see at one time
    reds = 0
    greens = 0
    blues = 0

    # Track what's the most of each color we see at one time
    max_seen_reds = 0
    max_seen_greens = 0
    max_seen_blues = 0

    # Go through each game, incrementing the colors as we see them
    results = line.split()[2:]
    for x in range(0, len(results), 2):
        if 'red' in results[x + 1]:
            reds += int(results[x])
        elif 'green' in results[x + 1]:
            greens += int(results[x])
        elif 'blue' in results[x + 1]:
            blues += int(results[x])

        # A semicolon denotes the end of a set of cubes, same with the end of the line
        if ";" in results[x + 1] or x == len(results) - 2:            

            # Update the most of a single color we've seen in each set of cubes
            max_seen_reds = max(max_seen_reds, reds)
            max_seen_greens = max(max_seen_greens, greens)
            max_seen_blues = max(max_seen_blues, blues)

            # Check if the game is possible in pt. 1
            if reds > max_allowed_reds or blues > max_allowed_blues or greens > max_allowed_greens:
                possible = False

            # Reset this set of cubes' counts
            reds = 0
            greens = 0
            blues = 0

    # If the game is possible in pt. 1, update the sum for the possible games with the game's ID
    if possible:
        possible_games += int(line.split()[1].replace(":", ""))

    # Calculate the "power" of the game and add it to the sum of powers for all games
    power_sum += max_seen_reds * max_seen_greens * max_seen_blues

print("The sum of IDs of all possible games is", possible_games)
print("The sum of the powers for each game is", power_sum)