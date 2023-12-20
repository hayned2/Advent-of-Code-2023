import os
from math import lcm

# Parse input file
input = open(os.path.dirname(os.path.realpath(__file__)) + '/day20_input.txt')
lines = input.readlines()
input.close()

# Parse the input. Track all the conjunction modules.
# For pt. 2, manual inspection found that 'rx' has a single conjunction module feeding into it, so find that one and mark it down
modules = {}
conjunctions = set()
rx_source = None
for line in lines:
    line = line.strip()
    label, destinations = line.split(" -> ")
    destinations = destinations.split(", ")
    if 'rx' in destinations:
        rx_source = label[1:]
    if label == 'broadcaster':
        modules[label] = destinations
    elif label[0] == '%':
        modules[label[1:]] = ['%', False, destinations]
    elif label[0] == '&':
        modules[label[1:]] = ['&', {}, destinations]
        conjunctions.add(label[1:])

# Update all of the conjunction modules with their inputs
for label in modules:
    destinations = None
    if label == 'broadcaster':
        destinations = modules[label]
    else:
        destinations = modules[label][2]
    for destination in destinations:
        if destination in conjunctions:
            modules[destination][1][label] = 'L'

# Primary function for simulating button presses
def press_button():

    # For pt. 2, the conjunction module that feeds into 'rx' has multiple inputs. We need to mark those down so we can monitor them for cycles
    # For 'rx' to receive a low signal, then rx_source needs to have received all high signals from its inputs. Let's track when each of the inputs emits a high signal.
    if rx_source:
        cycles = {}
        rx_source_inputs = modules[rx_source][1]

    # Trackers
    high_pulses = 0
    low_pulses = 0
    counter = 0

    # Continue until we reach a stopping condition
    while True:

        # Handle pt. 1. If our input doesn't have an 'rx' output, stop here.
        if counter == 1000:
            print(f'There were {high_pulses} high pulses and {low_pulses} low pulses, for a total product of: {high_pulses * low_pulses}')
            if not rx_source:
                print("There is no 'rx' output, so pt. 2 is non-applicable")
                return

        # Iterate counter, start with a low signal in the broadcast module
        counter += 1
        queue = [(None, 'broadcaster', 'L')]

        # Keep going until all signals have been handled
        while len(queue) > 0:

            source, label, power = queue.pop(0)
            if power == 'H':
                high_pulses += 1
            else:
                low_pulses += 1
            
            # Some labels that get signals aren't modules, so we don't need to do anything with them
            if label not in modules:
                continue

            # Handle the broadcaster signal
            if label == 'broadcaster':
                for destination in modules[label]:
                    queue.append((label, destination, power))
                continue

            # Handle flip-flop modules
            if modules[label][0] == '%' and power == 'L':
                modules[label][1] = not modules[label][1]
                for destination in modules[label][2]:
                    queue.append((label, destination, 'H' if modules[label][1] else 'L'))

            # Handle conjunction modules
            elif modules[label][0] == '&':
                modules[label][1][source] = power
                pulse = 'L' if all(memory == 'H' for memory in modules[label][1].values()) else 'H'
                for destination in modules[label][2]:
                    queue.append((label, destination, pulse))

                # If one of the key conjunctions modules for pt. 2 outputs a high signal, track the number of button presses it took. This is the cycle length.
                # Thankfully, like Day 8, the cycle is simple and starts immediately.
                if rx_source and label in rx_source_inputs and pulse == 'H':
                    if label not in cycles:
                        cycles[label] = counter

                        # If we've identified all of the key conjunction modules' cycle lengths, find their LCM and report it for pt. 2 and end calculations
                        if len(cycles) == len(rx_source_inputs):
                            print("The number of button presses it takes for the 'rx' module to receive a low signal is:", lcm(*cycles.values()))
                            return

press_button()