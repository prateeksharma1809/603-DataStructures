"""
file: tests.py
description: Verify the LinkedHashSet class implementation
"""

__author__ = "Prateek Sharma"

from linkedhashset import LinkedHashSet


def print_set(a_set):
    for word in a_set:  # uses the iter method
        print(word, end=" ")
    print()


def hash_fun(obj):
    return 0


def test0():
    print("====================test0 - Start========================")
    table = LinkedHashSet(100)
    table.add("to")
    table.add("do")
    table.add("is")
    table.add("to")
    table.add("he")
    table.add("bee")
    table.add("she")
    table.add("be")

    print(repr(table))
    print("String representation of table")
    print(table)

    print_set(table)

    print("'to' in table?", table.contains("to"))
    table.remove("to")
    print("'to' in table?", table.contains("to"))
    print("'be' in table?", table.contains("be"))
    table.remove("be")
    print("'be' in table?", table.contains("be"))
    print("'bee' in table?", table.contains("bee"))
    table.remove("bee")
    print("'bee' in table?", table.contains("bee"))

    print_set(table)
    print("====================test0 - End========================")


def test1():
    print("====================test1 - Start========================")
    # With custom hash function
    table = LinkedHashSet(10, hash_function=hash_fun)
    print(repr(table))
    table.add("to")
    table.add("do")
    table.add("is")
    table.add("to")
    table.add("he")
    table.add("bee")
    table.add("she")
    table.add("done")
    table.add("my")
    table.add("help")
    table.add("batman")
    table.add("should")
    table.add("fly")
    table.add("be")

    print(repr(table))

    print_set(table)

    print("'to' in table?", table.contains("to"))
    table.remove("to")
    print("'to' in table?", table.contains("to"))
    print("'be' in table?", table.contains("be"))
    table.remove("be")
    print("'be' in table?", table.contains("be"))
    print("'bee' in table?", table.contains("bee"))
    table.remove("bee")
    print("'bee' in table?", table.contains("bee"))

    print_set(table)

    print(repr(table))
    print("====================test1 - End========================")


def test2():
    # where rehashing when deleting
    print("====================test2 - Start========================")
    table = LinkedHashSet(100)
    table.add("to")
    table.add("do")
    table.add("is")
    table.add("to")
    table.add("he")
    table.add("bee")
    table.add("she")
    table.add("be")

    print(repr(table))

    print_set(table)

    print("'to' in table?", table.contains("to"))
    table.remove("to")
    print("'to' in table?", table.contains("to"))
    print("'be' in table?", table.contains("be"))
    table.remove("be")
    print("'be' in table?", table.contains("be"))
    print("'bee' in table?", table.contains("bee"))
    table.remove("bee")
    print("'bee' in table?", table.contains("bee"))

    print_set(table)
    print("After rehashing")
    print(repr(table))
    print("====================test2 - End========================")


def test3():
    print("====================test3 - Start========================")
    #  rehashing while adding
    table = LinkedHashSet(10)
    print(repr(table))
    table.add("to")
    table.add("do")
    table.add("is")
    table.add("to")
    table.add("he")
    table.add("bee")
    table.add("she")
    table.add("done")
    table.add("my")
    table.add("help")
    table.add("batman")
    table.add("should")
    table.add("fly")
    table.add("be")

    print(repr(table))

    print_set(table)

    print("'to' in table?", table.contains("to"))
    table.remove("to")
    print("'to' in table?", table.contains("to"))
    print("'be' in table?", table.contains("be"))
    table.remove("be")
    print("'be' in table?", table.contains("be"))
    print("'bee' in table?", table.contains("bee"))
    table.remove("bee")
    print("'bee' in table?", table.contains("bee"))

    print_set(table)
    print("After rehashing")
    print(repr(table))
    print("====================test3 - End========================")


if __name__ == "__main__":
    test0()
    test1()
    test2()
    test3()
