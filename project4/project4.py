# TRAVELING SALESMAN PROBLEM
import os, sys, matplotlib, random, time, itertools

City = complex

def distance(a, b):
    return abs(a - b)

def Cities(n):
    return list(set(City(random.randrange(10, 890), random.randrange(10, 590)) for c in range(n)))

def allTours(cities):
    return [[cities[0]] + list(tour) for tour in itertools.permutations(cities[1:])]

random.seed('seed')
cities8 = Cities(3)

print cities8
print allTours(cities8)
print distance(cities8[0], cities8[1])
