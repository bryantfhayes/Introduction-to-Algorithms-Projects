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
    return [[cities[0]] + list(tour) for tour in itertools.permutations(cities[1:])]

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
    for city in tour:
        f.write(str(city.id) + '\n')
    f.close()

# Takes in an algorithm as well as a list of cities. It applies algorithm and plots the result if -p flag is set
def calculateTour(algorithm, cities):
    # Find the solution and time how long it takes
    t0 = time.time()
    tour = algorithm(cities)
    t1 = time.time()
    if options.plot:
        # Plot the tour as blue lines between blue circles, and the starting city as a red square.
        plotline(list(tour) + [tour[0]])
        plotline([tour[0]], 'rs')
        plt.show()
    print("{} city tour; total distance = {:.1f}; time = {:.3f} secs for {}".format(
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
    return cities

def basicGreedy(cities):
    global currentCity
    remainingCities = cities
    currentCity = cities[0]
    remainingCities.remove(currentCity)
    tour = [currentCity]

    while len(remainingCities) > 0:
        # Find the closest city
        currentCity = min(remainingCities, key=distanceFromCurrentCity)
        # Add it to the tour
        tour.append(currentCity)
        # Remove city from remaining options
        remainingCities.remove(currentCity)

    return tour
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

    tour = calculateTour(algorithms[int(options.algorithm)], cities)
    if options.file != None:
        printToFile(options.file, tour)

if __name__ == '__main__':
    main()
