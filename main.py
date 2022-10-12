# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from RandomNumberGenerator import RandomNumberGenerator


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    sample_dist = {
        1: 0.25,
        2: 0.5,
        7: 0.25
    }
    rng = RandomNumberGenerator(1000, sample_dist)
    print(rng.get_seed())
    print(rng.get_random_numbers())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
