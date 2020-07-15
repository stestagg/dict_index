from benchmark.base import Test, make_dict

import random

INDICES = [random.randint(0, 100_000_000_000) for i in range(100_000)]


class RepeatedAccess(Test):

    """
    Purpose of this test is to measure the overeheads of just the index
    operation, while reducing the cost of constructing the initial objects
    used for indexing
    """

    NAME = "Access 100k items by index"

    def __init__(self, n):
        super().__init__(n)
        self.indices = [i % n for i in INDICES]

    @Test.method
    def use_list(self):
        items = list(self.values.items())
        for i in self.indices:
            last = items[i]
        return last

    @Test.method
    def proposed(self):
        items = self.values.items()
        for i in self.indices:
            last = items[i]
        return last
