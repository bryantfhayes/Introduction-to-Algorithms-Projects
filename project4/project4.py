# TRAVELING SALESMAN PROBLEM
import os, sys, matplotlib, random, time, itertools
import matplotlib.pyplot as plt
from optparse import OptionParser

currentCity = None

# Setup the option parser for choosing the algorithm
parser = OptionParser()

parser.add_option("-a", "--algorithm", dest="algorithm", help="choose which algorithm to execute", metavar="<1 2 3 4>")

parser.add_option("-p", "--plot", action="store_true", dest="plot", default=False, help="Plot result on graph")

parser.add_option("-f", "--file", dest="file", metavar="<filename>", help="Load cities from file: <id> <x> <y>")

parser.add_option("-r", "--random", dest="random", metavar="<n>", help="Load 'n' cities randomly")

parser.add_option("-i", "--improve", action="store_true", dest="improve", default=False, help="Will try to improve solution post-algorithm using 2-opt")

(options, args) = parser.parse_args()

# Create an 'object'. This gives us an X and a Y values to treat as coordinates.
class City():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

def nearestInt(n):
    if (n > 0):
        return int(n+.5)
    else:
        return int(n-.5)

# Generate a bunch random city objects and return them in list
def generateRandomCities(n):
    return list(set(City(c, random.randrange(10, 1000), random.randrange(10, 1000)) for c in range(n)))

def generateCitiesFromFile(filename):
    lines = [line.strip() for line in open(filename)]
    return list(set(City(int(line.split()[0]), int(line.split()[1]), int(line.split()[2])) for line in lines))

# Given a list of tour possibilities, return the shortest
def shortestTour(tours):
    return min(tours, key=tourDistanceSum)

# Given two points (complex numbers), return the distance between them
def distance(a, b):
    return nearestInt(pow((pow(b.x - a.x, 2) + pow(b.y - a.y, 2)), 0.5))

# Given a list of cities, return every permutation of tours to visit.
def allTours(cities):
    allTours = []
    for tour in itertools.permutations(cities[1:]):
        allTours.append((cities[0],) + tour + (cities[0],))
    return allTours

# Calculates the sum of all the distances along the 'tour'
def tourDistanceSum(tour):
    return sum(distance(tour[i], tour[i-1]) for i in range(len(tour)))

# Calculate distance from GLOBAL variable currentCity
def distanceFromCurrentCity(n):
    return distance(n, currentCity)

# Print output to the output file: filename + .tour
def printToFile(filename, tour):
    f = open(filename + '.tour', 'w+')
    f.write(str(tourDistanceSum(tour)) + '\n')
    for city in tour[:-1]:
        f.write(str(city.id) + '\n')
    f.close()

# Takes in an algorithm as well as a list of cities. It applies algorithm and plots the result if -p flag is set
def calculateTour(algorithm, cities):
    # Find the solution and time how long it takes
    t0 = time.time()
    tour = algorithm(cities)
    t1 = time.time()
    print("{} city tour; Initial Tour distance = {:.1f}; time = {:.3f} secs for {}".format(
          len(tour)-1, tourDistanceSum(tour), t1-t0, algorithm.__name__))
    return tour

# Utility function for plotting points on matlab plot
def plotline(points, style='bo-'):
    X, Y = [p.x for p in points], [p.y for p in points]
    plt.plot(X, Y, style)

# ------------------- ALGORITHMS ----------------------------------
# Find every existing tour and pick the best one
def optimalTSP(cities):
    return shortestTour(allTours(cities))

def inOrder(cities):
    return cities + [cities[0]]

def basicGreedy(cities):
    global currentCity
    remainingCities = cities
    startingCity = cities[0]
    currentCity = startingCity
    remainingCities.remove(currentCity)
    tour = [currentCity]

    while len(remainingCities) > 0:
        # Find the closest city
        currentCity = min(remainingCities, key=distanceFromCurrentCity)
        # Add it to the tour
        tour.append(currentCity)
        # Remove city from remaining options
        remainingCities.remove(currentCity)
    tour.append(startingCity)
    return tour

def execute2opt(tour):
    newDistance = tourDistanceSum(tour)
    currentDistance = sys.maxint
    newTour = tour
    while newDistance < currentDistance:
        # print "newDistance vs Old" + str(newDistance) + ' vs ' + str(currentDistance)
        try:
            currentDistance = newDistance
            (newTour, newDistance) = run2opt(newTour, currentDistance)

        # If a keyboard interrupt is used, finish nicely and show what we have so far...
        except KeyboardInterrupt:
            print("{} city tour; Optimized Distance = {:.1f}".format(
                  len(newTour)-1, tourDistanceSum(newTour)))

            if options.plot:
                # Plot the tour as blue lines between blue circles, and the starting city as a red square.
                plotline(list(newTour))
                plotline([newTour[0]], 'rs')
                plt.show()

            if options.file != None:
                printToFile(options.file, tour)

            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    print("{} city tour; Optimized distance = {:.1f}".format(
          len(newTour)-1, tourDistanceSum(newTour)))
    return newTour

def run2opt(tour, currentDistance):
    for i in xrange(len(tour)-1):
        for k in xrange(i + 1, len(tour)):
            newTour = optswap(tour, i, k)
            newDistance = tourDistanceSum(newTour)
            if newDistance < currentDistance:
                return(newTour, newDistance)
    return(tour, currentDistance)

def optswap(tour, i, k):
    newTour = []
    for j in xrange(0, i):
        newTour.append(tour[j])
    for j in xrange(k, i-1, -1):
        newTour.append(tour[j])
    for j in xrange(k + 1, len(tour)):
        newTour.append(tour[j])
    return newTour

# -----------------------------------------------------------------

algorithms = [optimalTSP, basicGreedy]

def main():
    if (options.random == None) and (options.file == None):
        print "Please choose either FILE or RANDOM mode"
        exit(1)
    if (options.algorithm == None) or ((int(options.algorithm) - 1) > len(algorithms)) or (int(options.algorithm) < 0):
        print "Please select an algorithm:"
        print "0. Optimal"
        print "1. Greedy (basic)"
        exit(1)

    if options.random != None:
        if int(options.random) > 1:
            random.seed(time.time())
            cities = generateRandomCities(int(options.random))
    elif options.file != None:
        cities = generateCitiesFromFile(options.file)

    cities.sort(key=lambda x: x.id)

    # Use initial algorithm to get base answer
    tour = calculateTour(algorithms[int(options.algorithm)], cities)

    if options.improve:
        tour = execute2opt(tour)

    # Write output to file if file is used as input
    if options.file != None:
        printToFile(options.file, tour)

    # Plot graph is -p flag is present
    if options.plot:
        # Plot the tour as blue lines between blue circles, and the starting city as a red square.
        plotline(list(tour))
        plotline([tour[0]], 'rs')
        plt.show()

if __name__ == '__main__':
    main()
