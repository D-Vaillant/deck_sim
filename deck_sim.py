#!/usr/bin/env python3
""" deck_sim.py: Simulates a deck of cards with various types of cards, 
                shuffles it, and counts occurrences of each type.
                Checks whether or not occurrences of each type exceed
                specified threshold and returns true or false.
                Repeats above two procedures a specified number of times
                and reports the percentage of repetitions which return true.
                
    Representative: An array which represents the possible combinations of 
                drawing sample_size cards. For a Deck with N symbols {a,b..z}
                a representative has the form [x_a, x_b..x_z] where
                    x_i <= Deck.count(i) 
                for all i and 
                    sum(x_a...x_z) = Deck.sample_size. """

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

    def __init__(self, s_sz = None, p_arr = None):
        self.sample_size = s_sz
        self.partition = p_arr
        
        self.getInformation() # Gets sample_size and partition from user input
        self.cards = self.generateCardArr() # creates array of "cards"
        
        # creates self.representatives
        self.representatives = []
        self.generateRepresentatives(self.sample_size)

    def getInformation(self):
        if not self.sample_size:
            self.sample_size = int(input("Enter sample population: "))
            print("Sample size set to {}.".format(self.sample_size))
        if not self.partition:
            entry = 0
            partition_index = 0
            while(entry >= 0 and partition_index < 27):
                print("Running partition entry.")
                print("Enter a negative value to stop partition entry.")
                
                entry = int(input("Enter number of {} instances: ".format(
                                   cardSymbols[partition_index])))
                try:
                    self.partition[partition_index] = entry
                except IndexError:
                    print("Index overflow error..")
                    break
        return

    def generateCardArr(self):
        """ Takes self.size and self.partition and generates a deck. """

        dk = []
        for i, x in enumerate(self.partition):
            dk.extend([i] * x)
        return dk

    def generateRepresentatives(self, remainder, lst = [], partition_index = 0):
        """ Creates an array of all possible n-length samplings of cards.
                We call these "representatives".
            Usage: Remainder should be self.sample_size initially. 
            This one's a bit of a doozy, so hang in there. """

        if partition_index == len(self.partition): 
            # Enter this part if we've gone over any symbol.
            if not remainder: self.representatives.append(tuple(lst)) 
            return 0 # Shut down the recursion.

        for i in range(self.partition[partition_index]+1):
            # i is a candidate for the representative.
            temp_list = lst[:] 
            temp_rem = remainder - i
            if temp_rem < 0: return None # Terminate if i is too large. 
            elif temp_rem == 0:
                # Finish the representative up if i would make it sum up to 
                # sample_size. 
                temp_list.append(i)
                for q in range(partition_index+1, len(self.partition)): 
                    temp_list.append(0) 
                self.representatives.append(tuple(temp_list))
                return None
            else: # temp_rem > 0, i.e. "more elements needed".
                temp_list.append(i) # tack on i to rep_arr
                self.generateRepresentatives(temp_rem, temp_list, 
                                             partition_index+1)
                # Go back through for the next symbol in the representative.

    def __str__(self):
        out = '|'.join([self.cardSymbols[x] for x in self.cards])
        out += '\n'
        out += ("Sample size: {}\n"
                "Partition: {}".format(self.sample_size, self.partition))
        return out


class InductiveDeck(Deck):
    """ Adds probability methods which rely on running trials. """
    def __init__(self, s_sz = None, p_arr = None, num_trials = 0):
        Deck.__init__(self, s_sz, p_arr)
        
        if num_trials > 0:
            self.trial_count = num_trials
        else:
            self.trial_count = int(input("Enter number of trials: "))
            print("Trial count set to {}.".format(self.trial_count))

        return
            
    def trialRun(self):
        shuffle(self.cards)
        cc = Counter(self.cards[:self.sample_size])
        return tuple(cc[x] for x in range(len(self.partition)))

    def main(self):
        cm = Counter()
        for x in range(self.trial_count): cm[self.trialRun()] += 1

        return {x:(y/self.trial_count) for x, y in cm.items()} 


class HypergeometricDeck(Deck):
    def main(self):
        total_size = sum(self.partition)
        total_comb = self.choose(total_size, self.sample_size)

        A = dict()
        for x in self.representatives:
            product = 1
            for index, symbols_drawn in enumerate(x):
                product *= self.choose(self.partition[index], symbols_drawn)
            A[x] = product/total_comb
        return A
        
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

"""
def tuple_append(tup, x):
    lst = list(tup)
    list.append(x)
    return tuple(lst)

def novel_range(reprD, level):
    num =  

def matrix_maker(repr_dict, level = None, *args):
    if level = None: level = len(list(repr_dict.keys())[0])
    if level == 0:
        return repr_dict[*args]
    elif level == 1:
        return [matrix_maker(repr_dict, level-1, tuple_append(tmp, x)) for x in novel_range(repr_dict, level)]
"""


""" PRESENTATION CLASS
Translates a map from a representative array to percentages to a
user-readable format. """

class percentage_wrapper():
    def __init__(self, map_repr_to_percentages):
        self.map = map_repr_to_percentages
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


""" UNIT TESTING FUNCTIONS """
def representTester(deckObject):
    summationArr = [deckObject.sample_size == sum(x) 
                    for x in deckObject.representatives]
    lessThanArr = [[x >= y for x, y in zip(deckObject.partition, R)] 
                           for R in deckObject.representatives]
    out = True
    for x in summationArr: out = x and out
    for x in lessThanArr: out = x.count(True) and out
    
    return out
