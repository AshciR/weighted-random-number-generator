from typing import List

from RandomNumberGenerator import RandomNumberGenerator


def main():
    # Test Data, the distribution has to add up to 1.0
    sample_dist = {
        1: 0.2,
        2: 0.05,
        7: 0.25,
        9: 0.1,
        11: 0.4
    }

    print('Distribution:')
    print(sample_dist)
    # Arbitrary seed value (the meaning of life)
    seed = 42
    # Instantiate the random number generator
    rng = RandomNumberGenerator(seed, sample_dist)

    test_random_number_generator(rng)


def test_random_number_generator(rng):
    random_numbers = []
    for i in range(10_000_000):
        num = rng.get_random_number()
        random_numbers.append(num)
    freq_map = create_frequency_map(random_numbers)
    print("\nNumber of generated values: %d " % (len(random_numbers)))
    print('Frequency Map')
    print(freq_map)
    normalized_freq_map = calculate_normalized_map(freq_map, len(random_numbers))
    print('\nNormalized Frequency Map')
    print(normalized_freq_map)


def create_frequency_map(numbers: List[int]):
    freq_map = {}

    for num in numbers:
        if num in freq_map:
            freq_map[num] = freq_map[num] + 1
        else:
            freq_map[num] = 1

    return freq_map


def calculate_normalized_map(freq_map, total_numbers):
    normalized_map = {}
    for key in freq_map:
        normalized_map[key] = freq_map[key] / total_numbers

    return normalized_map


if __name__ == '__main__':
    main()
