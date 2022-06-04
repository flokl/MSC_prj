import csv
from dataclasses import dataclass


@dataclass
class DecisionNode():
    action: str
    count: int
    nextActions: list


def readCSV(stringOfCSV):  # reads CSV and Puts every line in a list and returns list of list
    with open(stringOfCSV, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    allElementsWithHierarchy = list()
    for i in data:
        allElementsWithHierarchy.append(i[0].split(';'))
    return allElementsWithHierarchy


def getRelevantItemsFromList(data, percentageOfRelevantData):  # takes all items and returns the relevant ones
    allElements = [item for sublist in data for item in sublist]
    singleElements = list(dict.fromkeys(allElements))
    relevantItems = list()
    for i in singleElements:
        count = allElements.count(i)
        if count >= len(data) * (percentageOfRelevantData / 100):
            relevantItems.append(i)
    return relevantItems


def newDTStructure(data, features):
    cleanStructure = list()
    for i in data:
        helpListEntry = list()
        for j in i:
            if features.count(j) > 0:
                helpListEntry.append(j)
        cleanStructure.append(helpListEntry)
    return cleanStructure


def decision_tree(data):
    """
    Build a tree out of a 2d array
    :param data: 2d array of actions
    :return: trees structure of DecisionNode's
    """

    action_list = dict()

    for action_entries_list in data:
        action_list = build_depth(action_entries_list, action_list)

    return action_list


def build_depth(action_entries_list, action_list=dict()):
    """
    Traverse a single scenario line into the deep until the last action and build the DecisionNode's
    :param action_entries_list: scenario line with actions
    :param action_list: DecisionNode action list
    :return: DecisionNode action list
    """

    if not action_entries_list:
        return

    if action_entries_list[0] in action_list:
        action_list[action_entries_list[0]].count += 1
    else:
        action_list[action_entries_list[0]] = DecisionNode(action_entries_list[0], 1, dict())

    build_depth(action_entries_list[1:], action_list[action_entries_list[0]].nextActions)
    return action_list


csvPath = '../data_gen/scenario_data.csv'
dataAsListofList = readCSV(csvPath)
relevantItems = getRelevantItemsFromList(dataAsListofList, 10)
# print(relevantItems)
cleanData = newDTStructure(dataAsListofList, relevantItems)
dt = decision_tree(cleanData)
