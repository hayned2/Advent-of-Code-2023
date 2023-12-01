import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day1_input.txt')

# Total counts for parts 1 and 2
total = 0
total2 = 0

# Iterate over each line
for line in input:
    value = ''

    # Go character by character and grab only digits
    for character in line:
        if character.isdigit():
            value += character

    # Error handling for a line that doesn't have any digits (e.g. the example for pt. 2)
    if (len(value) == 0):
        value = '0'

    # Add together the first and last digits (if there's only one digit in a line, that single digit becomes a double-digit for the total: for example lol4lol would be '44')
    total += int(value[0] + value[-1])

    # Reset the value for pt. 2
    value = ''

    # Replace the words with actual digits. There is a mean case in here for the following scenario: eightwothree
    # To handle this, I add the first and last letter in the replacements. So eightwothree becomes eight2othree --> eight2ot3e --> e8t2ot3e. This doesn't seem to cause a problem with generating fake numbers
    line = line.replace('one', 'o1e').replace('two', 't2o').replace('three', 't3e').replace('four', 'f4r').replace('five', 'f5e').replace('six', 's6x').replace('seven', 's7n').replace('eight', 'e8t').replace('nine', 'n9e')
    for character in line:
        if character.isdigit():
            value += character
    total2 += int(value[0] + value[-1])

print("Part 1 Calibration Value:", total)
print("Part 2 Calibration Value:", total2)