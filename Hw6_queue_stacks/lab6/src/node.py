"""
node.py
author: CS RIT
description: A linkable node class for use in stacks, queues, and linked lists
"""
from typing import Any


class LinkedNode:
    __slots__ = "_value", "_link"
    _value: Any
    _link: "LinkedNode"

    def __init__(self, value: Any, link: "LinkedNode" = None) -> None:
        """Create a new node and optionally link it to an existing one.
        param value: the value to be stored in the new node
        param link: the node linked to this one
        """
        self._value = value
        self._link = link

    def get_value(self) -> Any:
        return self._value

    def get_link(self) -> "LinkedNode":
        return self._link

    def set_link(self, node: "LinkedNode") -> None:
        self._link = node

    def __str__(self) -> str:
        """Return a string representation of the contents of
        this node. The link is not included.
        """
        return str(self._value)

    def __repr__(self) -> str:
        """Return a string that, if evaluated, would recreate
        this node and the node to which it is linked.
        This function should not be called for a circular
        list.
        """
        return "LinkedNode(" + repr(self._value) + "," + repr(self._link) + ")"


def test() -> None:
    nodes = LinkedNode(1, LinkedNode("two", LinkedNode(3.0)))
    n = nodes
    while n != None:
        print(n.get_value())
        n = n.get_link()
    print()
    print(nodes)
    print(repr(nodes))


if __name__ == "__main__":
    test()
