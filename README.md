# Weighted Random Number Generator

## What does it do?
It'll provide you a random number based on a weighted distribution.
E.g.
```python
sample_dist = {
        1: 0.2,
        2: 0.05,
        7: 0.25,
        9: 0.1,
        11: 0.4
}
```
1 would be returned 20% of the time
7 would be returned 25% of the time

etc..

## Requirements
- Python 3 (N.B it will not work with Python 2!)

## How to run
Run the `main.py` file
```shell
python main.py
```

## Additional Notes:
`RandomNumberGenerator.py` contains the relevant random number generation code
