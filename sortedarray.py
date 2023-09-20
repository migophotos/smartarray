from random import random, randint


class SortedArray(list):
    def __init__(self, reverse: bool = False, unsorted: bool = False):
        super().__init__()
        self.reverse = reverse
        self.unsorted = unsorted

    def append(self, element) -> None:
        if self.__len__() == 0 or self.unsorted:
            super().append(element)
            return

        left = 0
        right = len(self) - 1

        while left <= right:
            mid = (left + right) // 2

            if not self.reverse:
                if element < self[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if element > self[mid]:
                    right = mid - 1
                else:
                    left = mid + 1

        self.insert(left, element)

    def check_valid_array(self):
        prev_val = None
        for el in self:
            if prev_val is None:
                prev_val = el
                continue
            if not self.reverse and el < prev_val:
                raise IndexError
            if self.reverse and el > prev_val:
                raise IndexError
            prev_val = el


if __name__ == "__main__":
    arr = SortedArray(reverse=False)
    for ind in range(100_000):
        val = randint(1, 100000)
        # print(f'{val}')
        arr.append(val)

    print(f'\nSorted array length: {arr.__len__()}')
    arr.check_valid_array()

    arr = SortedArray(reverse=True)
    for ind in range(10000):
        val = randint(1, 100000)
        # print(f'{val}')
        arr.append(val)
    print(f'\nReverse sorted array length: {arr.__len__()}')
    arr.check_valid_array()

    arr = SortedArray(unsorted=True)
    for ind in range(10_000):
        val = randint(1, 10000)
        # print(f'{val}')
        arr.append(val)
    print(f'\nUnsorted array length: {arr.__len__()}')

