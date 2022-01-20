import sys

#function for splitting the arguments into chunks of 3 for the action results
def argsSplit(list): 
    for i in range(0,len(list),3):
        yield list[i:i+3]

#class that stores data from .in file, compiling it for a given state
class state:
    def __init__(self, stateInfo):
        self.stateName = stateInfo[0]
        self.reward = float(stateInfo[1])
        self.actions = []
        x = stateInfo[2:]
        y = list(argsSplit(x)) 
        d = {} #dictionary for actions (not results)
        for act in y:
            actNum = act[0]
            if actNum not in d: 
                d[actNum] = []
            d[actNum].append(act)
        for p in d:
            a = action(d[p])
            self.actions.append(a)
        self.jValue = self.reward

#class that stores the probabilities to going to each state given the action     
class action: #lawsuit
    def __init__(self, actionInfo):
        self.outcomes = actionInfo

#start of main
if len(sys.argv) != 5:
    print("Error: requires exactly four arguments: first the number of states in the MDP, second the number of possible actions, third the .in file, and last the discount factor")
    sys.exit(1) 

statesNum = sys.argv[1]
actionsNum = sys.argv[2]
discountFactor = float(sys.argv[4])
trainingData = []

with open(sys.argv[3], 'r') as trainData:
    extractTrainData = trainData.readlines()
    for d in extractTrainData:
        data = d.split()
        for index, da in enumerate(data):
            da = da.replace('(','').replace(')','') #remove paranthesis from info
            data[index] = da
        trainingData.append(data)

states = []
dictStates = {} #dictionary for directly connecting the state number (ex: s1) and the state class

for d in trainingData:
    s = state(d)
    dictStates[s.stateName] = s
    states.append(s)


#for printing possible actions
#for s in states:
#   for a in s.actions:
#        print(a.outcomes)

finalJValues = [] #final j values after an iteration, change all states to have their respective j values
print("After iteration 1:")
for s in states:
    correctAct = ""
    jValues = []
    for arg in s.actions:
        j = s.reward
        pastJs = 0
        for a in arg.outcomes:
            chance = float(a[2])
            actionValue = dictStates[a[1]].jValue #j value at state s for action
            j = j + discountFactor*actionValue*chance
        jValues.append(j)
    correctAct = s.actions[jValues.index(max(jValues))].outcomes[0][0]
    finalJValues.append(jValues[jValues.index(max(jValues))])
    print("(" + s.stateName + " " + correctAct + " " + '{0:.4f}'.format(s.jValue) + ")", end = " ")

print()

for i,s in enumerate(states):
   s.jValue = finalJValues[i]
finalJValues = []


for x in range(2, 21):
    print("After iteration " + str(x) + ": ")
    for s in states:
        correctAct = ""
        jValues = []
        for arg in s.actions:
            j = s.reward
            pastJs = 0
            for a in arg.outcomes:
                chance = float(a[2])
                actionValue = dictStates[a[1]].jValue #j value at state s for action
                j = j + discountFactor*actionValue*chance
            jValues.append(j)
        correctAct = s.actions[jValues.index(max(jValues))].outcomes[0][0]
        finalJValues.append(jValues[jValues.index(max(jValues))])
        print("(" + s.stateName + " " + correctAct + " " + '{0:.4f}'.format(s.jValue) + ")", end = " ")
    print()

    for i,s in enumerate(states):
        s.jValue = finalJValues[i]
    finalJValues = []