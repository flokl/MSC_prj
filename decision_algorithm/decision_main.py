import csv
import sys
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class DecisionNode:
    action: str
    count: int
    nextActions: list


@dataclass
class ActionPathNode:
    action: str
    probability: Decimal


def main() -> None:
    pre_defined_features = 9
    pre_defined_percentage = 20
    pre_defined_print_path_entries = 10
    pre_defined_csv_path = '../data_gen/scenario_data.csv'

    try:
        data_as_list_of_list = read_csv(define_csv_path(pre_defined_csv_path))
    except:
        print("An error occurred. Please check configuration and restart program")
        sys.exit()

    target_features = choose_amount_of_features(pre_defined_features)
    target_percentage = choose_amount_of_percentage(pre_defined_percentage)
    print(
        "It will be searched for %d Features with a percentage of %d percent. It is possible that depending on the data "
        "and the %% more or less features will be found \n Processing...\n" % (target_features, target_percentage))
    relevant_items = get_relevant_items_from_list(data_as_list_of_list, target_features, target_percentage)
    next_steps = determine_next_steps(relevant_items)
    cleanData = new_dt_structure(data_as_list_of_list, relevant_items)
    dt = decision_tree(cleanData)
    probabilities = next_probable_action(next_steps, dt)
    next_paths = next_probable_paths_list(dt, next_steps)
    print_next_actions_and_paths(probabilities, next_paths, pre_defined_print_path_entries)


def get_percentage(input_float):
    """
    :param input_float: inputs float value
    :return: float value multiplied by 100
    """
    return input_float * 100


def define_csv_path(input_pre_defined_csv_path):
    """
    Asks user which csv file should be opened
    :param input_pre_defined_csv_path: pre defined csv
    :return: path to user demanded csv file
    """
    input_bool = False
    while not input_bool:
        custom_path = input(
            "Please enter the path to the csv file you want to analyse. If no input is entered the default file %s "
            "will be used [ENTER]\n" % input_pre_defined_csv_path)
        if custom_path == "":
            return input_pre_defined_csv_path
        else:
            try:
                read_csv(custom_path)
                return custom_path
            except:
                print("An error occurred, please try again")


