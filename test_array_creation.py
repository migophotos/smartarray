import pytest
from smartarray import SmartArray
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
    arr.append(val="item 1", key="i-1")
    arr.append(val="item 3", key="i-3")
    arr.insert(value="inserted item 0", key="key-i-0", at_index=0)
    arr.insert(value="inserted item 2", key="key-i-2", at_index=2)
    print(arr)
    assert arr.length() == 4
    assert arr.at(index=0) == {'key-i-0': 'inserted item 0'}
    assert arr.at(index=3) == {'i-3': 'item 3'}


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


def test_array_copying_and_sort():
    arr = SmartArray()
    for i in range(10):
        arr.append(i)

    arr_copy = arr.scopy()
    assert arr_copy.length() == 10
    sorted_list = arr.sort()
    revers_sorted_list = arr_copy.sort(reverse=True)
    assert sorted_list != revers_sorted_list
    print(f"\nOriginal array: {arr}\nIts copy: {arr_copy}")
    print(f"Sorted list: {arr.get_sorted_list()}\nReverse sorted list: {arr_copy.get_sorted_list()}")


def test_clear_array():
    arr = SmartArray(from_dict={"k1": 1, "k2": 2, "k3": 3, "k4": 3, "k5": 5})
    arr.clear()
    assert(arr.length() == 0)


if __name__ == "__main__":
    arr1 = SmartArray()
