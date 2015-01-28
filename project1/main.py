# Author: Group 8 (Bryant, Nathan, Keenan)
# Date: 01/27/2015
# Description: This program contains four algorithms which use
#              various approaches to find the max sub array from
#              a larger array.

import os, sys, re
from optparse import OptionParser
from time import time

################## SETUP ######################################
# GLOBAL VARIABLES
TEST_FILE = "mstest.txt"
globalArray = []
algorithmDictionary = {'1' : "Algorithm #1" , '2' : "Algorithm #2" , '3' : "Algorithm #3" , '4' : "Algorithm #4"}
# Setup the option parser for choosing the algorithm
parser = OptionParser()
parser.add_option("-a", "--algorithm", dest="algorithm",
                      help="choose which algorithm to execute",
                      metavar="<1 2 3 4>")

parser.add_option("-l", "--long",
                      action="store_true", dest="long", default=False,
                      help="use extended test file")

parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
    default=False, help="do not show any success text")

(options, args) = parser.parse_args()

if options.long:
  TEST_FILE = "mstest_l.txt"
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
  v = re.findall(', [0-9]*', line)
  return map(int, m.group(0)[1:-1].split(',')), v[-1][2:]

# Algorithm #1 uses a basic iterative approach
# Takes about 250 Seconds for 20,000 lines
def algorithm1(array):
  #print "Running algorithm #1..."  
  maxSum = 0
  currSum = 0
  t0 = time()
 
 # BEGIN ALGORITHM #1 HERE
  for i in xrange(0, len(array)):
    for k in xrange(0, len(array)):
      for m in xrange(i, k+1):
        currSum += array[m]
      if currSum > maxSum:
        maxSum = currSum
      currSum = 0
 # END ALGORITHM #1 HERE
  
  t1 = time()
  runTime = t1 - t0
  return (maxSum, runTime)
  
# Algorithm #2 uses an improved iterative approach.
# Takes about 9 Seconds for 20,000 lines
def algorithm2(array):
  #print "Running algorithm #2..."
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
  # END ALGORITHM #2 HERE

  t1 = time()
  runTime = t1 - t0
  
  return (maxSum, runTime)

def algorithm3(array):
  #print "Running algorithm #3..."
  maxSum = 0
  t0 = time()  
  
  # BEGIN ALGORITHM #3 HERE
  maxSum = maxSubArray(array, 0, len(array)-1)
  # END ALGORITHM #3 HERE
  
  t1 = time()
  runTime = t1 - t0
  return (maxSum, runTime)

def algorithm4(array):
  #print "Running algorithm #4..."
  maxSum = 0
  currSum = 0
  t0 = time()

  # BEGIN ALGORITHM #4 HERE
  for val in array:
    currSum = max2(0, currSum + val)
    maxSum = max2(maxSum, currSum)
  # END ALGORITHM #4 HERE

  t1 = time()
  runTime = t1 - t0
  return (maxSum, runTime)

def main():
  global globalArray

  # Read the test cases from the test file and save to global 2D array
  with open(TEST_FILE) as f:
    for line in f:
      (array, val) = extractArray(line)
      globalArray.append([array, val])
    # At this point globalArray contains all the arrays from the file in [x][0]
    # and the corresponding max_sum in [x][1]
  

  totalTime = 0
  totalTests = len(globalArray)

  for j in xrange(len(globalArray)):
    maxSum = 0
    array = globalArray[j][0]
    real_sum = int(globalArray[j][1])

    if options.algorithm == '1':
      (maxSum, runTime) = algorithm1(array)
    elif options.algorithm == '2':
      (maxSum, runTime) = algorithm2(array)
    elif options.algorithm == '3':
      (maxSum, runTime) = algorithm3(array)
    elif options.algorithm == '4':
      (maxSum, runTime) = algorithm4(array)
    else:
      print "No algorithm selected. Quitting..."
      exit()
    
    if not options.quiet:
      if maxSum == real_sum:
        print "SUCCESS. Time = " + str(runTime)
      else:
        print "FAIL! We got " + str(maxSum) + " but the right answer was "+str(real_sum)
    # Keep track of total run time
    totalTime += runTime
    
  print "\nResults for " + algorithmDictionary[options.algorithm] 
  print "=================================="
  print "Total Time = " + str(totalTime)
  print "Average Time per Iteration = " + str(totalTime / totalTests)

if __name__ == "__main__":
  main()
