"""
This is a Pseudorandom Number Generator (PRNG) that will
generate values based on a given distribution.

Because of this requirement:
"The class or module should support the ability to replay the same sequence of random numbers
regardless of platform it is compiled on and regardless of whether the program is directly translated to
another programming language." the class should not use package or library that will produce random numbers.

In order to accomplish the deterministic PNRG, I will do the following steps.
1. Create a PNRG. From my research, I learnt about the Linear Congruence method
which I will use to generate numbers between 0 and 1 (inclusive)

2. Create a set that contains the cumulative distribution for the probabilities. E.g:
1 => 0.25
2 => 0.5
7 => 0.25
would translate to
[0.25, 0.75, 1]
[1, 2, 7]

3. Use the PRNG to generate a number between 0 to 1, and depending on the number, I can assign a value. E.g:
- if 0.4 was produced, that falls between index 0.25 and 0.75, choose 0.75 which maps to 2
- if 0.8 was produced, that falls between index 0.75 and 0.1, choose 0.75 which maps to 7

Things to consider:
- The random number generator will be called billions of times, so performance is important.
  -- I want a performance of ideally O(log n)
- The size of the set of numbers will typically be at least a thousand, possibly well into the millions
  -- Since the set can be in the millions, the discrete size for the cumulative can
     be as small as 0.000001 (1/1e6). The PNRG will need to account for this.
"""


class RandomNumberGenerator:
    """
    Instantiates the Pseudorandom number generator with a seed value.
    """

    def __init__(self, seed: int):
        self.seed = seed

    def get_seed(self):
        return self.seed
