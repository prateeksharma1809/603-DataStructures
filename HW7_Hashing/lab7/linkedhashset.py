from typing import Iterator, Any
from set import SetType

"""
description: A homemade node with 3 pointers to previous, next and fwd links
"""

__author__ = "Prateek Sharma"


class ChainNode:
    __slots__ = ("_data", "_prev", "_next", "_fwd")
    _data: Any
    _prev: "ChainNode"
    _next: "ChainNode"
    _fwd: "ChainNode"

    """getters and setters for the instance variables"""

    def get_data(self) -> Any:
        return self._data

    def set_data(self, data) -> None:
        self._data = data

    def get_prev(self) -> "ChainNode":
        return self._prev

    def set_prev(self, prev) -> None:
        self._prev = prev

    def get_next(self) -> "ChainNode":
        return self._next

    def set_next(self, next) -> None:
        self._next = next

    def get_fwd(self) -> "ChainNode":
        return self._fwd

    def set_fwd(self, fwd) -> None:
        self._fwd = fwd

    def __init__(
        self,
        obj: Any,
        prev: "ChainNode" = None,
        next: "ChainNode" = None,
        fwd: "ChainNode" = None,
    ):
        """
        Create a new node.
        :param obj: the item to stored in the node
        :param prev: the previous node inserted in the set (ordering link)
        :param next: the next node inserted in the set (ordering link)
        :param fwd: the next node in the bucket's chain (hash table link)
        :return: None
        """
        self._data = obj
        self._next = next
        self._prev = prev
        self._fwd = fwd

    def __repr__(self) -> str:
        """
        Return a string with the string representation of the object
        in this node and the object of the node to which it is linked by
        the fwd link.
        This function should not be called for a circular
        list. The format of the string is as follows:
          {obj1} -> {obj2} -> {obj3}
        """
        return "{" + repr(self._data) + "} -> {" + repr(self._next) + "}"

    def __str__(self) -> str:
        """
        Return the string representation of the object in this node.
        """
        return str(self._data)


"""
description: A homemade hash table that remembers insertion order

"""


