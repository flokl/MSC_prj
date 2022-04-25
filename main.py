#!/usr/bin/env python
import json
import random

SCENARIOS_OUTPUT_FILE = "scenario_data.csv"

SCENARIOS = [
    "phishingmail_entries.json",
    "usbpackage_entries.json",
    "softwareinstall_entries.json"
]


def main():
    actions = []

    for i in range(1000):
        actions = gen_data(SCENARIOS[0])
        random_data = gen_random_data(len(actions[len(actions) - 1]))
        data.append(mix_log_data(actions, random_data, int(len(random_data) * 0.8), 100))

    write_csv(SCENARIOS_OUTPUT_FILE, data)


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


def gen_random_data(amount: int) -> list:
    """
    Generates random log data
    :param amount: amount of entries
    :return: list of length size
    """
    random_data = []

    for i in range(0, amount):
        random_data.append("randomevent" + str(random.randint(0, 1000)))

    return random_data


def mix_log_data(log_data1: list, log_data2: list, max_entries_between: int, probability_between: int) -> list:
    """
    Mixes log_data2 into log_data1. First line data from log_data1 gets mixed with a random line from log_data2.
    At maximum max_entries_between get mixed in between two entries of log_data1.
    :param log_data1: Log data with generated actions
    :param log_data2: Log with unrelated data
    :param max_entries_between: Maximum new entries between two entries from log_data1.
    :param probability_between: Probability at which entries get mixed between two entries from log_data1.
    :return: list of mixed log_data
    """

    log_data_mixed = []

    for item_data1 in log_data1:
        if random.randrange(0, 99, 1) < probability_between:
            amount = random.randrange(0, max_entries_between, 1)
            log_data_mixed += ([item_data1] + log_data2[:amount])
            # Remove mixed entries from list
            [log_data2.pop(0) for i in log_data2[:amount]]
        else:
            log_data_mixed += [item_data1]

    # Append remaining entries
    # log_data_mixed += log_data2

    return log_data_mixed


def write_csv(filename: str, data: list) -> None:

    with open(filename, 'w') as output_file:
        for line in data:
            output_file.write(';'.join(line))
            output_file.write('\n')


if __name__ == "__main__":
    main()
