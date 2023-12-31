from typing import List


class ArrayItem:
    """

    """
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None, next_item=None, prev_item=None):
        self.key = key
        self.value = value
        self.prev = prev_item
        self.next = next_item

    def get(self):
        if self.key is None:
            return self.value
        else:
            return {self.key: self.value}


class SmartArray:
    __slots__ = ("__next", "__last", "__items", "__length", "__sorted_list")

    def __init__(self, length=0, initial_value=0, from_list: list | None = None, from_dict: dict | None = None):
        self.__next = None
        self.__last = None
        self.__items = None
        self.__length = 0
        self.__sorted_list = None

        if length:
            self.__add(initial_value, n=length)

        if from_list is not None:
            self.from_list(from_list)
        if from_dict is not None:
            self.from_dict(from_dict)

        self.__length = self.length()

    def __str__(self):
        result = "["
        item = self.__items
        while item:
            if type(item.key) == str:
                key_str = f"'{item.key}'"
            else:
                key_str = f"{item.key}"

            if type(item.value) == str:
                val_str = f"'{item.value}'"
            else:
                val_str = f"{item.value}"

            if len(result) > 1:
                result += ","

            if key_str.find("None") >= 0:
                result += f"{val_str}"
            else:
                result += f"{key_str}: {val_str}"

            item = item.next

        result += "]"
        return result

    def __iter__(self):
        self.__next = None
        return self

    def __next__(self):
        if self.__next is None:
            self.__next = self.__items

        elif self.__next.next:
            self.__next = self.__next.next

        else:
            self.__next = None
            raise StopIteration

        return self.__next.value if self.__next.key is None else {self.__next.key: self.__next.value}

    def __getitem__(self, item):
        return self.at(index=item)

    def __setitem__(self, index, value):
        if type(value) == dict:
            for k in value:
                self.set_at(index=index, value=value[k], key=k)
        else:
            if isinstance(index, (str, float)) or index < 0:
                raise ValueError(f"index must be integer in range from 0 up to length of array -1")
            if index > self.length():
                raise IndexError(f"index {index} out of range")
            self.set_at(index=index, value=value)

    def __delitem__(self, key):
        self.delete(key=key)

    def __count(self) -> int:
        """
        Count the length of SmartArray instance
        :return: the count of items, 0 - in case of empty
        """
        item = self.__items
        length = 0
        while item:
            length += 1
            item = item.next
        return length

    def __add(self, value, key=None, n=1):
        prev_item = None if not self.__last else self.__last

        for index in range(0, n):
            item = ArrayItem(value=value, key=key, prev_item=prev_item)

            if not self.__items:
                self.__items = item
                prev_item = item
                self.__last = item
            else:
                prev_item.next = item
                prev_item = item
                self.__last = prev_item

        self.__length = self.__count()

    def __at(self, index=-1, key=None, value=None) -> ArrayItem | None:
        """
        Find and return an ArrayItem by index or first occurrence of item with specified key or value
        :param index:
        :param key:
        :param value:
        :return: ArrayItem or None
        """
        if index > self.__length // 2:
            item = self.__last
            n = self.__length - 1
            while item:
                if index == n or (key and key == item.key) or (value and value == item.value):
                    return item
                n -= 1
                item = item.prev
        else:
            item = self.__items
            n = 0
            while item:
                if index >= 0 and index == n:
                    return item
                if (key and key == item.key) or (value and value == item.value):
                    return item
                item = item.next
                n += 1

        return None

    def __sort_by_value(self, e):
        return "" if e["value"] is None else e["value"]

    def __sort_by_key(self, e):
        return "" if e["key"] is None else e["key"]

    def from_list(self, from_list):
        for il in from_list:
            self.__add(il)

    def from_dict(self, from_dict: dict):
        for dk in from_dict:
            self.__add(from_dict[dk], key=dk)

    def sort(self, reverse: bool = False, sort_by: str = "val"):
        """
        Sort an array by "val" or by "key" and return the new list with sorted elements
        :param reverse: True - ascending sort order, False - descending sort order
        :param sort_by: "val" - sort by values, "key" - sort by keys
        :return: the new list of sorted items in form: [{key:value},{key:value},...], or [value, value, ...]
        """
        list_to_sort = self.filter()
        if len(list_to_sort):
            if sort_by == "key":
                list_to_sort.sort(reverse=reverse, key=self.__sort_by_key)
            else:
                list_to_sort.sort(reverse=reverse, key=self.__sort_by_value)

            self.__sorted_list = []
            for item in list_to_sort:
                if item['key'] is None:
                    self.__sorted_list.append(item['value'])
                else:
                    self.__sorted_list.append(item)

            return self.__sorted_list

    def get_sorted_list(self) -> List:
        """
        :return: return the previously sorted list
        """
        return self.__sorted_list

    def length(self) -> int:
        """
        Count the length of SmartArray instance
        :return: the count of items, 0 - in case of empty
        """
        return self.__count()

    def set_at(self, index, value=None, key=None):
        """
        Set the value and key to item at specified index
        :param index: the index of item that will be changed
        :param value: optional parameter that will be stored
        :param key: optional parameter that will bbe stored
        :return: [bool] True in case of item was found and changed
        """
        item: ArrayItem = self.__at(index=index)
        if item:
            item.key = key if key else item.key
            item.value = value if value else item.value
            return True
        return False

    def insert(self, value, key=None, at_index=0):
        """
        Insert the new ArrayItem at specified position
        :param value: new ArrayItem value
        :param key: new ArrayItem key (optional)
        :param at_index: new ArrayItem position inside array, Default is 0
        :return: False in case of index is out of length
        """
        cur_item = self.__at(at_index)
        if cur_item is None:
            return False

        new_item = ArrayItem(value=value, key=key)

        if at_index == 0:
            new_item.next = self.__items
            new_item.next.prev = new_item
            self.__items = new_item
        else:
            new_item.next = cur_item
            new_item.prev = cur_item.prev
            new_item.prev.next = cur_item.prev = new_item

        self.__length = self.__count()
        return True

    def clear(self):
        """
        Delete all items from SmartArray
        :return: None
        """
        while self.length():
            self.delete(self.length()-1)
        self.__sorted_list = None

    def delete(self, at_index=-1, value=None, key=None):
        """
        Delete item from array. ArrayItem may be identified by its position, by value or by key
        In case of ArrayItem, specified by value or key only the first found item will be deleted
        :param at_index: an index of item that must be deleted
        :param value: the item with this value will be deleted
        :param key: the item with this ey will be deleted
        :return: False in case of out of index
        """
        del_item = self.__at(at_index, key=key, value=value)
        if del_item is None:
            return False

        if at_index == 0:
            self.__items = del_item.next
            if del_item.next is not None:
                del_item.next.prev = None
            if self.__length == 1:
                self.__last = None
            del del_item
        else:
            del_item.prev.next = del_item.next
            if del_item.next:
                del_item.next.prev = del_item.prev
            else:
                self.__last = del_item.prev

            del del_item

        self.__length = self.__count()
        return True

    def index(self, value=None, key=None) -> int:
        """
        Find the index of first occurrence of item with specified value or key
        :param value: find item by value
        :param key: find value by key
        :return: an index of first occurrence of item or -1 in case of item not found
        """
        index = -1
        item = self.__items
        while item:
            if value and value == item.value:
                index += 1
                break
            if key and key == item.key:
                index += 1
                break
            item = item.next
            index += 1

        return index

    def value(self, index: int = -1, key=None):
        """
        Find and return the value of item specified by index or first occurrence of item, specified by key
        :param index: an index of item
        :param key: a key of item
        :return: value or None in case of item was not found
        """
        item = self.__at(index, key=key)
        if item is None:
            return None

        return item.value

    def key(self, index: int = -1, value=None):
        """
        Find and return the key of item specified by index or first occurrence of item, specified by value
        :param index: an index of item
        :param value: a value of item
        :return: key or None in case of item was not found or item has not key
        """
        item = self.__at(index, value=value)
        if item is None:
            return None

        return item.key

    def at(self, index: int = -1, key=None, value=None):
        """
        Find an item by specified parameter and return the {key: value} or value in case of key is None
        :param index: return an item by specified index
        :param key: return the first occurrence of item with specified key
        :param value: return the first occurrence of item with specified value
        :return: the dict of item parameters: key and value in form {item.key: item.value}, or just the value in
        case of key is None, or None in case of item was not found
        """
        if index < 0:
            index = self.length() - abs(index)
        item = self.__at(index, key=key, value=value)
        if item is None:
            return None

        return item.get()

    def get_item(self, start_from: str = 'first') -> ArrayItem:
        """
        Get reference on first or last item in array
        :param start_from: str 'first' or 'last'
        :return: reference on first or last item in array, or None in case of empty array
        """
        if start_from == 'first':
            return self.__items
        if start_from == 'last':
            return self.__last

    def get_next(self, current: ArrayItem | None = None) -> ArrayItem:
        """
        Get next item after current or None in case current item is last
        :param current: reference on current item. if None returns the first ArrayItem reference
        :return: next item after current or None in case current item is last
        """
        if current is None:
            return self.__items
        return current.next

    def get_prev(self, current: ArrayItem | None = None) -> ArrayItem:
        """
        Get item before current or None in case current item is first
        :param current: reference on current item. If None returns the last ArrayItem reference
        :return: item before current or None in case current item is first
        """
        if current is None:
            return self.__last
        return current.prev

    def filter(self, by_value=None, by_key=None) -> List[{}]:
        """
        Finds all concurrences specified by key or by value, builds and
        returns the list of pairs in form [{key:value}, {key:value}, ...]
        In case of two parameters are None this function return the list of all pairs

        :param by_value: [any] find all concurrences by specified value
        :param by_key: [any]  find all concurrences by specified key

        :return: List: the list of pairs in form [{key:value}, {key:value}, ...],
            or empty list in case of no one items was found

        Example
                print(arr.filter(by_key="key")
        """
        filtered = []
        item = self.__items
        while item:
            if by_key and by_key == item.key:
                filtered.append({item.key: item.value})
            if by_value and by_value == item.value:
                filtered.append({item.key: item.value})
            if by_key is None and by_value is None:
                filtered.append({"key": item.key, "value": item.value})
            item = item.next
        return filtered

    def scopy(self):
        """
        Returns the safe copy of this array
        :return:
            SmartArray: the copy of current instance of SmartArray
        """
        new_arr = SmartArray()
        item = self.__items
        while item:
            new_arr.append(item.value, key=item.key)
            item = item.next
        return new_arr

    def append(self, value, key=None, count: int = 1) -> int:
        """
        Append the new item at the end of SmartArray instance
        :param value: [any] - the value
        :param key: [any] - optional parameter
        :param count: [int] - optional parameter, the count of items to be appended
        :return: the new length of array
        """
        self.__add(value=value, key=key, n=count)
        return self.length()


if __name__ == "__main__":
    val = 0
    arr = SmartArray(from_list=[1, 2, 3, 4, 5])
    print(f'original array: {arr}')
    for i, el in enumerate(arr):
        val = arr[i]
        arr[i] = val * val

    print(f'squared array: {arr}')
    for i, el in enumerate(arr):
        val = arr[i]
        arr[i] = val // (i + 1)
    print(f'original array: {arr}')

    i = 0
    for el in arr:
        print(f'arr[{i}] == {el}')
        i += 1
        if i == 3:
            break

    for el in arr:
        print(f'{el}')

    last_el = arr.at(-2)
    print(last_el)

    for i in range(-1, -6, -1):
        print(f'arr[{arr.length() - abs(i)}] == {arr.at(i)}')
