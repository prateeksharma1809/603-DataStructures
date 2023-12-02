import os
import sys
from typing import Hashable

from graph import FieldGraph
from vertex import Vertex

"""
author: Prateek Sharma
"""


class HoliCow:
    __slots__ = "_field_graph", "_no_of_cows", "_no_of_paintball"
    _no_of_cows: int
    _no_of_paintball: int

    PAINTBALL = "paintball"
    COW = "cow"

    def __init__(self, field_graph: FieldGraph) -> None:
        self._field_graph = field_graph
        self._no_of_cows = 0
        self._no_of_paintball = 0

    def __str__(self):
        """
        create the string representation of the graph
        :return: str
        """
        return (
            "Number of vertices: "
            + str(self._field_graph.get_size())
            + ", cows:"
            + str(self._no_of_cows)
            + ", paint balls: "
            + str(self._no_of_paintball)
        )

    def read_file(self, file_name: str) -> dict[str, dict[str, list[int]]]:
        """
        method to read file and populate the data into a dict
        :param:filename: name of the file from which the data to be read
        :return: dict of field description
        """
        field_description = {HoliCow.COW: {}, HoliCow.PAINTBALL: {}}
        with open(file_name) as file:
            for line in file:
                values = line.strip()
                value = values.split()
                if value[0] not in field_description:
                    raise ValueError(
                        "invalid value for field, it can be of type 'cow' or 'paintball'"
                    )
                field_description[value[0]][value[1]] = [int(i) for i in value[2:]]
        return field_description

    def create_graph_from_file(self, file_name: str) -> None:
        """
        Create the graph from file input
        :param file_name: name of the file to be read
        :return: None
        """
        data = self.read_file(file_name)
        self._create_vertex_for_cows(data[HoliCow.COW])
        self._create_vertex_for_colors(data[HoliCow.PAINTBALL])
        self._check_and_populate_neighbours()

    def _create_vertex_for_cows(self, cows: dict[Hashable, list]) -> None:
        """
        creates vertex of type cows
        :param cows: dictionary with all the cow with their name as key and coordinates as values
        :return: None
        """
        for cow_name, coordinates in cows.items():
            vertex = self._field_graph.add_vertex(
                cow_name, coordinates[0], coordinates[1], HoliCow.COW, 0
            )
            if vertex.get_type() == HoliCow.COW:
                self._no_of_cows += 1
            else:
                raise ValueError("Incorrect entry")

    def _create_vertex_for_colors(self, color: dict[Hashable, list]) -> None:
        """
        creates vertex of type paintball
        :param color: dictionary with all the paintballs with their color as key and coordinates as values
        :return: None
        """
        for color_name, coordinates in color.items():
            # self._no_of_paintball += 1
            vertex = self._field_graph.add_vertex(
                color_name,
                coordinates[0],
                coordinates[1],
                HoliCow.PAINTBALL,
                coordinates[2],
            )
            if vertex.get_type() == HoliCow.PAINTBALL:
                self._no_of_paintball += 1
            else:
                raise ValueError("Incorrect entry")

    def _check_and_populate_neighbours(self) -> None:
        """
        creates neighbours of the vertex by calculating the distance b/w them and comparing it to radius
        :return:None
        """
        for vertex1 in self._field_graph:
            # checking only for the paintballs
            if vertex1.get_type() != HoliCow.COW:
                for vertex2 in self._field_graph:
                    # preventing self mapping
                    if vertex1.get_id() != vertex2.get_id():
                        if (
                            self.calculate_distance(vertex1, vertex2)
                            <= vertex1.get_radius()
                        ):
                            self._add_neighbour(vertex1, vertex2)

    def _add_neighbour(self, src_vertex: Vertex, dest_vertex: Vertex) -> None:
        """
        adds edge by calling add edge method and passing all the parameters required
        :param src_vertex: The source vertex
        :param dest_vertex: The destination vertex
        :return: None
        """
        self._field_graph.add_edge(
            src_vertex.get_id(),
            src_vertex.get_x(),
            src_vertex.get_y(),
            src_vertex.get_type(),
            src_vertex.get_radius(),
            dest_vertex.get_id(),
            dest_vertex.get_x(),
            dest_vertex.get_y(),
            dest_vertex.get_type(),
            dest_vertex.get_radius(),
        )

    def calculate_distance(self, vertex1: Vertex, vertex2: Vertex) -> int:
        """
        calculates distance bw two vertex using x and y values of each and returns distance
        :param vertex1: first vertex
        :param vertex2: second vertex
        :return: int
        """
        return (
            (vertex1.get_x() - vertex2.get_x()) ** 2
            + (vertex1.get_y() - vertex2.get_y()) ** 2
        ) ** 0.5

    def trigger_paintball_and_display_max(self) -> None:
        """
        method to print the details by internally calling trigger_paintball and then displaying the
        max count with details
        :return: None
        """
        no_of_cows_painted_by_color, are_any_cows_painted = self.trigger_paintball()
        if are_any_cows_painted:
            self._display_max_paintball(no_of_cows_painted_by_color)
        else:
            print("No cows were painted by any starting paintball!")

    def trigger_paintball(self) -> (dict[str, [int, dict[str, set]]], bool):
        """
        triggers paintball one by one and prints as well as populate details
        of which paintball triggered which and which cow is painted as well as no of cows
        :return: (dict[str, [int, dict[str, set]]], bool)
        """
        no_of_cows_painted_by_color = {}
        are_any_cows_painted = False
        for vertex in self._field_graph:
            if vertex.get_type() != HoliCow.COW:
                are_any_cows_painted = self.start_triggering_one_by_one_and_display(
                    are_any_cows_painted, vertex, no_of_cows_painted_by_color
                )
        return no_of_cows_painted_by_color, are_any_cows_painted

    def start_triggering_one_by_one_and_display(
        self,
        are_any_cows_painted: bool,
        vertex: "Vertex",
        no_of_cows_painted_by_color: dict[Hashable, [int, dict[Hashable, set]]],
    ) -> bool:
        """
        helper method of trigger_paintballs which calls a recursive method _trigger_ball
        to calculate the details
        :param are_any_cows_painted: boolean value true if at least one cow is painted
        :param vertex: paint colour vertex
        :param no_of_cows_painted_by_color: dict storing values for
        which color painted how many cows and their names
        :return: bool
        """
        print("Triggering " + str(vertex.get_id()) + " paint ball...")
        cows_painted_by_color = {}
        acc = self._trigger_ball(vertex, set(), 0, cows_painted_by_color)
        no_of_cows_painted_by_color[vertex.get_id()] = [acc, cows_painted_by_color]
        if len(cows_painted_by_color) > 0:
            are_any_cows_painted = True
        return are_any_cows_painted

    def _trigger_ball(
        self,
        vertex: "Vertex",
        visited: set,
        acc: int,
        cows_painted_by_color: dict[Hashable, set],
    ) -> int:
        """
        recursive method to check if there are any cows painted and
        if there is a color as neighbour then triggering that and also checking
        :param vertex: current vertex
        :param visited: set for storing the visited vertex so as to prevent cycles
        :param acc: counter for storing the value of cows painted
        :param cows_painted_by_color: dict storing details of which cow is painted by which color
        :return: int, no of cows that are painted
        """
        visited.add(vertex.get_id())
        if len(vertex.get_neighbors()) <= 0:
            return acc
        else:
            acc = self._check_recursively(acc, cows_painted_by_color, vertex, visited)
            return acc

    def _check_recursively(
        self,
        acc: int,
        cows_painted_by_color: dict[Hashable, set],
        vertex: Vertex,
        visited: set,
    ) -> int:
        """
        helper method for _trigger_ball
        :param acc: counter for storing the value of cows painted
        :param cows_painted_by_color: dict storing details of which cow is painted by which color
         :param vertex: cow or paintball
        :param vertex: neighbour of the key
        :param visited: set for storing the visited vertex so as to prevent cycles
        :return: int, no of cows that are painted
        """
        for name in vertex.get_neighbors():
            if name.get_type() == HoliCow.COW:
                acc += 1
                if name.get_id() not in cows_painted_by_color:
                    cows_painted_by_color[name.get_id()] = set()
                cows_painted_by_color[name.get_id()].add(vertex.get_id())
                print(
                    "\t"
                    + str(name.get_id())
                    + " is painted "
                    + str(vertex.get_id())
                    + "!"
                )
            elif name.get_id() not in visited:
                print(
                    "\t"
                    + str(name.get_id())
                    + " paint ball is triggered by "
                    + str(vertex.get_id())
                    + " paint ball"
                )
                acc = self._trigger_ball(name, visited, acc, cows_painted_by_color)
        return acc

    def trigger_and_display(self) -> None:
        """
        method to call and display methods of FieldGraph class in order to display the expected outputs
        :return: None
        """
        for vertex in self._field_graph:
            print(vertex)
        print()
        self.trigger_paintball_and_display_max()

    def _display_max_paintball(
        self, no_of_cows_painted_by_color: dict[Hashable, [int, dict[Hashable, set]]]
    ) -> None:
        """
        finds the color which painted the max no of cows and displays it with the help of helper function
        _print_max_details
        :param no_of_cows_painted_by_color: dict storing values for
        which color painted how many cows and their names
        :return: None
        """
        max_count = 0
        max_color = ""
        max_dict = None
        for key, values in no_of_cows_painted_by_color.items():
            if max_count < values[0]:
                max_count = values[0]
                max_color = key
                max_dict = values[1]
        print()
        self._print_max_details(max_color, max_count, max_dict)

    def _print_max_details(
        self, max_color: Hashable, max_count: int, max_dict: dict[Hashable, set]
    ) -> None:
        """
        helper method of _display_max_paintball for printing max details
        :param max_color: color which painted max no of cows
        :param max_count: max no of cows count
        :param max_dict: cow details painted by triggering this color
        :return: None
        """
        print(
            "Triggering the "
            + str(max_color)
            + " paint ball is the best choice with "
            + str(max_count)
            + " total paint on the cows:"
        )
        for vertex in self._field_graph:
            if vertex.get_type() == HoliCow.COW:
                if vertex.get_id() in max_dict:
                    print(
                        str(vertex.get_id()) + "'s",
                        "colors:",
                        str(max_dict[vertex.get_id()]),
                    )
                else:
                    print(str(vertex.get_id()) + "'s", "colors:", "{}")


def check_file_exists(file_name: str) -> bool:
    """
    to check if there is a file present at the given path
    :param file_name: name of the file to be checked
    :return: bool, true if present else false
    """
    return os.path.exists(file_name)


def main() -> None:
    """
    mein method to run the holicow program
    :return:None
    """
    if len(sys.argv) != 2:
        print("Usage: python3 holicow.py {filename}")
    elif not check_file_exists(sys.argv[1]):
        print("File not found: ", sys.argv[1])
    else:
        holi_cow = HoliCow(FieldGraph())

        holi_cow.create_graph_from_file(sys.argv[1])
        print("Field of Dreams")
        print(holi_cow)
        print("----------------------------------------------------")
        holi_cow.trigger_and_display()


if __name__ == "__main__":
    main()
