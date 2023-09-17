from random import randint

from smartarray import SmartArray, ArrayItem
from sortedarray import SortedArray
from pympler import asizeof


def test_array_slot_attribute():
    big_arr = SmartArray(length=1_000_000, initial_value="0")
    print(f'\nclass SmartArray size: {asizeof.asizeof(big_arr)}')
    assert big_arr is not None
    print(f'array length: {big_arr.length()}')
    assert big_arr.length() == 1_000_000
    big_arr.set_at(big_arr.length() - 1, 1000000, 1000000)
    assert big_arr.at(big_arr.length() - 1)
    print(f'last element: {big_arr.at(big_arr.length() - 1)}')
    assert big_arr.at(big_arr.length() - 1) == {1000000: 1000000}


def test_array_creation_and_filtering():
    arr_0 = SmartArray()
    assert arr_0 is not None

    arr_1 = SmartArray(length=10, initial_value="empty")
    assert arr_1.length() == 10
    assert arr_1.at(arr_1.length()-1) == "empty"

    arr_2 = SmartArray(from_list=[1, 2, 3, 4, 5])
    assert arr_2.length() == 5
    assert arr_2[4] == 5

    arr_3 = SmartArray(from_dict={"k1": 1, "k2": 2, "k3": 3, "k4": 3, "k5": 5})
    assert arr_3.length() == 5
    same_values = arr_3.filter(by_value=3)
    assert len(same_values) == 2
    arr_3.set_at(3, value=4)
    same_values = arr_3.filter(by_value=3)
    assert len(same_values) == 1
    assert same_values[0] == {'k3': 3}
    assert arr_3[3] == {'k4': 4}


def test_array_insertion():
    arr = SmartArray()
    arr.append(value="item 1", key="i-1")
    arr.append(value="item 3", key="i-3")
    arr.insert(value="inserted item 0", key="key-i-0", at_index=0)
    arr.insert(value="inserted item 2", key="key-i-2", at_index=2)
    print(arr)
    assert arr.length() == 4
    assert arr.at(index=0) == {'key-i-0': 'inserted item 0'}
    assert arr.at(index=3) == {'i-3': 'item 3'}


def test_array_copy_and_sort():
    arr = SmartArray()
    for i in range(10):
        arr.append(i)

    arr_copy = arr.scopy()
    assert arr_copy.length() == 10
    print(f"\nOriginal array: {arr} .... Its copy: {arr_copy}")

    sorted_list = arr.sort()
    revers_sorted_list = arr_copy.sort(reverse=True)
    assert sorted_list != revers_sorted_list
    print(f"Sorted list: {arr.get_sorted_list()} .... Reversed sorted list: {arr_copy.get_sorted_list()}")


def test_array_modification():
    arr = SmartArray()
    for i in range(10):
        arr.append(i)
    assert arr.length() == 10
    arr.set_at(0, value=100)
    assert arr[0] == 100
    arr.delete(0)
    assert arr.length() == 9


def test_array_loop_modification():
    arr = SmartArray(from_list=[1, 2, 3, 4, 5])
    print(f'\noriginal array: {arr}')
    for index, el in enumerate(arr):
        val = arr[index]
        assert val == el
        arr[index] = val * val
        assert arr[index] == val * val

    print(f'squared array: {arr}')


def test_array_iterator_reset():
    arr = SmartArray(from_list=[1, 2, 3, 4, 5])
    print('\n')
    i = 0
    for el in arr:
        print(f'arr[{i}] == {el}')
        i += 1
        if i == 3:
            break

    n = 0
    for el in arr:
        print(f'arr[{n}]: {el}')
        assert el == arr[n]
        n += 1


def test_array_get_at_negative_index():
    print('\n')
    arr = SmartArray(from_list=[1, 2, 3, 4, 5])
    for index in range(-1, -6, -1):
        print(f'arr[{arr.length() - abs(index)}] == {arr.at(index)}')
        assert arr.at(index) == arr[arr.length() - abs(index)]


def test_array_get_first_next_prev_items():
    arr = SmartArray(from_list=[1, 2, 3, 4, 5])

    # test get_first and get_next
    item: ArrayItem | None = arr.get_item('first')
    assert item.value == arr[0]
    item = arr.get_next(item)
    assert item.value == arr[1]
    item = arr.get_next()   # in case of current is None returns first
    assert item.value == arr[0]

    # test get_last and get_prev
    item: ArrayItem | None = arr.get_item('last')
    assert item.value == arr[-1]
    item = arr.get_prev(item)
    assert item.value == arr[-2]
    item = arr.get_prev()   # in case of current is None return last
    assert item.value == arr[-1]

    # test while through all items in array
    summary = 0
    item: ArrayItem | None = arr.get_item()
    while item:
        summary += item.value
        item = arr.get_next(item)
    assert summary == 15

    item: ArrayItem | None = arr.get_item('last')
    while item:
        summary -= item.value
        item = arr.get_prev(item)
    assert summary == 0


def test_clear_array():
    arr = SmartArray(from_dict={"k1": 1, "k2": 2, "k3": 3, "k4": 3, "k5": 5})
    arr.clear()
    assert(arr.length() == 0)


def test_sorted_array_ascending():
    arr = SortedArray()
    for ind in range(1_000):
        val = randint(1, 10000)
        arr.append(val)

    print(f'\nAscending sorted array length: {arr.__len__()}')
    print(arr)
    arr.check_valid_array()
    assert(arr[0] < arr[len(arr)-1])


def test_sorted_array_descending():
    arr = SortedArray(reverse=True)
    for ind in range(1_000):
        val = randint(1, 10000)
        arr.append(val)

    print(f'\nDescending sorted array length: {arr.__len__()}')
    print(arr)
    arr.check_valid_array()
    assert(arr[0] > arr[len(arr)-1])


def test_sorted_array_unsorted():
    arr = SortedArray(unsorted=True)
    for ind in range(1_000):
        val = randint(1, 10000)
        arr.append(val)

    print(f'\nUnsorted array length: {arr.__len__()}')
    print(arr)
    assert(arr[0] != arr[len(arr)-1])



if __name__ == "__main__":
    arr1 = SmartArray()
