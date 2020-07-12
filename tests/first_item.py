
from runner import TestRunner


class FirstItem(TestRunner):
    DESC = "Retrieve the first item"

    def proposed(self, obj):
        obj.items()[0]

    def existing(self, obj):
        list(obj.items())[0]


if __name__ == '__main__':
    FirstItem().do_test()