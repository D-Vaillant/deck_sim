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

def unit_test():
    D = InductiveDeck(60, [40,10,10])
    D.main()
    

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
            print("Partition summed to ", partSum, ".")
            print("However, size was specified as ", self.size, ".")
            raise ArithmeticError("Partition too large!")
        elif partSum < self.size:
            self.partition.insert(0, self.size - partSum)
        else: pass
        
    def generateCardArr(self):
        """ Takes self.size and self.partition and generates a deck. """

        dk = []
        for i, x in enumerate(self.partition):
            dk.extend([self.cardSymbols[i]] * x)
        return dk

class InductiveDeck(Deck):
    def main(self):
        sampleSize, trialCount, symbolReqs = self.get_information_unit()
        
        successList = [self.tester(
                            self.run_trial(sampleSize), 
                            symbolReqs)
                       for x in range(trialCount)]
        print("Success rate: {0}%.".format((successList.count(True))/trialCount))

    def get_information_unit(self):
        return 7, 10000, {'A': 2}

    def get_information(self):
        sz = int(input('Sample size: '))
        tr = int(input('Trial count: '))

        char_inc = lambda x: chr(ord(x)+1)
        ch = 'A'
        _ = True
        part_dict = {}
        
        print("Enter 0 to terminate partition size entry.")
        while(_):
            _ = int(input("Required number of cards of symbol {}:  ".format(ch)))
            if _: 
                part_dict[ch] = _
                char_inc(ch)
        return sz, tr, part_dict


    """ Adds probability methods which rely on running trials. """
    def run_trial(self, sample_size):
        shuffle(self.cards)
        return Counter(self.cards[:sample_size])

    def tester(self, trialResults, minRequired):
        """ Takes a Counter from run_trial and a min. requirement dict, returns True or False. """
        isSuccessful = True 

        for symbol, req in minRequired.items():
            if trialResults[symbol] < req: 
                pass
            else: 
                isSuccessful = False
                break

        return isSuccessful

class CombinatoricDeck(Deck):
    def __init__(self):
        self.main()

    def infoput(self):
        """ Takes input, returns a tuple of the relevant variables. """
        element_sizes = {}
        pop_size = int(input('How many cards total? - '))
        var_1 = int(input('How many types of non-blank cards? - '))
        total = 0
        for i in range(var_1):
            a = int(input('How many cards of type {0}? - '.format(i+1)))
            total += a
            if total > pop_size: raise ValueError("Population overflow.")
            element_sizes[i] = a
        if total < pop_size:    
            element_sizes[i+1] = pop_size - total
        print("Current card distribution: {0}".format(element_sizes))
        sample_size = int(input("How many cards will be drawn? - "))
        requirelist = [(i, int(input("How many cards of type {0} ".format(i+1) +
                             "should be drawn? - "))) for i in range(var_1)]
        return pop_size, element_sizes, sample_size, requirelist

    @staticmethod
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

    def main(self):
        pop, ele, sam, req = self.testput()
        total = self.choose(pop,sam)
        hit_array = []

        """ Generates a list of representative sequences recursively.
            See outline for details. """
        
        def seq_gen(lst, p, rem):
            temp_list = list(lst)
            if p == len(ele)-1:
                temp_list.append(rem)
                hit_array.append(temp_list)
                return None
            for i in range(ele[p]):
                temp_list = list(lst)
                temp_rem = rem - i
                if temp_rem < 0: return None
                elif temp_rem == 0:
                    temp_list.append(rem)
                    for q in range(p+1, len(ele)): temp_list.append(0)
                    hit_array.append(temp_list)
                    return None
                else:
                    temp_list.append(i)
                    seq_gen(temp_list, p+1, temp_rem)

        seq_gen([], 0, sam)

        A = dict()
        for x in hit_array:
            product = 1
            for y in range(len(x)):
                product *= self.choose(ele[y], x[y])
            A[tuple(x)] = product/total
        return percentage_wrapper(A)
        
    def testput(self):
        return 60, {0: 20, 1: 20, 2: 10, 3: 10}, 7, 2

class percentage_wrapper():
    def __init__(self, memory, type_dist = None):
        self.mem = memory
        self.x_axis = [x for x in memory.keys()]
        self.x_arity = len(self.x_axis[0])
        self.typenames = {}
        self.typemaxes = type_dist if type_dist else self.type_finder(memory)
        self.sample_size = sum(self.x_axis[0])
        self.y_axis = [y for y in memory.values()]

    def type_finder(self, memory):
        return dict([(a, max([b[a] for b in self.x_axis]))
                            for a in range(self.x_arity)])

    ##def set_typenames(self, string_list = ['']*self.x_arity):
    ##    for i in range(x_arity):
            
    
    def interval_select(self, r, x_ax, s_p):
        """ Returns X in x_ax such that s_pair[0] <= X[position] <= s_pair[1] """
        s_p = (0, self.x_arity - 1) if s_p == () else s_p
        if s_p[0]-1 > s_p[1]: raise ValueError("empty interval.")
        if r >= len(x_ax[0]): raise IndexError("position out of bounds.")

        return [x for x in x_ax if x[r] in range(s_p[0], s_p[1]+1)]

    def comp_int_select(self, selection_dict):
        """ Takes a list of interval pairs and returns a list of coordinates in 
            x_axis which are within the specified ranges. """
        out = self.x_axis
        if len(selection_dict) != self.x_arity:
            raise IndexError("Selection dict must be {0} pairs big.".format(
                                                                self.x_arity))
        for i in range(self.x_arity):
            out = self.interval_select(i, out, selection_dict[i])
        return out

    def selection_creator(self):
        """ Creates a selection dictionary using user input. """            
        selection = {}
        for i in range(self.x_arity):
            a = input('Minimum cards of type {0}? - '.format(i+1))
            b = int(input('Maximum cards of type {0}? - '.format(i+1)))
            selection[i] = (int(a) if a!='' else None, int(b) if b!='' else None)
        return selection

    def main(self):
        """ Gives percentage chance of user input coming out true. """
        s = self.selection_creator()
        return sum([self.mem[x] for x in self.comp_int_select(s)])

 
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
