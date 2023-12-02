"""
authors: CS-RIT, Prateek Sharma
"""


def sort_maze(solved_maze: list) -> list:
    """
    method is implementation of merge sort, it divides list into half recursively until base case is reached
     and then calls merge on it
    :param solved_maze: maze with max sum populated in each column
    :return: sorted list
    """
    if len(solved_maze) < 2:
        return solved_maze
    else:
        return merge(
            sort_maze(solved_maze[: len(solved_maze) // 2]),
            sort_maze(solved_maze[len(solved_maze) // 2 :]),
        )


def merge(left_list: list, right_list: list) -> list:
    """
    method to merge 2 sorted list into one sorted list and return it
    :param left_list: sorted left list
    :param right_list: sorted right list
    :return: sorted list by combining left and right list
    """
    result = []
    left_index, right_index = 0, 0
    while left_index < len(left_list) and right_index < len(right_list):
        if left_list[left_index].max_sum > right_list[right_index].max_sum:
            result.append(left_list[left_index])
            left_index += 1
        else:
            result.append(right_list[right_index])
            right_index += 1
    result.extend(left_list[left_index:])
    result.extend(right_list[right_index:])
    return result
