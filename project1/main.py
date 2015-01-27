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

# Setup the option parser for choosing the algorithm
parser = OptionParser()
parser.add_option("-a", "--algorithm", dest="algorithm",
                      help="choose which algorithm to execute",
                      metavar="<1 2 3 4>")

parser.add_option("-l", "--long",
                      action="store_true", dest="long", default=False,
                      help="use extended test file")

(options, args) = parser.parse_args()

if options.long:
  TEST_FILE = "mstest_l.txt"
###############################################################

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
def algorithm1():
  print "Running algorithm #1..."
  
  totalTime = 0
  totalTests = len(globalArray)

  # First for-loop is for iterating through all test arrays, not part of
  # algorithm complexity.
  for j in xrange(len(globalArray)):
    maxSum = 0
    currSum = 0
    array = globalArray[j][0]
    real_sum = int(globalArray[j][1])

    # BEGIN ALGORITHM #1 HERE
    t0 = time()
    for i in xrange(0, len(array)):
      for k in xrange(0, len(array)):
        for m in xrange(i, k+1):
          currSum += array[m]
        if currSum > maxSum:
          maxSum = currSum
        currSum = 0
    t1 = time()
    totalTime += t1 - t0
    # END ALGORITHM #1 HERE

    if maxSum == real_sum:
      print "SUCCESS! Time = " + str(t1-t0)
    else:
      print "FAIL! We got " + str(maxSum) + " but the right answer was " + str(real_sum)

  print "Total Time = " + str(totalTime)
  print "Average Time per Iteration = " + str(totalTime / totalTests)

# Algorithm #2 uses an improved iterative approach.
# Takes about 9 Seconds for 20,000 lines
def algorithm2():
  print "Running algorithm #2..."
  
  totalTime = 0
  totalTests = len(globalArray) 

  # First for-loop is for iterating through all test arrays, not part of
  # algorithm complexity.
  for j in xrange(len(globalArray)):
    maxSum = 0
    currSum = 0
    array = globalArray[j][0]
    real_sum = int(globalArray[j][1])

    # BEGIN ALGORITHM #2 HERE
    t0 = time()
    for i in xrange(0, len(array)):
      currSum = 0
      for k in xrange(i, len(array)):
        currSum += array[k]
        if currSum > maxSum:
          maxSum = currSum
    t1 = time()
    totalTime += t1 - t0
    # END ALGORITHM #2 HERE
    
    if maxSum == real_sum:
      print "SUCCESS. Time = " + str(t1-t0)
    else:
      print "FAIL! We got " + str(maxSum) + " but the right answer was " + str(real_sum)

  print "Total Time = " + str(totalTime)
  print "Average Time per Iteration = " + str(totalTime / totalTests)


def algorithm3():
  print "Running algorithm #3..."
  pass

def algorithm4():
  print "Running algorithm #4..."
  pass

def main():
  global globalArray

  # Read the test cases from the test file and save to global 2D array
  with open(TEST_FILE) as f:
    for line in f:
      (array, val) = extractArray(line)
      globalArray.append([array, val])
    # At this point globalArray contains all the arrays from the file in [x][0]
    # and the corresponding max_sum in [x][1]
  
  if options.algorithm == '1':
    algorithm1()
  elif options.algorithm == '2':
    algorithm2()
  elif options.algorithm == '3':
    algorithm3()
  elif options.algorithm == '4':
    algorithm4()
  else:
    print "No algorithm selected. Quitting..."

if __name__ == "__main__":
  main()
