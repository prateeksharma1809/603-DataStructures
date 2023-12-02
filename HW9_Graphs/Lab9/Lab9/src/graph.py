"""
CSCI-603: Graphs
Author: RIT CS, Prateek Sharma

An implementation of a graph data structure as an adjacency list.

Code taken from the online textbook and modified:

http://interactivepython.org/runestone/static/pythonds/Graphs/Implementation.html
"""
from typing import Hashable

from vertex import Vertex


class FieldGraph:
    """
    A graph implemented as an adjacency list of vertices.

    :slot: vertList (dict):  A dictionary that maps a vertex key to a Vertex
        object
    :slot: _no_of_cows (int):  The total number of cows in the graph
    :slots: _no_of_paintballs(int): The total number of paintballs in the graph
    """

    __slots__ = "_vertDict", "_size"
    _vertDict: dict[Hashable, Vertex]
    _size: int

    def __init__(self):
        """
        Initialize the graph
        :return: None
        """
        self._vertDict = {}
        self._size = 0

    def add_vertex(
        self, key: Hashable, x: int, y: int, type: str, radius: int
    ) -> Vertex:
        """
        Add a new vertex to the graph.
        :param key: The identifier for the vertex (typically a string)
        :param x: x coordinate of the vertex
        :param y: y coordinate of the vertex
        :param type: cow or paintball type of vertex
        :param radius: radius of the vertex
        :return: Vertex
        """
        # count this vertex if not already present
        if self.get_vertex(key) is None:
            self._size += 1
            vertex = Vertex(key, x, y, type, radius)
            self._vertDict[key] = vertex
        return vertex

    def get_vertex(self, key: Hashable) -> Vertex:
        """
        Retrieve the vertex from the graph.
        :param key: The vertex identifier
        :return: Vertex if it is present, otherwise None
        """
        if key in self._vertDict:
            return self._vertDict[key]
        else:
            return None

    def __contains__(self, key: Hashable) -> bool:
        """
        Returns whether the vertex is in the graph or not.  This allows the
        user to do:

            key in graph

        :param key: The vertex identifier
        :return: True if the vertex is present, and False if not
        """
        return key in self._vertDict

    def add_edge(
        self,
        src: Hashable,
        x1: int,
        y1: int,
        type1: str,
        radius1: int,
        dest: Hashable,
        x2: int,
        y2: int,
        type2: str,
        radius2: int,
        cost: int = 0,
    ):
        """
        Add a new directed edge from a source to a destination of an edge cost.
        :param src: The source vertex identifier
        :param dest: The destination vertex identifier
        :param cost: The edge cost (defaults to 0)
        :param x1,x2: x coordinate of the vertex 1 and 2 respectively
        :param y1,y2: y coordinate of the vertex 1 and 2 respectively
        :param type1, type2: cow or paintball type of vertex 1 and 2 respectively
        :param radius1, radius2: radius of the vertex 1 and 2 respectively
        :return: None
        """
        if src not in self._vertDict:
            self.add_vertex(src, x1, y1, type1, radius1)
        if dest not in self._vertDict:
            self.add_vertex(dest, x2, y2, type2, radius2)
        self._vertDict[src].add_neighbor(self._vertDict[dest], cost)

    def get_vertices(self):
        """
        Return the collection of vertex identifiers in the graph.
        :return: A list of vertex identifiers
        """
        return self._vertDict.keys()

    def __iter__(self):
        """
        Return an iterator over the vertices in the graph.  This allows the
        user to do:

            for vertex in graph:
                ...

        :return: A list iterator over Vertex objects
        """
        return iter(self._vertDict.values())

    def get_size(self):
        return self._size


def testGraph():
    """
    A test function for the Graph class.
    :return: None
    """
    # cows = {"Daisy": [2, 6], "Babe": [8, 4], "Milka": [6, 3], "Fauntleroy": [10, 2]}
    cows = {"Fauntleroy": [10, 2]}
    colors = {
        "RED": [4, 4, 3],
        "BLUE": [8, 5, 1],
        "GREEN": [6, 5, 2],
        "PINK": [3, 3, 3],
        "WHITE": [0, 0, 5],
        "YELLOW": [12, 3, 3],
    }
    # add all the edges to the graph
    field = FieldGraph()

    # for state, details in Field.items():
    #     for neighbor in details:
    #         # this automatically creates a new vertices if not already present
    #         northeast.add_vertex(state, neighbor)

    # display the vertices, which will show the connected neighbors.
    # this will call the __iter__() method to get the Vertex objects.
    for state in field:
        print(state)

    # print(northeast.get_vertices())
    print(field)
    # a = field.trigger_paintballs()
    # print(a)
    # # check the __contains__() method
    # print("MA in northeast (True)?", "MA" in northeast)
    # print("CA in northeast (False)?", "CA" in northeast)
    #
    # # test getVertex()
    # print("MA vertex:", northeast.get_vertex("MA"))


if __name__ == "__main__":
    testGraph()
