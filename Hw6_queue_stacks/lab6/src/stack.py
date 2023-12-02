"""
stack.py
author: CS RIT
description: A linked stack (LIFO) implementation
"""
from typing import Any

from node import LinkedNode


class Stack:
    __slots__ = "_top"
    _top: LinkedNode

    def __init__(self) -> None:
        """Create a new empty stack."""
        self._top = None

    def __str__(self) -> str:
        """Return a string representation of the contents of
        this stack, top value first.
        """
        result = "Stack["
        n = self._top
        while n != None:
            result += " " + str(n.get_value())
            n = n.get_link()
        result += " ]"
        return result

    def is_empty(self) -> bool:
        return self._top == None

    def push(self, newValue: Any) -> None:
        self._top = LinkedNode(newValue, self._top)

    def pop(self) -> None:
        assert not self.is_empty(), "Pop from empty stack"
        self._top = self._top.get_link()

    def peek(self) -> Any:
        assert not self.is_empty(), "peek on empty stack"
        return self._top.get_value()

    insert = push
    remove = pop
