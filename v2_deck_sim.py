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

           

