from benchmark.base import Test, make_dict
import itertools

class GetFirstKey(Test):

    NAME = "Get first key"

    @Test.method
    def use_list(self):
        """
        Calling list on the dict
        """
        return list(self.values)[0]

    @Test.method
    def use_iter(self):
        """
        Calling iter on the keys
        """
        return next(iter(self.values.keys()))

    @Test.method
    def proposed(self):
        """
        Using keys indexing
        """
        return self.values.keys()[0]


class GetFirstItem(Test):

    NAME = "Get first item"

    @Test.method
    def use_list(self):
        """
        Calling list on the dict
        """
        return list(self.values.items())[0]

    @Test.method
    def use_iter(self):
        """
        Calling iter on the view
        """
        return next(iter(self.values.items()))

    @Test.method
    def proposed(self):
        """
        Using view indexing
        """
        return self.values.items()[0]


class GetLastKey(Test):

    NAME = "Get last key"

    @Test.method
    def use_list(self):
        return list(self.values)[-1]

    @Test.method
    def use_iter(self):
        return next(reversed(self.values.keys()))

    @Test.method
    def proposed(self):
        return self.values.keys()[-1]



class IterKeys(Test):

    NAME = "Iterate over all keys"

    @Test.method
    def list_index(self):
        """ This is a bad way of doing this """
        keys = list(self.values.keys())
        for i in range(len(keys)):
            last_key = keys[i]
        return last_key

    @Test.method
    def list_iter(self):
        """ This is a bad way of doing this """
        keys = list(self.values.keys())
        for key in keys:
            last_key = key
        return last_key

    @Test.method
    def direct_iter(self):
        for key in self.values.keys():
            last_key = key
        return last_key

    @Test.method
    def keys_index(self):
        """
        Using keys indexing. This approach is *not* recommended,
        but included here to assess the performance of sitations
        where this may be done in 'error'.
        """
        keys = self.values.keys()
        for i in range(len(keys)):
            last_key = keys[i]
        return last_key

    @Test.method
    def iter_keys(self):
        """
        Using the sensible iter()
        """
        for key in iter(self.values.keys()):
            last_key = key
        return last_key



class IterItems(Test):

    NAME = "Iterate over all items"

    @Test.method
    def list_index(self):
        """ This is a bad way of doing this """
        items = list(self.values.items())
        for i in range(len(items)):
            last_item = items[i]
        return last_item

    @Test.method
    def list_iter(self):
        """ This is a bad way of doing this """
        items = list(self.values.items())
        for item in items:
            last_item = item
        return last_item

    @Test.method
    def direct_iter(self):
        for item in self.values.items():
            last_item = item
        return last_item

    @Test.method
    def items_index(self):
        """
        Using items indexing. This approach is *not* recommended,
        but included here to assess the performance of sitations
        where this may be done in 'error'.
        """
        items = self.values.items()
        for i in range(len(items)):
            last_item = items[i]
        return last_item

    @Test.method
    def iter_items(self):
        """
        Using the sensible iter()
        """
        for item in iter(self.values.items()):
            last_item = item
        return last_item


class GetMiddleValue(Test):

    NAME = "Get a value from the middle"

    def __init__(self, n):
        super().__init__(n)
        self.index = min((n // 2), n-1)

    @Test.method
    def use_list(self):
        """
        Calling list on the dict
        """
        return list(self.values.values())[self.index]

    @Test.method
    def use_iter(self):
        """
        Calling iter on the keys
        """
        return next(itertools.islice(
            self.values.values(), 
            self.index, 
            self.index+1)
        )

    @Test.method
    def iter_2(self):
        """
        Count over the iter results
        """
        left = self.index
        for value in self.values.values():
            if left == 0:
                return value
            left -= 1

    @Test.method
    def proposed(self):
        """
        Using keys indexing
        """
        return self.values.values()[self.index]
