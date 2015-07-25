# deck_sim

Hypergeometric distribution calculator. Takes a sample size and a symbol distribution array and returns the probability of any particular distribution of symbols being drawn.

InductiveDeck does the calculation by drawing randomly from the population repeatedly and dividing each result by the total number of trials. Naturally, this is terribly inefficient and should not be used - it exists only as an early draft and a curiosity.

HypergeometricDeck implements the calculations for hypergeometric probability proper. More information can be found at <a href>https://en.wikipedia.org/wiki/Hypergeometric_distribution</a> regarding the equations used.

PercentageWrapper takes the output of the Deck outputs and allows users to display the data as they so choose. 
