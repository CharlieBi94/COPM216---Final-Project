import math
import random
import matplotlib.pyplot as plt
from numpy import double


class SampleSet:
    def __init__(self, base_temperature: int = None):
        self._data: float = 0
        self.base_temperature = base_temperature or 20
        self.x = 0

    # this is public
    @property
    def get_data(self) -> float:
        self._data: float = self._get_random()
        # return self.base_temperature + (self._data * 10)  # make the random value bigger
        self.x += 1
        return self.generate_data(x=self.x, a=5, d=self.base_temperature)

    random_dict = {
        'value': random.randint(3, 7) / 10,  # base random value to be used
        'delta': 0.004,
        'cycle': 0}  # each cycle, the 'trend' is decided

    # this is private
    def _get_random(self) -> float:
        # make a big flow
        if self.random_dict['cycle'] == 0:
            self.random_dict['cycle'] = random.randint(2, 8) * 10
            self.random_dict['delta'] = -1
        self.random_dict['cycle'] -= 1
        self.random_dict['value'] += self.random_dict['delta']

        # make it fluctuate like a real data
        self.random_dict['value'] += random.randint(-30, 30) / 1000

        # generating values from 0 to 1
        if self.random_dict['value'] < 0:
            self.random_dict['delta'] = abs(self.random_dict['delta'])
            self.random_dict['value'] = random.randint(50, 150) / 1000
        if self.random_dict['value'] > 1:
            self.random_dict['delta'] = abs(self.random_dict['delta']) * -1
            self.random_dict['value'] = random.randint(850, 950) / 1000
        return round(self.random_dict['value'], 2)

    # creates a sin shape
    def generator_sine(self, x: float, a: float = 1, b: float = 1, c: float = 0, d: float = 0) -> double:
        p_s = random.uniform(-c, c * math.pi)
        ran_range = random.gauss(a, a / 2)
        height = random.uniform(d - random.uniform(0, d / 2), d + random.uniform(0, d / 2))
        number = double(ran_range * math.sin(b * x * math.pi + p_s) + height)
        return number

    # adds variance to number
    def generator_chaos(self, mean: double, std: float = 1) -> double:
        return double(random.gauss(mean, std))

    # generates numbers 1 - 3 in a uniform way, using 100 for more 'consistency'
    def pattern_decider(self, odds1=50, odds3=25) -> int:
        number = random.uniform(0, 100)
        if number <= odds1:
            return 0
        elif number > 100 - odds3:
            return 2
        else:
            return 1

    def generate_data(self, x: float, a: float = 1, b: float = 1, c: float = 0, d: float = 0) -> double:
        pattern = self.pattern_decider()
        pattern_value = 0.0
        if pattern == 0:
            pattern_value = self.generator_sine(x, a, b, c, d)
        elif pattern == 1:
            pattern_value = self.generator_sine(x, a, b, c + 90, d)
        elif pattern == 2:
            pattern_value = self.generator_sine(x, a, b, c - 90, d)

        value = self.generator_chaos(pattern_value)
        return value
