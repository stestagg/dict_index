from benchmark.base import Test, make_dict

class GetLastKeyWithHoles(Test):

    NAME = "Get last key from a dict that has had entries removed (branch misses)"

    REMOVE_EVERY = 10

    def __init__(self, n):
        num_to_remove = n // self.REMOVE_EVERY
        n_adjusted = n + num_to_remove
        super().__init__(n_adjusted)
        for i in range(self.REMOVE_EVERY//2, n, self.REMOVE_EVERY):
            del self.values[i]
        assert len(self.values) == n

    @Test.method
    def use_list(self):
        return list(self.values)[-1]

    @Test.method
    def use_iter(self):
        return next(reversed(self.values.keys()))

    @Test.method
    def proposed(self):        
        return self.values.keys()[-1]
