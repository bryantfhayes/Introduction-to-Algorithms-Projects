import sys, os
from optparse import OptionParser
from time import time

# Set recursion depth to one million
sys.setrecursionlimit(40000)

# Setup the option parser for choosing the algorithm
parser = OptionParser()

parser.add_option("-a", "--algorithm", dest="algorithm", help="Choose which algorithm to execute")

parser.add_option("-f", "--file", dest="filename", help="Enter input file name")

parser.add_option("-t", "--time", action="store_true", dest="time",
    default=False, help="Get time it takes to run each algorithm run")

parser.add_option("-d", "--demo", dest="demo",
    default=False, help="Run test cases A = 2000, 2100, 2200, ... 3000. 1)[1,5,25,50]...2)[1,3,4,17,31]")

(options, args) = parser.parse_args()

# ERROR CHECK --------------------------------------
if not options.filename:   # if filename is not given
  parser.error('Filename not given')
# --------------------------------------------------

# Global Variables
V  = []     # Current V value
A  = 0     # Current A value
Vq = []    # Queue for V values
Aq = []    # Queue for A values
Iq = 0     # Global index for V/A Queue
C  = []    # Optimal Array for changedp
Cv = []    # Value of last subtracted V[i] for idx i
numberOfSets = 0 # The number of sets to run through

# Execute the change slow algorithm which runs in exponential time
def executeChangeSlow():
  global V, A
  # Make sure V[] and A are ready at this point
  solution = []
  t0 = time()
  solution = changeSlow(V, A)
  t1 = time()
  if options.time:
    print "TIME = %lf" % (t1-t0)
  
  print "The solution is: " + str(solution)
  print "Total number of coins: " + str(solutionCoinSum(solution))
  return (solution, solutionCoinSum(solution))

# Takes in a list and sums each i*solution[i]
def solutionCoinSum(solution):
  sum = 0
  for val in solution:
    sum += val
  return sum

# The actual changeSlow algorithm is here
def changeSlow(V, k):
  # V = The list containing coin values
  # A = The value we are trying to make using various coins
  numberOfUniqueCoins = len(V)
  localSolution = []
  
  # Base Case:
  for i in xrange(0, numberOfUniqueCoins):
    if V[i] == k:
      # Create a list of size "numberOfUniqueCoins"
      localSolution = [0] * numberOfUniqueCoins
      localSolution[i] = 1
      return localSolution
  
  # Otherwise:
  localSolution = [0] * numberOfUniqueCoins
  # Replace sys.maxint with sys.maxsize in Python v3.0
  minimumNumberOfCoins = sys.maxint
  for i in xrange(1, k/2+1):
    localSolution1 = changeSlow(V, i)
    localSolution2 = changeSlow(V, k-i)
    latestCoinCount = calculateCoinCount(localSolution1, localSolution2)
    if latestCoinCount < minimumNumberOfCoins:
      minimumNumberOfCoins = latestCoinCount
      localSolution = sumBothSolutions(localSolution1, localSolution2)
  return localSolution

# UTILITY_METHOD
# Iterate through two arrays and find the sum of all the values.
def calculateCoinCount(a, b):
  coinCount = 0
  for x in a:
    coinCount += x
  for x in b:
    coinCount += x
  return coinCount

# UTILITY_METHOD
# Input two solutions of equal length and merge them into a single list. 
def sumBothSolutions(a, b):
  newSolution = [0] * len(a)
  for i in xrange(0, len(a)):
    newSolution[i] = a[i] + b[i]
  return newSolution

def testCase():
  global Vq, Aq, numberOfSets
  for i in xrange(0,11):
    numberOfSets += 1
    if options.demo == '1':
      tempV = [1, 10, 25, 50]
      tempA = 2000 + (100*i)
    elif options.demo == '2':
      tempV = [1, 3, 4, 17, 31]
      tempA = 2000 + (100*i)
    Vq.append(tempV)
    Aq.append(tempA)
    print tempV, tempA
# Sets the global variables Vq and Aq from the input file
# This creates the queue of sets to analyze
def loadInputFile(filename):
  global Vq, Aq, numberOfSets
  with open(filename) as f:
    lines = f.readlines()
  for i in xrange(0, len(lines), 2):
    numberOfSets += 1
    tempV = lines[i].strip('\n')[1:-1]
    tempV = map(int, tempV.split(','))
    tempA = int(lines[i+1].strip('\n'))
    Vq.append(tempV)
    Aq.append(tempA)

