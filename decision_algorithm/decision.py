
import csv
from typing import NamedTuple

class DecisionNode(NamedTuple):
    count: int
    action: str
    nextActions: list


def readCSV(stringOfCSV): # reads CSV and Puts every line in a list and returns list of list
    with open(stringOfCSV, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    allElementsWithHierarchy = list()
    for i in data:
        allElementsWithHierarchy.append(i[0].split(';'))
    return allElementsWithHierarchy

def getRelevantItemsFromList(data, percentageOfRelevantData): #takes all items and returns the relevant ones
    allElements = [item for sublist in data for item in sublist]
    singleElements = list(dict.fromkeys(allElements))
    relevantItems = list()
    for i in singleElements:
        count = allElements.count(i)
        if count >= len(data) * (percentageOfRelevantData/100):
            relevantItems.append(i)
    return relevantItems

def newDTStructure(data,features):
    cleanStructure=list()
    for i in data:
        helpListEntry=list()
        for j in i:
            if features.count(j)>0:
                helpListEntry.append(j)
        cleanStructure.append(helpListEntry)
    return cleanStructure

def decisionTree(data,features):
   # depth=0
    #actionList=list()
    #for actionEntriesList in data:
     #   for actionEntries in actionEntriesList:
      #      actionList.append(DecisionNode())
   count=0;
   allcounts=list()
   #for feature in features:
   actionList = list()
   for actionEntries in data:
       if actionEntries[0] in actionList:
           actionList[actionEntries[0]] += 1
       else:
           actionList.append(actionEntries[0])
   print(actionList)

   return


csvPath='../data_gen/scenario_data.csv'
dataAsListofList=readCSV(csvPath)
relevantItems=getRelevantItemsFromList(dataAsListofList, 10)
print(relevantItems)
decisionTree(newDTStructure(dataAsListofList,relevantItems),relevantItems)



