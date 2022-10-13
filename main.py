# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from RandomNumberGenerator import RandomNumberGenerator


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    sample_dist = {
        1: 0.2,
        2: 0.05,
        7: 0.25,
        9: 0.1,
        11: 0.4
    }
    rng = RandomNumberGenerator(23487, sample_dist)
    # print(rng.get_seed())
    # print(rng._get_random_numbers())
    # print()
    # for i in range(15):
    #     print(rng._get_next_random_number_from_prng())
    #
    # print(rng._get_cumulative_distribution())
    freq_map = {}
    for i in range(10000):
        print(rng.get_random_number())
        num = rng.get_random_number()
        if num in freq_map:
            freq_map[num] = freq_map[num] + 1
        else:
            freq_map[num] = 1

    print(freq_map)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
