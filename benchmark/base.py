import time

def make_dict(n):
	result = {}
	for i in range(n):
		result[i] = i % 1000
	return result


class Test:
    _TEST_METHODS = set()
    DICT_SIZES = {1, 10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000, 50_000_000}
    NUM_RUNS = 10

    NAME = NotImplemented

    @classmethod
    def method(cls, fn):
        # All test methods go on the base class,
        # we'll unpick them later
        Test._TEST_METHODS.add(fn)
        return fn

    @classmethod
    def all_test_classes(cls):
        if cls.NAME is not NotImplemented:
            yield cls
        for cls in cls.__subclasses__():
            yield from cls.all_test_classes()

    @classmethod
    def variants(cls):
        return cls.DICT_SIZES

    @classmethod
    def test_methods(cls):
        # This doesn't allow inheriting test methods..
        for attr in  cls.__dict__.values():  
            if attr in Test._TEST_METHODS:
                yield attr

    @classmethod
    def run_test(cls, variant, method):
        inst = cls(variant)
        before = time.perf_counter()
        result = method(inst)
        after = time.perf_counter()
        return result, (after-before) * 1_000

    def __init__(self, n):
        self.values = make_dict(n)
