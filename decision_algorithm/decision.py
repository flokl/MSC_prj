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


def getRelevantItemsFromList(data, expectedFeatures, percentageOfRelevantData):  # takes all items and returns the relevant ones
    """
    Gets all Elements and searches for the labels that are most likely features.
    :param data: all elements as list
    :param expectedFeatures: Determines how many features are expected
    :param percentageOfRelevantData: Start point of percentage in how many scenarios a feature should be expected
    :return:
    """
    if percentageOfRelevantData<1:
        expectedFeatures-=1
        percentageOfRelevantData=100
    allElements = [item for sublist in data for item in sublist]
    singleElements = list(dict.fromkeys(allElements))
    relevantItems = list()
    for i in singleElements:
        count = allElements.count(i)
        if count >= len(data) * (percentageOfRelevantData / 100):
            relevantItems.append(i)
    if len(relevantItems)<expectedFeatures:
        relevantItems=getRelevantItemsFromList(data, expectedFeatures, percentageOfRelevantData - 1)
    else:
        print("found %d Features. With a Relevance Percentage of %d " % (len(relevantItems), percentageOfRelevantData))
        for feature in relevantItems:
            print(feature)
    return relevantItems


def newDTStructure(data, features):
    cleanStructure = list()
    for i in data:
        helpListEntry = list()
        for j in i:
            if features.count(j) > 0:
                helpListEntry.append(j)
        if helpListEntry:
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


def next_probable_action(completed_actions, decision_tree):
    """
    Extract the probabilities of the next possible actions based on the previous actions
    :param completed_actions: actions performed previously
    :param decision_tree: the complete decision tree
    :return: actions with probabilities
    """
    if not completed_actions:
        probabilities = dict()
        sum = 0
        for action in decision_tree:
            sum += decision_tree[action].count
        for action in decision_tree:
            probabilities[decision_tree[action].action] = decision_tree[action].count / sum
        return probabilities
    return next_probable_action(completed_actions[1:], decision_tree[completed_actions[0]].nextActions)


csvPath = '../data_gen/scenario_data.csv'
dataAsListofList = readCSV(csvPath)
relevantItems = getRelevantItemsFromList(dataAsListofList, 8, 20)
# print(relevantItems)
cleanData = newDTStructure(dataAsListofList, relevantItems)
dt = decision_tree(cleanData)
probabilities = next_probable_action(['report', 'open'], dt)
print(probabilities)
# delete 10, open 12, forward 10, ignore 8
