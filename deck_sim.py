#!/usr/bin/env python3
""" deck_sim.py: Simulates a deck of cards with various types of cards, 
                shuffles it, and counts occurrences of each type.
                Checks whether or not occurrences of each type exceed
                specified threshold and returns true or false.
                Repeats above two procedures a specified number of times
                and reports the percentage of repetitions which return true."""

__author__ = "David Vaillant"

from random import shuffle
from collections import Counter

class Deck():
    # Limits number of card symbols to 27.
    cardSymbols = {i+1 : chr(ord('A')+i) for i in range(26)}
    cardSymbols.update({0:'_'})

    def __init__(self, sz, partArr = None, isShuffled = False):
        self.size = sz

        self.partition = partArr or [sz]
        self.partitionChecker() 
        
        self.cards = self.generateCardArr()
        if isShuffled: shuffle(self.cards)

    def partitionChecker(self):
        partSum = sum(self.partition)

        if partSum > self.size:
            print("Partition summed to ", partSum ".")
            print("However, size was specified as ", self.size, ".')
            raise ArithmeticError("Partition too large!")
        elif partSum < self.size:
            self.partition.insert(0, self.size - partSum)
        else: pass
        
    def generateCardArr(self):
        """ Takes self.size and self.partition and generates a deck. """

        dk = []
        for i, x in self.partition:
            dk.extend([cardSymbols[i] * x)
        return dk

class InductiveDeck(Deck):
    def main(self):
        sampleSize, trialCount, symbolReqs = self.get_information()
        
        successList = [self.minimum_tester(
                            self.run_trial(sampleSize), symbolReqs)
                            for x in range(trialCount)]
        print("Success rate: {0}%.".format((successList.count(True))/trialCount)

    def get_information(self):
        sz = int(input('How many cards total? - '))
        
        char_inc = lambda x: chr(ord(x)+1)
        ch = 'A'
        _ = True
        part_dict = {}
        
        print("Enter 0 to terminate partition size entry.")
        while(_):
            _ = int(input("How many cards of symbol {}?".format(ch)))
            if _: part_dict[ch] = _


    """ Adds probability methods which rely on running trials. """
    def run_trial(self, sample_size):
        shuffle(self.cards)
        return Counter(self.cards[:sample_size])

    def minimum_tester(self, trialResults, minRequired):
        """ Takes a Counter from run_trial and a min. requirement dict, returns True or False. """
        isSuccessful = None

        for symbol, req in enumerate(minRequired):
            if trialResults[symbol] < req: 
                isSuccessful = False
                break
            else: 
                isSuccessful = True

        return isSuccessful

class CombinatoricDeck(Deck):
    def choose(n, k):
        """ A fast way to calculate binomial coefficients by Andrew Dalke. """
        if 0 <= k <= n:
            ntok = 1
            ktok = 1
            for t in range(1, min(k, n - k) + 1):
                ntok *= n
                ktok *= t
                n -= 1
            return ntok // ktok
        else:
            return 0


### HERE LIES THINGS ###
''' Takes a distribution array (element_sizes), a population size, and the

    size of cards to be sampled. Has error correction to ensure that the sum
    of the distribution array matches the population size. 
    Creates a deck and iterates over sample_size cards to determine counts of
    each type of card. Returns a map from types to counts. '''
''' Takes variables via command line input and calculates percentage of
    successes. '''
def main():
    element_sizes = []
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
