# Author: Group 8 (Bryant, Nathan, Keenan)
# Date: 01/30/2015
# Description: This program contains four algorithms which use
#              various approaches to find the max sub array from
#              a larger array.

import os, sys, re, random
from optparse import OptionParser
from time import time

################## SETUP ######################################
# GLOBAL VARIABLES
TEST_FILE = "MSS_Problems.txt"
RAND_MIN = -1000
RAND_MAX = 1000
globalArray = []
maxSubArrayArray = []
algorithmDictionary = {'1' : "Algorithm #1" , '2' : "Algorithm #2" , '3' : "Algorithm #3" , '4' : "Algorithm #4"}
# Setup the option parser for choosing the algorithm
parser = OptionParser()

parser.add_option("-a", "--algorithm", dest="algorithm", help="choose which algorithm to execute", metavar="<1 2 3 4>")

parser.add_option("-q", "--quiet", action="store_true", dest="quiet", default=False, help="do not show any success text")

parser.add_option("-f", "--file", action="store_true", dest="file", default=False, help="gather array data from file mstest.txt")

parser.add_option("-t", "--test", dest="test", metavar="<#>", help="run test on 10 iterations of a randomly generated array of size '#'")

parser.add_option("-d", "--demo", action="store_true", dest="demo", default=False, help="run selected algorithm on arrays of size 100, 200,...1000, 2000,..., 10000")

(options, args) = parser.parse_args()

###############################################################

# UTILITY FUNCTION
def max2(a, b):
  if a > b:
    return a
  else:
    return b

# UTILITY FUNCTION
def max3(a, b, c):
  return max2(max2(a, b), c)

# Used for algorithm #3, returns larges sum found between two arrays
def maxMiddleSum(array, low, mid, high):

  # Calculate max subarray on left side of current array
  sum = 0
  leftSum = 0
  for i in range(mid, low-1, -1):
    sum += array[i]
    if sum > leftSum:
      leftSum = sum

  # Calculate max subarray on right side of the current array
  sum = 0
  rightSum = 0
  for i in range(mid+1, high+1, 1):
    sum += array[i]
    if sum > rightSum:
      rightSum = sum

  return (leftSum + rightSum)

# Used for algorithm #3, returns maxSubArray sum
def maxSubArray(array, low, high):
  # BASE CASE
  if low == high:
    return array[low]
  mid = (low + high) / 2

  # Return the maximum of left sum, right sum, and combined(middle) sum
  return max3(maxSubArray(array, low, mid), maxSubArray(array, mid+1, high),
      (maxMiddleSum(array, low, mid, high)))

# Uses regex to take the array from the file as well as the sum listed at the
# end of each line. The string array is then mapped to an actual array in
# memory and returned.
def extractArray(line):
  re_expression = "\[([+-]?[0-9]*,? ?)*\]"
  m = re.search(re_expression, line)
  return map(int, m.group(0)[1:-1].split(','))

# Algorithm #1 uses a basic iterative approach
# Takes about 250 Seconds for 20,000 lines
def algorithm1(array):
  global maxSubArrayArray
  
  #print "Running algorithm #1..."  
  actualMaxArray = []
  currentMaxArray = []
  maxSum = 0
  currSum = 0
  t0 = time()
 
 # BEGIN ALGORITHM #1 HERE
  for i in xrange(0, len(array)):
    for k in xrange(0, len(array)):
      for m in xrange(i, k+1):
        currSum += array[m]
        currentMaxArray.append(array[m])
      if currSum > maxSum:
        maxSum = currSum
        actualMaxArray = currentMaxArray
        currentMaxArray = []
      else:
        currentMaxArray = []
      currSum = 0
  # END ALGORITHM #1 HERE
  
  t1 = time()
  runTime = t1 - t0
  
  return (maxSum, actualMaxArray, runTime)
  
# Algorithm #2 uses an improved iterative approach.
# Takes about 9 Seconds for 20,000 lines
def algorithm2(array):
  #print "Running algorithm #2..."
  maxSumIndexes = [0,0]
  maxSumArrayArray = []
  maxSum = 0
  currSum = 0
  t0 = time()
    
  # BEGIN ALGORITHM #2 HERE
  for i in xrange(0, len(array)):
    currSum = 0
    for k in xrange(i, len(array)):
      currSum += array[k]
      if currSum > maxSum:
        maxSum = currSum
        maxSumIndexes = [i,k]
  # END ALGORITHM #2 HERE
  

  t1 = time()
  runTime = t1 - t0
 
  # Record the values in th max sub array
  for x in xrange(maxSumIndexes[0], maxSumIndexes[1]+1):
    maxSumArrayArray.append(array[x])
  
  return (maxSum, maxSumArrayArray, runTime)

def algorithm3(array):
  #print "Running algorithm #3..."
  maxSum = 0
  maxSumArrayArray = []
  t0 = time()  
  
  # BEGIN ALGORITHM #3 HERE
  maxSum = maxSubArray(array, 0, len(array)-1)
  # END ALGORITHM #3 HERE
  
  t1 = time()
  runTime = t1 - t0
  if options.file:
    maxSumArrayArray = algorithm4(array)[1]
  else:
    maxSumArrayArray = []

  return (maxSum, maxSumArrayArray, runTime)

