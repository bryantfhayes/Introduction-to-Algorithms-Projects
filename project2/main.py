import sys
from optparse import OptionParser

# Setup the option parser for choosing the algorithm
parser = OptionParser()

parser.add_option("-a", "--algorithm", dest="algorithm", help="Choose which algorithm to execute", metavar="1.BruteForce, 2.Greedy, 3.Dynamic")

parser.add_option("-f", "--file", dest="filename", help="Enter input file name")

(options, args) = parser.parse_args()

# ERROR CHECK --------------------------------------
if not options.filename:   # if filename is not given
  parser.error('Filename not given')
# --------------------------------------------------

# Global Variables
V = [1, 10, 25, 50]
A = 11

def executeChangeSlow():
  global V, A
  # Make sure V[] and A are ready at this point
  solution = []
  solution = changeSlow(V, A)
  print "The solution is: " + str(solution)
  print "Total number of coins: " + str(solutionCoinSum(solution))
  return (solution, solutionCoinSum(solution))

def solutionCoinSum(solution):
  sum = 0
  for val in solution:
    sum += val
  return sum

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

# CHANGESLOW_UTILITY_METHOD
# Iterate through two arrays and find the sum of all the values.
def calculateCoinCount(a, b):
  coinCount = 0
  for x in a:
    coinCount += x
  for x in b:
    coinCount += x
  return coinCount

# CHANGESLOW_UTILITY_METHOD
# Input two solutions of equal length and merge them into a single list. 
def sumBothSolutions(a, b):
  newSolution = [0] * len(a)
  for i in xrange(0, len(a)):
    newSolution[i] = a[i] + b[i]
  return newSolution

# Sets the global variables V and A from the input file.
def loadInputFile(filename):
  global V,A
  with open(filename) as f:
    lines = f.readlines()
  V = lines[0].strip('\n')[1:-1]
  V = map(int, V.split(','))
  A = int(lines[1].strip('\n'))

def saveOutput(filename, solution, m):
  f = open(filename[:-4] + "change.txt",'w')
  f.write(str(solution))
  f.write('\n')
  f.write(str(m))
  f.close()

def main():
  
  # Variables
  solution = []
  m = 0

  # Setup
  loadInputFile(options.filename)
  
  # Algorithm Call
  if options.algorithm == '1':
    (solution, m) = executeChangeSlow()
  elif options.algorithm == '2':
    pass
  elif options.algorithm == '3':
    pass
  else:
    print "No algorithm selected. Quitting..."
    exit(1)

  # Output solution to file
  saveOutput(options.filename, solution, m)

if __name__ == "__main__":
  main()
