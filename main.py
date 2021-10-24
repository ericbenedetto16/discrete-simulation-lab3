import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# Simulation Parameters
timeSteps = 1000
a = 0.1
b = 0.6
startingState = 2
transitionMatrix = np.array([[1-a, a],[b, 1 - a - b, a],[b, 1 - b]], dtype=object) # State 2, 1, 0
stateMovements = np.array([[0, -1], [1, 0, -1], [1, 0]], dtype=object) # State 2, 1, 0

# State Variables
X = startingState
prevState = X
randomNum = -1

# Counter
events = list()
lengthOfRenewals = list()
numRenewals = 0
timeBetweenFailures = list()
lastFailure = 0
numFailures = 0
timeBetweenCatastrophes = list()
lastCatastrophy = 0
downTime = 0
stateOverTime = dict()
stateOverTime[0] = X

# Simulation Loop
for i in range(1, timeSteps):
    prevState = X
    
    randomNum = random.choices(stateMovements[abs(X - startingState)], weights=transitionMatrix[abs(X - startingState)])
    X += randomNum[0]

    stateOverTime[i] = X

    # We Now Have Less Servers than the Previous Timestep
    fail = X < prevState
    if fail:
        timeBetweenFailures.append(i - lastFailure)
        lastFailure = i
        numFailures += 1

    if X == 0:
        timeBetweenCatastrophes.append(i - lastCatastrophy)
        lastCatastrophy = i

    # If We Now Have More Servers than the Previous Timestep
    if X > prevState:
        lengthOfRenewals.append(i - lastFailure)
        numRenewals += 1

    # If We Still have Any Servers Down
    if prevState < startingState:
        downTime += 1 

    events.append({"Time": i, "PrevState": prevState, "CurrState": X, "Success/Failure": "Success" if not fail else "Fail"})

# Report Generator
df = pd.DataFrame(events)
print(df)

failureRate = round(numFailures / timeSteps, 2)
renewRate = round(numRenewals / downTime, 2)

print(f"Failure Rate: {round(numFailures / timeSteps, 2)}")
print(f"Renewal Rate: {round(numRenewals / downTime, 2)}")
print(f"Average Lifetime of a Server: {np.mean(timeBetweenFailures)}")
print(f"Average Downtime of a Server: {np.mean(lengthOfRenewals)}")
print(f"MTTF for System: {np.mean(timeBetweenCatastrophes)}")

plt.title("State Over Time")
plt.hlines(stateOverTime.values(), stateOverTime.keys(), [key + 1 for key in stateOverTime.keys()])
plt.yticks(np.arange(0, len(transitionMatrix[0]) + 1))

plt.show()