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
from typing import Dict, List, Tuple


class RandomNumberGenerator:
    """
    Instantiates the Pseudorandom number generator with a seed value.
    """

    # Decided that this was a reasonable number of values
    AMOUNT_OF_RANDOM_NUMBERS = 100000

    def __init__(self, seed: int, distribution_map: Dict[int, float]):
        self.seed = seed
        self.distribution_map = distribution_map
        self.random_numbers = generate_random_numbers(self.seed, self.AMOUNT_OF_RANDOM_NUMBERS, [])
        # We're gonna use a pointer to keep track of the next generated number to return
        # B/c the generated numbers is an array, we'll start at index 0
        self.pointer = 0
        self.values, self.cumulative_distribution = create_cumulative_distribution_tuple(self.distribution_map)

    def get_seed(self) -> int:
        return self.seed

    def get_random_number(self) -> int:
        normalized_random_value = self._get_next_random_number_from_prng()
        # self.cumulative_distribution will be naturally sorted, so we can use a binary search
        index_of_random_value = find_index_for_value_binary_search(self.cumulative_distribution,
                                                                   normalized_random_value)
        return self.values[index_of_random_value]

    def _get_next_random_number_from_prng(self) -> float:
        """
        Returns the next random number from the generated random number list
        """

        next_random_number = self.random_numbers[self.pointer]
        self.pointer = determine_next_pointer(self.pointer, self.random_numbers.__len__())

        return next_random_number

    def _get_random_numbers(self) -> List[float]:
        return self.random_numbers

    def _get_cumulative_distribution(self):
        return self.values, self.cumulative_distribution


def create_cumulative_distribution_tuple(distribution_map: Dict[int, float]) -> Tuple[List[int], List[float]]:
    """
    Create a tuple that contains the cumulative distribution for probabilities. E.g:
    1 => 0.25
    2 => 0.5
    7 => 0.25
    would translate to
    ([1, 2, 7], [0.25, 0.75, 1])
    """
    numbers = list(distribution_map.keys())
    distribution = list(distribution_map.values())

    cumulative_distribution = create_cumulative_distribution(distribution)

    return numbers, cumulative_distribution


def create_cumulative_distribution(distribution: List[float]) -> List[float]:
    """
    Create a set that contains the cumulative distribution for the probabilities. E.g:
    [0.25, 0.5, 0.25]
    would translate to
    [0.25, 0.75, 1]
    :param distribution
    :return: the cumulative distribution
    """
    # We need the initial value
    cumulative_distribution = [distribution[0]]

    for i in range(1, len(distribution)):
        next_distribution = cumulative_distribution[i - 1] + distribution[i]
        cumulative_distribution.append(next_distribution)

    return cumulative_distribution


def generate_random_numbers(seed: int,
                            amount_of_numbers_to_generate: int,
                            generated_numbers: List[float]) -> List[float]:
    """
    Generates N amount of random numbers based on a seed value.
    Internally uses the Lehmer random number generator algorithm found here:
    https://en.wikipedia.org/wiki/Lehmer_random_number_generator
    """
    # My research showed me that there are certain numbers that produce
    # good distributions with a high period. I'm following the advice
    # of using a MINSTD found here: https://en.wikipedia.org/wiki/Lehmer_random_number_generator
    # Please note that b = 0
    multiplier = 7 ** 5
    modulus = 2 ** 31 - 1

    # Initialize the random number using the seed
    next_random_number = generate_random_number(seed, multiplier, modulus)

    for i in range(amount_of_numbers_to_generate):
        next_random_number = generate_random_number(next_random_number, multiplier, modulus)
        generated_numbers += [next_random_number / modulus]

    return generated_numbers


def generate_random_number(number: int, multiplier: int, modulus: int) -> int:
    """
    Uses the Linear Congruence method to generate "random" numbers.
    f(x) = (a * x_1 + b) mod M
    https://en.wikipedia.org/wiki/Linear_congruential_generator

    Where:
    X, is the sequence of pseudo-random numbers
    m, ( > 0) the modulus
    a, (0, m) the multiplier
    b, (0, m) the increment
    X0,  [0, m) ??? Initial value of sequence known as seed
    """

    return (multiplier * number) % modulus


def determine_next_pointer(pointer: int, length_of_array: int) -> int:
    """
    Determines the next circular pointer for an array.
    If the pointer reaches the end of the array,
    it starts back at the beginning
    """
    is_end_of_array = pointer == length_of_array - 1

    return 0 if is_end_of_array else pointer + 1


def find_index_for_value(values: List[float], value_to_search_for: float) -> int:
    """
    Looks for the index that the value within the range of the search value. E.g.
    find_index_for_value_n([0.25, 0.3, 0.5, 0.7, 0.75, 0.8, 0.9, 1], 0.45)
    would return 2 b/c it's within the range 0.3 to 0.5 (inclusive)

    find_index_for_value_n([0.25, 0.3, 0.5, 0.7, 0.75, 0.8, 0.9, 1], 0.1)
    would return 0 b/c it's within the range 0.3 to 0.24 (inclusive)

    It needs the list to be sorted before the method is called.
    Worst case search takes O(n) on average O(n/2).

    A more effective solution would use a binary search or another divide and conquer algorithm.

    :param values:
    :param value_to_search_for:
    :return: the index
    """
    for i in range(len(values)):
        if values[i] == value_to_search_for:
            return i

        if values[i] < value_to_search_for <= values[i + 1]:
            return i + 1

    return 0


def find_index_for_value_binary_search(values: List[float], value_to_search_for: float) -> int:
    """
    Looks for the index that the value within the range of the search value. E.g.
    find_index_for_value_n([0.25, 0.3, 0.5, 0.7, 0.75, 0.8, 0.9, 1], 0.45)
    would return 2 b/c it's within the range 0.3 to 0.5 (inclusive)

    find_index_for_value_n([0.25, 0.3, 0.5, 0.7, 0.75, 0.8, 0.9, 1], 0.1)
    would return 0 b/c it's within the range 0.3 to 0.24 (inclusive)

    Uses a binary search

    :param values:
    :param value_to_search_for:
    :return: the index
    """
    low = 0
    high = len(values)
    mid = 0

    while low < high:
        mid = (low + high) // 2

        if values[mid] == value_to_search_for:
            return mid

        # If target is less than array element, then search the left side
        if value_to_search_for < values[mid]:

            # If target is greater than previous mid, return closest of two
            if mid > 0 and value_to_search_for > values[mid - 1]:
                higher_index = mid
                return get_higher_index(values[mid - 1], values[mid], value_to_search_for, higher_index)

            # Repeat for left half
            high = mid

        # Search right side of the array
        else:
            if mid < (len(values) - 1) and value_to_search_for < values[mid + 1]:
                higher_index = mid + 1
                return get_higher_index(values[mid], values[mid + 1], value_to_search_for, higher_index)

            low = mid + 1

    # Only single element left after search
    return mid


def get_higher_index(val1, val2, target, index):
    """
    Returns the higher value index if a value
    is in between 2 numbers. E.g.
    5 in array [4,6] would return index 1
    2 in array [4,6] would return index 0
    """
    if val1 < target <= val2:
        return index
    else:
        return index - 1