class LinkedHashSet(SetType):
    __slots__ = (
        "_load_limit",
        "_hash_function",
        "_table",
        "_capacity",
        "_collisions",
        "_front",
        "_back",
    )
    _table: list["ChainNode"]
    _capacity: int
    _collisions: int
    _front: "ChainNode"
    _back: "ChainNode"

    def __init__(
        self,
        initial_num_buckets: int = 1,
        load_limit: float = 0.75,
        hash_function=hash,
    ):
        """
        This abstract class just keeps the state information about the
        'size', or number of entries in the set.
        (So, all sets must manually maintain their number of entries.)
        """
        super().__init__()
        self._capacity = 10 if initial_num_buckets < 10 else initial_num_buckets
        self._load_limit = load_limit  # it should be load factor
        self._hash_function = hash_function
        self._table = initial_num_buckets * [None]
        self._front = None
        self._back = None

    def __len__(self) -> int:
        """
        Return the number of elements in this set.
        :return: the number of elements in the set.
        """
        return self.size

    def contains(self, obj: Any) -> bool:
        """
        Is the given obj in the set?
        The answer is determined through use of the '==' operator,
        i.e., the __eq__ method.
        :return: True iff obj or its equivalent has been added to this set
                       and not removed
        """
        hash_value = self._hash_function(obj) % self._capacity
        cursor = self._table[hash_value]
        if cursor is None:
            return False
        cursor = self._skip_unitil_object_found_or_fwd_is_none(cursor, obj)
        if cursor.get_data() == obj:
            return True
        return False

    def _skip_unitil_object_found_or_fwd_is_none(
        self, cursor: "ChainNode", obj: Any
    ) -> "ChainNode":
        """Method to iterate over linked list to find the element == operator
        :param: cursor: current postion of the cursor
        obj: object to be found
        :returns cursor after finding or reaching end
        """
        while cursor.get_data() != obj and cursor.get_fwd() is not None:
            cursor = cursor.get_fwd()
        return cursor

    def add(self, obj):
        """
        Insert a new object into the hash table and remember when it was added
        relative to other calls to this method. However, if the object is
        added multiple times, the hash table is left unchanged, including the
        fact that this object's location in the insertion order does not change.
        Double the size of the table if its load_factor exceeds the load_limit.
        :param obj: the object to add
        :return: True iff obj has been added to this set
        """
        hash_value = self._hash_function(obj) % self._capacity
        cursor = self._table[hash_value]
        if cursor is None:
            self._add_to_linked_list(obj)
            self._table[hash_value] = self._back
            self.size += 1
        else:
            cursor = self._skip_unitil_object_found_or_fwd_is_none(cursor, obj)
            if cursor.get_fwd() is None and cursor.get_data() != obj:
                self._add_to_linked_list(obj)
                cursor.set_fwd(self._back)
                self.size += 1
        if self.size / self._capacity > self._load_limit:
            self._rehash(self._capacity * 2)

    def _add_to_linked_list(self, obj: Any) -> None:
        """Method to add data to the linked list
        :param obj: object to be added
        """
        new_node = ChainNode(obj)
        if self._front is None:
            self._front = new_node
        else:
            self._back._next = new_node
            new_node._prev = self._back
        self._back = new_node

    def remove(self, obj):
        """
        Remove an object from the hash table (and from the insertion order).
        Resize the table if its load_factor has dropped below (1-load_limit).
        :param obj: the value to remove; assumes hashing and equality work
        :return: True iff the obj has been remove from this set
        """
        hash_value = self._hash_function(obj) % self._capacity
        cursor = self._table[hash_value]
        init_size = self.size
        if cursor.get_data() == obj:
            self._delete_from_linked_list(cursor)
            self._table[hash_value] = self._table[hash_value].get_fwd()
            self.size -= 1
        else:
            while cursor.get_fwd() is not None and cursor.get_fwd().get_data() != obj:
                cursor = cursor.get_fwd()
            if cursor.get_fwd().get_data() == obj:
                self._delete_from_linked_list(cursor.get_fwd())
                cursor.set_fwd(cursor.get_fwd().get_fwd())
                self.size -= 1
        # print("load limit", self.size / self._capacity)
        if self.size == init_size:
            raise ValueError()
        elif self._capacity >= 20 and self.size / self._capacity < 0.25:
            self._rehash(self._capacity // 2)

    class _Iter(Iterator):
        __slots__ = "cursor"
        cursor: "ChainNode"

        def __init__(self, cursor):
            self.cursor = cursor

        def __next__(self):
            if self.cursor is None:
                raise StopIteration()
            else:
                result = self.cursor.get_data()
                self.cursor = self.cursor.get_next()
                return result

    def __iter__(self) -> Iterator[Any]:
        """
        Build an iterator.
        :return: an iterator for the current elements in the set
        """
        return LinkedHashSet._Iter(self._front)

    def _rehash(self, new_capacity: int) -> None:
        """Method to add data to the linked list
        :param new_capacity: the new size of the hash table
        """
        # print("===Rehashing===")
        self._reinitialize_map_with_updated_capacity(
            new_capacity, self._copy_current_data_to_list()
        )

    def _reinitialize_map_with_updated_capacity(self, new_capacity, temp_list):
        """Method to add data to the map
        :param new_capacity: the new size of the hash table
        :param temp_list: the list of ordered data
        """
        self._capacity = new_capacity
        self._table = [None] * self._capacity
        self._front = None
        self._back = None
        for items in temp_list:
            self.add(items)

    def _copy_current_data_to_list(self) -> list[Any]:
        """
        method to copy the data in the linked list to a list and return it
        :return list[Any]-> list of the elements
        """
        cursor = self._front
        temp_list = []
        while cursor is not None:
            temp_list.append(cursor.get_data())
            cursor = cursor.get_next()
        return temp_list

    def _delete_from_linked_list(self, cursor: ChainNode) -> None:
        """
        method to delete a node from linked list
        :param cursor: current node to be deleted
        """
        # print("Node to be deleted", cursor)
        if cursor.get_prev() is None:
            self._delete_from_front(cursor)
        elif cursor.get_next() is None:
            self._delete_from_back(cursor)
        else:
            self._delete_from_middle(cursor)

    def _delete_from_middle(self, cursor: "ChainNode") -> None:
        """
        method to delete a node from middle of linked list
        """
        # print("deleting from middle")
        cursor.get_prev().set_next(cursor.get_next())
        cursor.get_next().set_prev(cursor.get_prev())

    def _delete_from_back(self, cursor: "ChainNode") -> None:
        """
        method to delete a node from back of linked list
        """
        # print("deleting from back")
        self._back = cursor.get_prev()
        self._back.set_next(None)

    def _delete_from_front(self, cursor: "ChainNode") -> None:
        """
        method to delete a node from front of linked list
        """
        # print("deleting from front")
        self._front = cursor.get_next()
        if self._front is None:
            self._back = None
        else:
            self._front.set_prev(None)

    def __repr__(self) -> str:
        """
        Return a string with the content of the hash table and information about the hash table such as
        the table's capacity, size, current load factor and load limit.
        """
        string = self._generate_string()
        return self._add_table_data_to_string(string)

    def _add_table_data_to_string(self, string: str) -> str:
        """
        method to add the data to the string and return it
        :param string: str to which data needs to be added
        :return str -> updated string
        """
        for i in range(len(self._table)):
            string += "\t" + str(i) + ": "
            if self._table[i] is not None:
                cursor = self._table[i]
                if cursor.get_fwd() is None:
                    string += str(cursor.get_data()) + " -> "
                while cursor.get_fwd() is not None:
                    string += str(cursor.get_data()) + " -> "
                    cursor = cursor.get_fwd()
            string += "None\n"
        return string

    def _generate_string(self) -> str:
        """
        generate a header for the repr method
        :return string with the data
        """
        string = (
            "String generated\n----------------\nCapacity: "
            + str(self._capacity)
            + ", Size: "
            + str(self.size)
            + ", Load Factor: "
            + str(self.size / self._capacity)
            + ", Load Limit: "
            + str(self._load_limit)
            + "\n\tHash table\n\t----------\n"
        )
        return string

    def __str__(self) -> str:
        """
        Return a string representation of the objects added to this set sorted by insertion order.
        The string will contain all the objects separated by comma and enclosed between curly braces.
        Example:
            "{obj1, obj2, obj3, ...}"
        """
        string = "{ "
        cursor = self._front
        while cursor is not None:
            string += str(cursor.get_data()) + ", "
            cursor = cursor.get_next()
        string += "}"
        return string
