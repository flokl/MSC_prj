import csv
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class DecisionNode():
    action: str
    count: int
    nextActions: list


def readCSV(stringOfCSV):
    """
    reads CSV file and returns a list of lists
    :param stringOfCSV: 
    :return: list of lists
    """
    with open(stringOfCSV, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    allElementsWithHierarchy = list()
    for entry in data:
        allElementsWithHierarchy.append(entry[0].split(';'))
    return allElementsWithHierarchy


def getRelevantItemsFromList(data, expectedFeatures, percentageOfRelevantData):  # takes all items and returns the relevant ones
    """
    Gets all Elements and searches for the labels that are most likely features.
    :param data: all elements as list
    :param expectedFeatures: Determines how many features are expected
    :param percentageOfRelevantData: Start point of percentage in how many scenarios a feature should be expected
    :return: extracted relevant features
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
    """
    inputs raw list of lists and relevant features and cleans non relevant features out of the structure
    :param data: list of lists
    :param features: relevant features
    :return: cleaned structure with only relevant features
    """
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


def next_probable_paths_list(decision_tree, completed_actions=[], depth=0):
    """
    Create a sorted list of possible paths with their corresponding probabilities.
    :param decision_tree: complete decision tree
    :param completed_actions: actions after which the tree list starts
    :param depth: unused
    :return: sorted list of action paths and probabilities
    """
    action_path_node_list = probability_paths_tree(decision_tree, completed_actions)
    probable_path_list = dict()
    for action_path_node in action_path_node_list:
        probable_path_list[action_path_node.action] = action_path_node.probability
    return dict(sorted(probable_path_list.items(), key=lambda x: x[1], reverse=True))


@dataclass
class ActionPathNode():
    action: str
    probability: Decimal


def probability_paths_tree(decision_tree, completed_actions=[]):
    """
    Traverse the tree until the starting point (after all completed_actions) is reached.
    From this new starting point traverse each path until a leave is reached and
    save the path of actions taken with the corresponding probabilities.
    :param decision_tree: the complete decision tree of possible actions
    :param completed_actions: the actions already completed and the starting point of the foreshadowing
    :return: a list of nodes with the corresponding probabilities
    """

    # Go to right position in tree
    if completed_actions:
        return probability_paths_tree(decision_tree[completed_actions[0]].nextActions, completed_actions[1:])

    if not decision_tree:
        ActionPathNode.action = ""
        ActionPathNode.probability = 1
        return [ActionPathNode]

    sum = 0
    for action in decision_tree:
        sum += decision_tree[action].count

    next_action_path_list = list()
    for action in decision_tree:
        next_action_path_node_list = probability_paths_tree(decision_tree[action].nextActions)
        for next_action_path in next_action_path_node_list:
            action_path_node = ActionPathNode('', -1)
            action_path_node.action = decision_tree[action].action + "," + next_action_path.action
            probability = decision_tree[action].count / sum
            action_path_node.probability = probability * next_action_path.probability
            next_action_path_list.append(action_path_node)
    return next_action_path_list


csvPath = '../data_gen/scenario_data.csv'
dataAsListofList = readCSV(csvPath)
relevantItems = getRelevantItemsFromList(dataAsListofList, 8, 20)
# print(relevantItems)
cleanData = newDTStructure(dataAsListofList, relevantItems)
dt = decision_tree(cleanData)
probabilities = next_probable_action(['report', 'open'], dt)
print(probabilities)
# delete 10, open 12, forward 10, ignore 8
next_paths = next_probable_paths_list(dt, ['report', 'open', 'forward'])
print(next_paths)
