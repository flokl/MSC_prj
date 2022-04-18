#!/usr/bin/env python
import json
import random

SCENARIOS_OUTPUT_FILE = "scenario_data.csv"
TRASH_ENTRY_FILE = "trash_entries.txt"

PHISHINGMAIL_SCENARIO = "phishingmail_entries.json"
USBPACKAGE_SCENARIO = "usbpackage_entries.json"
SOFTWAREINSTALL_SCENARIO = "softwareinstall_entries.json"


def main():
    actions = []

    for i in range(1000):
        actions.append(gen_data(PHISHINGMAIL_SCENARIO))
    write_csv(SCENARIOS_OUTPUT_FILE, actions)


def gen_data(json_file_name):
    with open(json_file_name, "r") as jsonfile:
        data = json.load(jsonfile)

        entry = 'START'
        previous_entry = entry

        if '*' not in data:
            data['*'] = ''
        # Static copy
        always_possible = data['*'][:]

        actions = []

        while 'END' not in data[entry]:

            if 'PREVIOUS' in data[entry]:
                next_entries = data[previous_entry]
            else:
                next_entries = data[entry]

            # Remove used actions
            if entry in always_possible:
                always_possible.remove(entry)

            # Add leftover action
            next_entries += always_possible

            # Unique options
            next_entries = list(set(next_entries))

            # Remove current from options
            if entry in next_entries:
                next_entries.remove(entry)

            next_entry_index = random.randrange(0, len(next_entries), 1)
            next_entry = next_entries[next_entry_index]

            if entry not in data['*']:
                previous_entry = entry
            entry = next_entry
            actions.append(entry)

        return actions


def read_txt(filename):
    data = []
    with open(filename, 'r') as input_file:
        data.append(input_file.readline())
    return data


def write_csv(filename, data):
    with open(filename, 'w') as output_file:
        for line in data:
            output_file.write(';'.join(line))
            output_file.write('\n')


if __name__ == "__main__":
    main()
