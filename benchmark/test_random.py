from benchmark.base import Test, make_dict

import random


class RandomSample(Test):

    NAME = "Retrieve random sample of items from dict"

    def __init__(self, n):
        super().__init__(n)
        random.seed(1)
        self.sample_size = min(len(self.values), 2000)

    @Test.method
    def use_list(self):
        return random.sample(list(self.values.items()), self.sample_size)

    @Test.method
    def proposed(self):
        return random.sample(self.values.items(), self.sample_size)


class RandomChoice(Test):

    NAME = "Retrieve random item from dict"

    def __init__(self, n):
        super().__init__(n)
        random.seed(1)
        self.sample_size = min(len(self.values), 2000)

    @Test.method
    def use_list(self):
        return random.choice(list(self.values.items()))

    @Test.method
    def proposed(self):
        return random.choice(self.values.items())
