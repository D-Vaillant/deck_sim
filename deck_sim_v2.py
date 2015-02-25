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
            
    Functional Outline:
        We solve the combinatorial problem of calculating the proportion of 
        subsets of size K with certain properties out of the set D of all
        subsets of size K.
        Set D has a partition P (containing p_1...p_n subsets of D). These 
        certain properties related to how many hands have a number of elements 
        in p_1...p_n. 

        Example: If P = {p_1, p_2}, we could find out how many hands of size
                 5 contain at least 2 elements of p_1.
"""
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

''' Takes input, returns a tuple of the relevant variables. '''
def infoput():
    element_sizes = []
    pop_size = int(input('How many cards total? - '))
    var_1 = int(input('How many types of non-blank cards? - '))
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
    return pop_size, element_sizes, sample_size, requirelist

def main():
    pop, ele, sam, req = infoput()
    total = choose(pop,sam)
    hit_array = []
    ''' Generates a list of representative sequences recursively.
        See outline for details. '''
    
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
            if temp_rem == 0:
                temp_list.append(rem)
                for q in range(p+1, len(ele)): temp_list.append(0)
                hit_array.append(temp_list)
                return None
            else:
                temp_list.append(i)
                seq_gen(temp_list, p+1, temp_rem)

    seq_gen([], 0, sam)
    for x in range(len(hit_array)):
        hit_array[x] = tuple(hit_array[x])

    A = []
    for x in hit_array:
        product = 1
        for y in range(len(x)):
            product *= choose(ele[y], x[y])
        A.append((x, product/total))
    
def testput():
    return 60, [20, 20, 10, 10], 7, 2

class percentage_wrapper():
    def __init__(self, memory):
        self.mem = memory

    def select(self, subset):
        if len(subset) != len(memory[0][0]):
            return None
        
    
    
    
    


