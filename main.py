#!/usr/bin/env python

OUTPUT_FILE = "scenario_data.csv"
TRASH_ENTRY_FILE = "trash_entries.txt"
PHISHINGMAIL_ENTRY_FILE = "phishingmail_entries.json"


def main():
    pass

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
