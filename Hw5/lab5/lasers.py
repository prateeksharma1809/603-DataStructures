import sys
from dataclasses import dataclass
from sort import sort_maze

"""
:author: Prateek Sharma
"""


@dataclass
class LaserMax:
    """
    Class to hold the laser max values, with direction and x,y coordinate for center
    max_sum : max sum value for that current position
    x : row index
    y : column index
    """

    max_sum: int
    direction: str
    x: int
    y: int


def read_file_and_populate_maze(filename: str) -> list:
    """
    method to read data from the given file and populate it into a list
    :param filename: name of the file from which the data to be read
    :return: list of read values
    """
    maze = []
    with open(filename) as file_pointer:
        print("Loaded: " + filename)
        for line in file_pointer:
            print(line.strip())
            maze.append(line.strip().split(" "))
    return maze


def check_and_fill_puzzle() -> list or None:
    """
    calls the solve maze function if the file is found else show error message
    :return: sorted, solved maze list, if found else None
    """
    if len(sys.argv) == 2:
        return solve_maze(read_file_and_populate_maze(sys.argv[1]))
    else:
        print("Usage: python3 lasers.py filename")


def calculate_sum(block1: str, block2: str, block3: str) -> int:
    """
    calculates the sum of the blocks passed in the argument
    :param block1: first block string value
    :param block2: 2nd block string value
    :param block3: 3rd block string value
    :return: integer sum of the 3 blocks
    """
    return int(block1) + int(block2) + int(block3)


def check_if_lazer_can_point_north(
    maze: list, row_index: int, column_index: int, lazer_max: LaserMax
):
    """
    block to check and calculate sum if the lazer can point in north direction and update it in lazer max
    :param maze: the puzzle passed in the file
    :param row_index: row index on which to check
    :param column_index: column index on which to check
    :param lazer_max: the list to hold the coordinates and details about lasers
    """
    if (
        row_index - 1 >= 0
        and column_index - 1 >= 0
        and column_index + 1 < len(maze[row_index])
    ):
        new_sum = calculate_sum(
            maze[row_index - 1][column_index],
            maze[row_index][column_index - 1],
            maze[row_index][column_index + 1],
        )
        if new_sum > lazer_max.max_sum:
            lazer_max.max_sum = new_sum
            lazer_max.direction = "N"


def check_if_lazer_can_point_east(
    maze: list, row_index: int, column_index: int, lazer_max: LaserMax
):
    """
    block to check and calculate sum if the lazer can point in east direction and update it in lazer max
    :param maze: the puzzle passed in the file
    :param row_index: row index on which to check
    :param column_index: column index on which to check
    :param lazer_max: the list to hold the coordinates and details about lasers
    """
    if (
        row_index - 1 >= 0
        and row_index + 1 < len(maze)
        and column_index + 1 < len(maze[row_index])
    ):
        new_sum = calculate_sum(
            maze[row_index - 1][column_index],
            maze[row_index + 1][column_index],
            maze[row_index][column_index + 1],
        )
        if new_sum > lazer_max.max_sum:
            lazer_max.max_sum = new_sum
            lazer_max.direction = "E"


def check_if_lazer_can_point_south(
    maze: list, row_index: int, column_index: int, lazer_max: LaserMax
):
    """
    block to check and calculate sum if the lazer can point in south direction and update it in lazer max
    :param maze: the puzzle passed in the file
    :param row_index: row index on which to check
    :param column_index: column index on which to check
    :param lazer_max: the list to hold the coordinates and details about lasers
    """
    if (
        row_index + 1 < len(maze)
        and column_index - 1 >= 0
        and column_index + 1 < len(maze[row_index])
    ):
        new_sum = calculate_sum(
            maze[row_index + 1][column_index],
            maze[row_index][column_index - 1],
            maze[row_index][column_index + 1],
        )
        if new_sum > lazer_max.max_sum:
            lazer_max.max_sum = new_sum
            lazer_max.direction = "S"


def check_if_lazer_can_point_west(
    maze: list, row_index: int, column_index: int, lazer_max: LaserMax
):
    """
    block to check and calculate sum if the lazer can point in west direction and update it in lazer max
    :param maze: the puzzle passed in the file
    :param row_index: row index on which to check
    :param column_index: column index on which to check
    :param lazer_max: the list to hold the coordinates and details about lasers
    """
    if row_index - 1 >= 0 and row_index + 1 < len(maze) and column_index - 1 >= 0:
        new_sum = calculate_sum(
            maze[row_index - 1][column_index],
            maze[row_index + 1][column_index],
            maze[row_index][column_index - 1],
        )
        if new_sum > lazer_max.max_sum:
            lazer_max.max_sum = new_sum
            lazer_max.direction = "W"


def solve_maze(maze: list) -> list:
    """
    loop through all the rows and columns and check if it can find a max position of lazer for that coordinate
    :param maze: puzzle passed as argument
    :return: sorted , solved maze
    """
    solved_maze = []
    for row_index in range(len(maze)):
        for column_index in range(len(maze[row_index])):
            lazer_max = LaserMax(0, None, row_index, column_index)
            check_if_lazer_can_point_north(maze, row_index, column_index, lazer_max)
            check_if_lazer_can_point_west(maze, row_index, column_index, lazer_max)
            check_if_lazer_can_point_east(maze, row_index, column_index, lazer_max)
            check_if_lazer_can_point_south(maze, row_index, column_index, lazer_max)
            # print(lazer_max, end="")  # uncomment to see the solved maze
            if lazer_max.direction is not None:
                solved_maze.append(lazer_max)
        # print()
    return sort_maze(solved_maze)


def main():
    """
    main method to call when the need to solve puzzle
    """
    solved_maze = check_and_fill_puzzle()
    if solved_maze is not None:
        ask_user_for_lazer_no(solved_maze)


def ask_user_for_lazer_no(solved_maze):
    """
    method to ask the number of lasers he want to display with max sum in which direction
        :param solved_maze: list with sorted elements
    """
    no_of_lasers = int(input("Enter number of lasers:"))
    if 0 != no_of_lasers > len(solved_maze):
        print("Too many lasers to place!")
    else:
        print_lazer_placements(no_of_lasers, solved_maze)


def print_lazer_placements(no_of_lasers: int, solved_maze: list):
    """
    print the lasers in descending order
    :param no_of_lasers: no of lasers user need to see
    :param solved_maze: list of laser placements available
    """
    total_sum = 0
    for i in range(no_of_lasers):
        if i == 0:
            print("Optimal placement:")
        print(
            "loc: ("
            + str(solved_maze[i].x)
            + ","
            + str(solved_maze[i].y)
            + "), facing: "
            + solved_maze[i].direction
            + ", sum: "
            + str(solved_maze[i].max_sum)
        )
        total_sum += solved_maze[i].max_sum
    print("Total: " + str(total_sum))


if __name__ == "__main__":
    main()