def read_csv(string_of_csv):
    """
    reads CSV file and returns a list of lists
    :param string_of_csv:
    :return: list of lists
    """
    with open(string_of_csv, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    all_elements_with_hierarchy = list()
    for entry in data:
        all_elements_with_hierarchy.append(entry[0].split(';'))
    return all_elements_with_hierarchy


def get_relevant_items_from_list(data, expected_features,
                                 percentage_of_relevant_data):  # takes all items and returns the relevant ones
    """
    Gets all Elements and searches for the labels that are most likely features. To create a decision tree the
    percentage has to be over 2%
    :param data: all elements as list
    :param expected_features: Determines how many features are expected
    :param percentage_of_relevant_data: Start point of percentage in how many scenarios a feature should be expected
    :return: extracted relevant features
    """
    if percentage_of_relevant_data <= 2:
        expected_features -= 1
        percentage_of_relevant_data = 100
    all_elements = [item for sublist in data for item in sublist]
    single_elements = list(dict.fromkeys(all_elements))
    relevant_items = list()
    for i in single_elements:
        count = all_elements.count(i)
        if count >= len(data) * (percentage_of_relevant_data / 100):
            relevant_items.append(i)
    if len(relevant_items) < expected_features and percentage_of_relevant_data > 1:
        relevant_items = get_relevant_items_from_list(data, expected_features, percentage_of_relevant_data - 1)
    else:
        print("Found %d Features. With a relevance of %d %%" % (len(relevant_items),
                                                                percentage_of_relevant_data))
    return relevant_items


def print_relevant_items(relevant_items_to_print):
    """
    Outputs the found relevant items
    :param relevant_items_to_print: list of relevant items
    :return: NULL
    """
    counter = 1
    for feature in relevant_items_to_print:
        print("%d: %s" % (counter, feature))
        counter += 1


def new_dt_structure(data, features):
    """
    inputs raw list of lists and relevant features and cleans non relevant features out of the structure
    :param data: list of lists
    :param features: relevant features
    :return: cleaned structure with only relevant features
    """
    clean_structure = list()
    for i in data:
        help_list_entry = list()
        for j in i:
            if features.count(j) > 0:
                help_list_entry.append(j)
        if help_list_entry:
            clean_structure.append(help_list_entry)
    return clean_structure


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


def next_probable_action(completed_actions, decision_tree_used):
    """
    Extract the probabilities of the next possible actions based on the previous actions
    :param completed_actions: actions performed previously
    :param decision_tree_used: the complete decision tree
    :return: actions with probabilities
    """
    if not completed_actions:
        probabilities = dict()
        sum = 0
        for action in decision_tree_used:
            sum += decision_tree_used[action].count
        for action in decision_tree_used:
            probabilities[decision_tree_used[action].action] = decision_tree_used[action].count / sum
        return probabilities
    try:
        return next_probable_action(completed_actions[1:], decision_tree_used[completed_actions[0]].nextActions)
    except:
        print("No probable actions were found")
        sys.exit()


def next_probable_paths_list(decision_tree_used, completed_actions=[], depth=0):
    """
    Create a sorted list of possible paths with their corresponding probabilities.
    :param decision_tree_used: complete decision tree
    :param completed_actions: actions after which the tree list starts
    :param depth: unused
    :return: sorted list of action paths and probabilities
    """
    action_path_node_list = probability_paths_tree(decision_tree_used, completed_actions)
    probable_path_list = dict()
    for action_path_node in action_path_node_list:
        probable_path_list[action_path_node.action] = action_path_node.probability
    try:
        return dict(sorted(probable_path_list.items(), key=lambda x: x[1], reverse=True))
    except:
        print("No probable paths were found")
        sys.exit()


def check_user_input(expected_int):
    """
    checks if user has inputed int value
    :param expected_int: input of user
    :return: returns 0 if user has typed in no positive int, otherwise returns the typed in int
    """
    try:
        val = int(expected_int)
        return val
    except ValueError:
        return 0


def probability_paths_tree(decision_tree_used, completed_actions=[]):
    """
    Traverse the tree until the starting point (after all completed_actions) is reached.
    From this new starting point traverse each path until a leave is reached and
    save the path of actions taken with the corresponding probabilities.
    :param decision_tree_used: the complete decision tree of possible actions
    :param completed_actions: the actions already completed and the starting point of the foreshadowing
    :return: a list of nodes with the corresponding probabilities
    """

    # Go to right position in tree
    if completed_actions:
        try:
            return probability_paths_tree(decision_tree_used[completed_actions[0]].nextActions, completed_actions[1:])
        except:
            print("No probable paths were found")
            sys.exit()

    if not decision_tree_used:
        ActionPathNode.action = ""
        ActionPathNode.probability = 1
        return [ActionPathNode]

    sum = 0
    for action in decision_tree_used:
        sum += decision_tree_used[action].count

    next_action_path_list = list()
    for action in decision_tree_used:
        next_action_path_node_list = probability_paths_tree(decision_tree_used[action].nextActions)
        for next_action_path in next_action_path_node_list:
            action_path_node = ActionPathNode('', -1)
            action_path_node.action = decision_tree_used[action].action + "," + next_action_path.action
            probability = decision_tree_used[action].count / sum
            action_path_node.probability = probability * next_action_path.probability
            next_action_path_list.append(action_path_node)
    try:
        return next_action_path_list
    except:
        print("No probable paths were found")
        sys.exit()


def choose_amount_of_features(count_of_pre_defined_features):
    """
    Asks user how many features are expected in the file
    :param count_of_pre_defined_features: pre defined amount of features
    :return: amount of features the file should be searched for
    """
    choose_features = input(
        "Please enter how much features you are expecting in the chosen file that will be relevant. Default of %d is "
        "used if non-valid or no input is entered [ENTER]\n" % count_of_pre_defined_features)
    if check_user_input(choose_features) > 0:
        return check_user_input(choose_features)
    else:
        return count_of_pre_defined_features


def choose_amount_of_percentage(percentage_of_pre_defined_percentage):
    """
    Asks user in what amount of rows the searched features should appear
    :param percentage_of_pre_defined_percentage: pre defined value
    :return: percentage of rows that should contain features
    """
    choose_percentage = input(
        "Please enter in %% how many rows you are expecting the features you want to extract (min 2%%, max 100%%). "
        "Default of %d is used if non-valid or no input is entered [ENTER]\n" % percentage_of_pre_defined_percentage)
    if 1 < check_user_input(choose_percentage) < 101:
        return check_user_input(choose_percentage)
    else:
        return percentage_of_pre_defined_percentage


def determine_next_steps(possible_steps):
    """
    Gets a list of possible steps that can be made. Asks user how many steps have already been made and fills list with that steps that have been made
    :param possible_steps: list of possible steps that can be made
    :return: list of steps that have already be made
    """
    count_of_next_steps = check_user_input(
        input("How many steps were already taken? Wrong inputs will be ignored.[ENTER]\n"))
    list_of_steps = list()
    for i in range(count_of_next_steps):
        print_relevant_items(possible_steps)
        input_number = check_user_input(
            input("Please choose %d. step that was already taken (Default: 1) [ENTER]\n" % (i + 1)))
        if 0 < input_number < len(possible_steps) + 1:
            list_of_steps.append(possible_steps[input_number - 1])
        else:
            list_of_steps.append(possible_steps[0])
    print("Steps that will be used as pre given:")
    counter = 1
    for item in list_of_steps:
        print("#%d: %s" % (counter, item))
        counter += 1
    return list_of_steps


def print_next_actions_and_paths(probabilities_to_print, paths_to_print, default_max_paths):
    """
    Sorts the next probabilities and prints them from high probability to low, then asks how many paths should be printed and prints the most probable paths depending on the input

    :param probabilities_to_print: dictionary with most probable next steps
    :param paths_to_print: dictionary with most probable next paths
    :param default_max_paths: default parameter of paths that should be printed
    :return: NULL
    """
    counter_probabilities = 1
    counter_paths = 1

    print("The %d most probable next steps are:" % len(probabilities_to_print))
    probabilities_sorted = sorted(probabilities_to_print, key=probabilities_to_print.get, reverse=True)
    for probable_entries in probabilities_sorted:
        print("#%d: %s with %.2f%% probability" % (
            counter_probabilities, probable_entries, get_percentage(probabilities_to_print.get(probable_entries))))
        counter_probabilities += 1

    max_amount = check_user_input(
        input("How many probable paths, of the %d found do you want to print? Wrong inputs are "
              "ignored (Default: %d) [ENTER]\n" % (len(paths_to_print), default_max_paths)))
    if (max_amount < 1):
        max_amount = default_max_paths
    if len(paths_to_print) < max_amount:
        print("The %d most probable paths are:" % len(paths_to_print))
    else:
        print("The %d most probable paths are:" % max_amount)
    for probable_paths in paths_to_print:
        print("#%d: %s with %.2f%% probability" % (
            counter_paths, probable_paths[:-1], get_percentage(paths_to_print.get(probable_paths))))
        counter_paths += 1
        if counter_paths > max_amount:
            return


if __name__ == "__main__":
    main()
