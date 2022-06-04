
import csv

def readCSV(stringOfCSV): # reads CSV and Puts every line in a list and returns list of list
    with open(stringOfCSV, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data

def getRelevantItemsFromList(data): #takes all items and returns the relevant ones
    allElementsWithHierarchy = list()
    for i in data:
        allElementsWithHierarchy.append(i[0].split(';'))
    allElements = [item for sublist in allElementsWithHierarchy for item in sublist]
    singleElements = list(dict.fromkeys(allElements))
    relevantItems = list()
    for i in singleElements:
        count = allElements.count(i)
        if count >= len(allElementsWithHierarchy) / 10:
            relevantItems.append(i)
    return relevantItems

csvPath='../data_gen/scenario_data.csv'
dataAsListofList=readCSV(csvPath)
relevantItems=getRelevantItemsFromList(dataAsListofList)
print(relevantItems)