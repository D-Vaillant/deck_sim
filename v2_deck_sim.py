#!/usr/bin/env python3
""" deck_sim_v2.py: Takes a deck of cards with specified type distribution
                    and calculates the proportion of subsets of hands of a
                    specified length which satisfy specified distributions.

    Variable Outline:
        pop_size: The size of the deck of cards.
        element_sizes: The size of each partition of the deck of cards.
        sample_size: The amount of cards being drawn from the deck.
        requirelist: The size of partitions which are compared
                     to the drawn cards.
        hit_array: A list of sequence representatives of subsets.
                   See functional outline.

    Method Outline:
        choose(n,k): Function courtesy of Andrew Dalke. Finds number of
                     subsets with size k of a set with size n.
        infoput(): Takes user input to define variables.
        seq_gen(): Uses recursion to generate hit_array.
                   See functional outline.
            
    Outlining the Mathematics:
        We solve the combinatorial problem of calculating the proportion of 
        subsets of size K with certain properties out of the set D of all
        subsets of size K.
        Set D has a partition P (containing p_1...p_n subsets of D). These 
        certain properties related to how many hands have a number of elements 
        in p_1...p_n. 

        Example: If P = {p_1, p_2}, we could find out how many hands of size
                 5 contain at least 2 elements of p_1.
"""

""" This module is deprecated, and its features will be merged with deck_sim in due time. """

## UTILITY FUNCTIONS ##
def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke.
    """
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

## COMMAND-LINE INTERFACE ##
def infoput():
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

def main():
    pop, ele, sam, req = testput()
    total = choose(pop,sam)
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
            product *= choose(ele[y], x[y])
        A[tuple(x)] = product/total
    return percentage_wrapper(A)
    
def testput():
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

            

