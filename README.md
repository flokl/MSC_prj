# MSC_prj
## Generating test data
To generate test data that can later be used to fill the behaviour model there is a separate program in `data_gen/scenarios/main.py`. This script can be started with a few arguments:
- -s (--scenarios) to input scenario (as JSON) data as a directed graph (default is phishingmail_entries)
- -n (--amountoflogs) to define number of scenario logs that should be generated (default 1000)
- -b (--maxbetween) to define max amount of random data getting mixed in between two relevant data points
- --maxbetweenpercentage define max amount (as a percentage of total amount) of random data getting mixed in between data points (default 80%)
- -p (--mixprobability) define probability random data gets mixed in between two data points (default 100%)
- -o (--outfile) define the output file of the generated data (default is scenario_data.csv) The csv file is semicolon separated.

The JSON file contains the description of a directed graph that describes the scenario (can be defined with argument -s). Every line should contain an argument that can be executed and which arguments can be executed after the current argument has been executed. For example the line:
`"open": ["check sender", "download attachment"]`
Describes that after the element has been opened that it is possible that the sender is checked or that the attachment is downloaded. If there is an endpoint after an action this can be marked with `[“END“]`. To define the initial possibilities the `“START”` tag must be used. To define actions that can be executed in every situation (except the previous action has the end tag) the `“*” `tag can be used.

The program will first create log data and then generates the csv output file from the generated logs.

## Creation of behaviour profile
The main program can be found under `data_gen/decision_algorithm/decision_main.py` and starts without arguments.

### Read CSV:
After the start of the program, it is possible to enter the path to the csv. The default value will be printed and can be selected with `ENTER`.

### Define search parameters:
The next options are that it is possible to define how many features are expected and in how many lines of the csv files each of these features is expected. This value will be defined in percent. There are also default values defined which can be selected with `ENTER`. These values are not fixed, and the program will dynamically adapt the values for best results, nevertheless with values that are near the results the processing time can be minimized.

After the search has been done the program will output which parameters it used to create the decision tree.

### Input taken steps:
It is now possible to input steps that have already been taken by the user. This enables the possibility that the decision tree can overtake the prediction in every phase.
First the program asks for input on how many steps have been taken. If one or more steps have been pre given a list with possible actions will appear and a step can be selected by typing the number next to the action. The program will ask for input until every pre given step defined before is filled with an action.

### Results:
The program will now output the most possible next steps predicted in descending order with the probability value.

Additionally, it can be selected how many paths should be printed.
A path is not only the probable next step, it defines what are the most probable actions in a row until an endpoint. The most probable paths will also output in descending order and contain all actions until an endpoint separated with a comma.
