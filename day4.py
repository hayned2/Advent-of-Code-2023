import os

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day4_input.txt')

# Tracker for pt. 1's total score
total_score = 0

# Tracker for how many of each card we have
card_counts = {}

for line in input:
    
    # For each card, track how many winning numbers we have
    card_winners = 0

    # Grab the card's number (could just iterate this, but you never know...)
    card_number = int(line.split()[1][:-1])

    # If we haven't gained any extra copies of this card yet, we need to initialize its entry in the dictionary
    if card_number not in card_counts:
        card_counts[card_number] = 0

    # By default, we get one original copy of each card
    card_counts[card_number] += 1

    # Parse out the winning numbers and the card's numbers
    winning_numbers = line.split('|')[0].split()[2:]
    card_numbers = line.split('|')[1].split()

    # Count how many card numbers are winning numbers
    for number in card_numbers:
        if number in winning_numbers:
            card_winners += 1

    # Increase the total score for pt. 1 based on the number of winning cards
    total_score += 2 ** (card_winners - 1) if card_winners > 0 else 0

    # For each winning number, add copies of the following cards to the dictionary
    for x in range(1, card_winners + 1):
        next_card = card_number + x
        if next_card not in card_counts:
            card_counts[next_card] = 0
        card_counts[next_card] += card_counts[card_number]

print("The total score of all the winning cards together is:", total_score)
print("The total number of scratch cards collected is:", sum(card_counts.values()))