#!/usr/bin/env python3
""" deck_sim.py: Simulates a deck of cards with various types of cards, 
                shuffles it, and counts occurrences of each type.
                Checks whether or not occurrences of each type exceed
                specified threshold and returns true or false.
                Repeats above two procedures a specified number of times
                and reports the percentage of repetitions which return true."""

__author__ = "David Vaillant"

from random import shuffle
from collections import defaultdict

''' Returns a shuffled deck with pop_size elements according to the
    distribution in element_sizes. '''
def deck_creation(element_sizes, pop_size):
    deck = []
    for i in range(len(element_sizes)):
        deck.extend([i] * element_sizes[i])
    shuffle(deck)
    return deck

''' Takes a distribution array (element_sizes), a population size, and the
    size of cards to be sampled. Has error correction to ensure that the sum
    of the distribution array matches the population size. 
    Creates a deck and iterates over sample_size cards to determine counts of
    each type of card. Returns a map from types to counts. '''
def run_trial(element_sizes, pop_size, sample_size):
    total = sum(element_sizes)
    if total < pop_size:
        element_sizes.append(pop_size - total)
    deck = deck_creation(element_sizes, pop_size)
    summary_dict = defaultdict(lambda: 0)
    for x in deck[:sample_size]:
        summary_dict[x] += 1
    return summary_dict

''' Takes two maps from types to counts, a sample and a requirement dictionary.
    Returns true if the each key in the sample dictionary is greater than
    the corresponding key in the requirement dictionary. '''
def minimum_tester(results, requirement):
    successes = 0
    for sample_dict in results:
        glass = True
        for x in requirement:
            if sample_dict[x] < requirement[x]: glass = False
        if glass: successes += 1
    return successes

''' Takes variables via command line input and calculates percentage of
    successes. '''
def main():
    element_sizes = []
    pop_size = int(input('How many cards total? - '))
    var_2 = int(input('How many types of non-blank cards? - '))
    total = 0
    for i in range(var_2):
        a = int(input('How many cards of type {0}? - '.format(i+1)))
        total += a
        if total > pop_size:
            print('Population overflow.')
            return NONE
        element_sizes.append(a)
    if total < pop_size:    
        element_sizes.append(pop_size - total)
    print("Current card distribution: {0}".format(element_sizes))
    sample_size = int(input("How many cards will be drawn? - "))
    requirelist = [(i, int(input("How many cards of type {0} ".format(i+1) +
                         "should be drawn? - "))) for i in range(var_2)]
    requirement_dict = dict(requirelist)
    runs = int(input("How many trials will be run? - "))
    results = [run_trial(element_sizes, pop_size, sample_size)
               for x in range(runs)]
    successes = minimum_tester(results, requirement_dict)
    print("Drew all cards {0}% of the time.".format((successes/runs)*100))
    boole = bool(input("Repeat? (Hit enter to terminate.) - "))
    while boole:
        sample_size = int(input("How many cards will be drawn? - "))
        results = [run_trial(element_sizes, pop_size, sample_size)
               for x in range(runs)]
        successes = minimum_tester(results, requirement_dict)
        print("Drew all cards {0}% of the time.".format((successes/runs)*100))
        boole = bool(input("Repeat? (Hit enter to terminate.) - "))

''' Allows manual setting of variables. '''
def lazymain():
    runs = 10000
    element_sizes = [19, 31]
    pop_size = sum(element_sizes)
    sample_size = 20
    var_2 = len(element_sizes) - 1
    requirelist = [(i, int(input("How many cards of type {0} ".format(i+1) +
                         "should be drawn? - "))) for i in range(var_2)]
    requirement_dict = dict(requirelist)
    results = [run_trial(element_sizes, pop_size, sample_size)
               for x in range(runs)]
    successes = minimum_tester(results, requirement_dict)
    print("Drew all cards {0}% of the time.".format((successes/runs)*100))