# loadInputFile() creates a queue of sets, this acts as a FIFO list
# where this function returns the latest set.
def getNextSetFromQueue():
  global Vq, Aq, Iq
  curr = (Vq[Iq], Aq[Iq])
  Iq += 1
  return curr

# Save output to a text file.
def saveOutput(filename, solution, m):
  f = open(filename[:-4] + "change.txt",'a')
  f.write(str(solution))
  f.write('\n')
  f.write(str(m))
  f.write('\n')
  f.close()

# Call this function to launch the greedy algorithm to find a solution
# on V[] and A given as global variables.
def executeChangeGreedy():
  global V, A
  # Make sure V[] and A are ready at this point
  solution = []
  t0 = time()
  solution = changeGreedy(V, A)
  t1 = time()
  if options.time:
    print "TIME = %lf" % (t1-t0)
  
  print "The solution is: " + str(solution)
  print "Total number of coins: " + str(solutionCoinSum(solution))
  return (solution, solutionCoinSum(solution))

# The greed algorithm. I believe it has an asymptotic runtime of O(V*k)
def changeGreedy(V, k):
  localSolution = [0] * len(V)
  for i in xrange(len(V)-1, -1, -1):
    if V[i] <= k:
      localSolution[i] = 1
      k -= V[i]
      break
  # Check for Base Case
  if k == 0:
    return localSolution
  # Otherwise, recurse further
  else:
    remainingSolution = changeGreedy(V, k)
    return sumBothSolutions(localSolution, remainingSolution)

# The actualy changedp algorithm is here
def changedp(V, k):
  global Cv
  coins = []
  tempCv = []
  if k == 0:
    return 0
  for i in xrange(0, len(V)):
    if V[i] <= k:
      if C[k - V[i]] < sys.maxint:
        coins.append(C[k - V[i]])
        tempCv.append(V[i])
      
  minCoin = min(coins)
  for i in xrange(0, len(coins)):
    if coins[i] == minCoin:
      minCoinIdx = i
      break
  Cv[k] += tempCv[minCoinIdx]

  return 1 + minCoin

# Kicks off the changedp algoithm (Dynamic Programming Method)
def executeChangedp():
  global V, A, C, Cv
  # Make sure V[] and A are ready at this point
  solution = [0] * len(V)
  C = [sys.maxint] * (A+1)
  Cv = [0] * (A+1)
  # Calculate every value in C[] from the bottom-up.
  # This allows you to use previous values to find future values.
  t0 = time()
  for i in xrange(0, A+1):
    C[i] = changedp(V, i)
    #print "%d = %d" % (i, C[i])
  j = A
  while j > 0:
    for w in xrange(0, len(V)):
      if Cv[j] == V[w]:
        solution[w] += 1
        j -= V[w]
  t1 = time()

  if options.time:
    print "TIME = %lf" % (t1-t0)

  print "The solution is: " + str(solution)
  print "Total number of coins: " + str(C[A])
  return (solution, C[A])

# MAIN
def main():
  global numberOfSets, V, A

  # Variables
  solution = []
  m = 0

  # Create Vq and Aq queue
  if options.demo == '1' or options.demo == '2':
    testCase()
    print "TEST"
  else:
    loadInputFile(options.filename)
  
  if os.path.isfile(options.filename[:-4] + "change.txt"):
    os.system("rm " + options.filename[:-4] + "change.txt")

  for i in xrange(0, numberOfSets):
    #print getNextSetFromQueue()
    (V, A) = getNextSetFromQueue()
    # Algorithm Call
    if options.algorithm == 'a':
      (solution, m) = executeChangeSlow()
      saveOutput(options.filename, solution, m)
      (solution, m) = executeChangeGreedy()
      saveOutput(options.filename, solution, m)
      (solution, m) = executeChangedp()
    elif options.algorithm == '1':
      (solution, m) = executeChangeSlow()
    elif options.algorithm == '2':
      (solution, m) = executeChangeGreedy()
    elif options.algorithm == '3':
      (solution, m) = executeChangedp()
    else:
      print "No algorithm selected. Quitting..."
      exit(1)

    # Output solution to file
    saveOutput(options.filename, solution, m)

if __name__ == "__main__":
  main()