def algorithm4(array):
  #print "Running algorithm #4..."
  maxSum = 0
  currSum = 0
  firstIndex = 0
  maxFirstIndex = 0
  maxLastIndex = 0
  maxSubArray = []
  t0 = time()

  # BEGIN ALGORITHM #4 HERE
  for i in xrange(0, len(array)):
    
    if currSum + array[i] < 0:
      firstIndex = i+1
      currSum = 0
    else:
      currSum = currSum + array[i]

    if maxSum < currSum:
      maxFirstIndex = firstIndex
      maxLastIndex = i
      maxSum = currSum
  # END ALGORITHM #4 HERE

  t1 = time()
  runTime = t1 - t0
  
  # Figure out sub array based on indexes
  for i in xrange(maxFirstIndex, maxLastIndex + 1):
    maxSubArray.append(array[i])
  
  return (maxSum, maxSubArray, runTime)

def generateArrays(n):
  t0 = time()
  tempArr1 = []
  for i in xrange(10):
    tempArr2 = []
    for j in xrange(n):
      tempArr2.append(random.randint(RAND_MIN, RAND_MAX))
    tempArr1.append(tempArr2)
  t1 = time()
  #print "\nGenerated array of size %d in %lf seconds" % (n, t1-t0)
  return tempArr1

def verifyArgs():

  if (not options.demo) and (not options.file) and (options.test == None):
    print "Must include either -t, -d, or -f option"
    exit()
  elif (options.file) and (options.test != None):
    print "Invalid arguement combination"
    exit()            
  elif (not options.demo) and (not options.file) and options.test < 1:
    print "-t arguement must be greater than 0"
    exit()
 
  if (not options.demo) and (not options.file):
    try:
      options.test = int(options.test)
    except:
      print "-t arguement must be an integer"
      exit()

  if options.algorithm != '1' and options.algorithm != '2' and options.algorithm != '3' and options.algorithm != '4':
    print "Not a valid algorithm"
    exit(1)

def mainTest():
  global globalArray

  for k in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]:
  
    globalArray = generateArrays(k)

    totalTime = 0
    totalTests = len(globalArray)

    for j in xrange(len(globalArray)):
      maxSum = 0
      maxSubArray = []
      array = globalArray[j]

      if options.algorithm == '1':
        (maxSum, maxSubArray, runTime) = algorithm1(array)
      elif options.algorithm == '2':
        (maxSum, maxSubArray, runTime) = algorithm2(array)
      elif options.algorithm == '3':
        (maxSum, maxSubArray, runTime) = algorithm3(array)
      elif options.algorithm == '4':
        (maxSum, maxSubArray, runTime) = algorithm4(array)
      else:
        print "No algorithm selected. Quitting..."
        exit()
    
      # Keep track of total run time
      totalTime += runTime
    print totalTime

def main():
  global globalArray

  # Make sure all flag/arguement combinations are valid
  verifyArgs() 

  if options.demo:
    mainTest()
    exit()

  if options.file:
    print "----------------------------------------------------------------------"
    print "                        %s                                            " % algorithmDictionary[options.algorithm]
    print "----------------------------------------------------------------------"
    # Read the test cases from the test file and save to global 2D array
    with open(TEST_FILE) as f:
      for line in f:
        array = extractArray(line)
        globalArray.append(array)
      # At this point globalArray contains all the arrays from the file in [x][0]
      # and the corresponding max_sum in [x][1]
  else:
    globalArray = generateArrays(options.test)

  totalTime = 0
  totalTests = len(globalArray)
  count = 0.0

  for j in xrange(len(globalArray)):
    maxSum = 0
    array = globalArray[j]
    maxSubArray = []
    
    if options.algorithm == '1':
      (maxSum, maxSubArray, runTime) = algorithm1(array)
    elif options.algorithm == '2':
      (maxSum, maxSubArray, runTime) = algorithm2(array)
    elif options.algorithm == '3':
      (maxSum, maxSubArray, runTime) = algorithm3(array)
    elif options.algorithm == '4':
      (maxSum, maxSubArray, runTime) = algorithm4(array)
    else:
      print "No algorithm selected. Quitting..."
      exit()
    
    if not options.quiet and options.file:
      print "\nOriginal Array: " + str(array)
      print "Maximum Sum: " + str(maxSum)
      print "Max SubArray: " + str(maxSubArray)
      print "Runtime: " + str(runTime)
    # Keep track of total run time
    totalTime += runTime
    count += 1

    if options.test != None:
      percent = str(count/10.0*100) + "%"
      sys.stdout.write("\r%s" % percent)
      sys.stdout.flush()
  #print "\nResults for " + algorithmDictionary[options.algorithm] 
  #print "=================================="
  #print "Total Time = " + str(totalTime)
  #print "Average Time per line = " + str(totalTime / 10) + "\n" 
  if options.test != None:
    sys.stdout.write("\r%s\n" % str(totalTime/10.0))
    sys.stdout.flush()
if __name__ == "__main__":
  main()
