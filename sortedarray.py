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
        self.__append(element)

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

    def __append(self, element, start: int | None = None, stop: int | None = None) -> None:
        prev_id = -1
        if self.reverse:
            start_ind = start or self.__len__() - 1
            stop_ind = stop or -1
            for ind in range(start_ind, stop_ind, -1):
                if element < self[ind]:
                    super().insert(ind+1, element)
                    return

                if element >= self[ind]:
                    prev_id = ind + 1

            if prev_id > 0:
                super().insert(0, element)
        else:
            start_ind = start or 0
            stop_ind = stop or self.__len__()
            for ind in range(start_ind, stop_ind):
                if element <= self[ind]:
                    super().insert(ind, element)
                    return

                if element > self[ind]:
                    prev_id = ind

            if prev_id >= 0:
                super().insert(prev_id+1, element)
            else:
                print(f'Not inserted value {element} at index {prev_id}')


if __name__ == "__main__":
    arr = SortedArray(reverse=False)
    for ind in range(3_000):
        val = randint(1, 10000)
        # print(f'{val}')
        arr.append(val)

    print(f'\nSorted array length: {arr.__len__()}')
    print(arr)
    arr.check_valid_array()

    arr = SortedArray(reverse=True)
    for ind in range(3_000):
        val = randint(1, 10000)
        # print(f'{val}')
        arr.append(val)
    print(f'\nReverse sorted array length: {arr.__len__()}')
    print(arr.__len__())
    print(arr)
    arr.check_valid_array()

    arr = SortedArray(unsorted=True)
    for ind in range(3_000):
        val = randint(1, 10000)
        # print(f'{val}')
        arr.append(val)
    print(f'\nUnsorted array length: {arr.__len__()}')
    print(arr.__len__())
    print(arr)

