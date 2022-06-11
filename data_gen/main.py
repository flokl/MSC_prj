#!/usr/bin/env python
import argparse
import datetime
import glob
import json
import os
import random

SCENARIO_PATH = 'scenarios/'
LOG_PATH = 'logs/'


def main() -> None:
    data = []

    parser = argparse.ArgumentParser(description='Generate log files.')
    parser.add_argument('-s', '--scenarios', dest='scenarios', nargs='+', default=['phishingmail_entries'],
                        help='scenario data as a directed graph')
    parser.add_argument('-n', '--amountoflogs', dest='amount', type=int, default=1000,
                        help='number of scenario logs that should be generated')
    parser.add_argument('-b', '--maxbetween', dest='max_entries_between', type=int, required=False,
                        help='max amount of random data getting mixed in between two data points')
    parser.add_argument('--maxbetweenpercentage', dest='max_entries_between_percentage', type=float, default=0.8,
                        help='max amount (as a percentage of total amount) of random data getting mixed in between '
                             'two data points')
    parser.add_argument('-p', '--mixprobability', dest='probability_between', type=float, default=100,
                        help='probability random data gets mixed in between two data points')
    parser.add_argument('-o', '--outfile', dest='output_file', type=str, default='scenario_data.csv',
                        help='the output file of the generated data')

    args = parser.parse_args()

    for i in range(args.amount):
        actions = gen_data(args.scenarios[random.randrange(0, len(args.scenarios), 1)])
        random_data = gen_random_data(len(actions[len(actions) - 1]))

        if args.max_entries_between:
            max_entries_between = args.max_entries_between
        else:
            max_entries_between = int(len(random_data) * args.max_entries_between_percentage)

        data.append(mix_log_data(actions, random_data, max_entries_between, args.probability_between))

    gen_log(data, LOG_PATH)

    # Data processing
    data_extracted = extract_from_log(LOG_PATH)
    write_csv(args.output_file, data_extracted)


def gen_data(json_file_name: str) -> list:
    """
    Generates log data based of a directed graph.
    :param json_file_name: Directed graph of possible actions
    :return: list of generated data
    """
    if not json_file_name.endswith('.json'):
        json_file_name += '.json'

    with open(SCENARIO_PATH + json_file_name, "r") as jsonfile:
        data = json.load(jsonfile)

        entry = 'START'
        previous_entry = entry
        # Clone list
        always_possible = data['*'][:] if '*' in data else list()

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

            if '*' in data and entry not in data['*']:
                previous_entry = entry

            entry = next_entry
            actions.append(entry)

        return actions


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
            # Remove mixed in entries from list
            [log_data2.pop(0) for i in log_data2[:amount]]
        else:
            log_data_mixed += [item_data1]

    # Append remaining entries
    # log_data_mixed += log_data2

    return log_data_mixed


def gen_log(data, path) -> None:
    """
    Generate logs out of the created data. One file corresponds to one scenario simulation.
    :param data: generated data
    :param path: path for the log files
    """

    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        files = glob.glob(path + '*')
        for f in files:
            os.remove(f)

    for line in data:

        delta_ms_30days = 1000 * 60 * 60 * 24 * 30
        delta_random_ms = random.randrange(0, delta_ms_30days, 1)
        logtime = datetime.datetime.now() - datetime.timedelta(milliseconds=delta_random_ms)

        with open(path + logtime.isoformat() + '.log', 'w+') as output_file:
            for entry in line:
                delta_ms_5min = 1000 * 60 * 5
                logtime += datetime.timedelta(milliseconds=random.randrange(0, delta_ms_5min, 1))
                output_file.write(logtime.isoformat() + '\t' + entry + '\n')


def extract_from_log(path) -> list(list()):
    """
    Extract all data from logs path without time
    :param path: path to the lgo files
    :return: 2d array, one line per log file
    """
    data = list()

    files = os.listdir(path)
    for file in files:
        with open(path + file, 'r') as input_file:
            scenario_data = list()
            for line in input_file:
                value = line.split('\t', 2)[1].strip()
                scenario_data.append(value)
        data.append(scenario_data)
    return data


def write_csv(filename: str, data: list) -> None:
    with open(filename, 'w+') as output_file:
        for line in data:
            output_file.write(';'.join(line))
            output_file.write('\n')


if __name__ == "__main__":
    main()
