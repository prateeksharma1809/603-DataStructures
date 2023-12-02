"""
CSCI-603 Lab 3: Fractal islands

program to draw fractal islands in a turtle’s
canvas using recursion

author: Prateek Sharma
"""

import re
import turtle


def init(length_of_one_side, no_of_sides) -> None:
    """
    Initialize for drawing.  (-length_of_one_side *2 , -length_of_one_side *2) is in the lower left and
    (length_of_one_side*2, length_of_one_side*2) is in the upper right.
    :pre: pos (0,0), heading (east), up
    :post: pos (length_of_one_side /2, (no_of_sides - 2) * length_of_one_side / 4), heading (east), down
    :return: None
    """
    turtle.setworldcoordinates(
        -length_of_one_side * 2,
        -length_of_one_side * 2,
        length_of_one_side * 2,
        length_of_one_side * 2,
    )
    turtle.up()
    turtle.setheading(0)
    turtle.title("fractal curve")
    turtle.speed(0)
    turtle.backward(length_of_one_side / 2)
    turtle.right(90)
    turtle.forward((no_of_sides - 2) * length_of_one_side / 4)
    turtle.left(90)
    # turtle.showturtle()
    turtle.pendown()


def draw_fractal_curve_1(length: float, n: int) -> float:
    """
    method to draw the first pattern
    :pre: pos (0,0), heading (east), down
    :post: pos (length, 0), heading (east), down
    :param length: side’s length of the pattern
    :param n: level
    :return:perimeter of the figure drawn
    """
    if n == 1:
        turtle.forward(length)
        parm = length
    else:
        parm = draw_fractal_curve_1(length / 3, n - 1)
        turtle.left(60)
        parm += draw_fractal_curve_1(length / 3, n - 1)
        turtle.right(120)
        parm += draw_fractal_curve_1(length / 3, n - 1)
        turtle.left(60)
        parm += draw_fractal_curve_1(length / 3, n - 1)
    return parm


def draw_fractal_curve_2(length: float, n: int) -> float:
    """
    method to draw the first pattern
    :pre: pos (0,0), heading (east), down
    :post: pos (length, 0), heading (east), down
    :param length: side’s length of the pattern
    :param n: level
    :return:perimeter of the figure drawn
    """
    if n == 1:
        turtle.forward(length)
        parm = length
    else:
        turtle.left(45)
        parm = draw_fractal_curve_2(length / (2**0.5), n - 1)
        turtle.right(90)
        parm += draw_fractal_curve_2(length / (2**0.5), n - 1)
        turtle.left(45)
    return parm


def main() -> None:
    """
    main method to call the draw functions one by one after taking input from user
    number of sides, length of a side and number of levels and passing it to draw functions
    :pre: pos (0,0), heading (east), down
    :post: pos (length, 0), heading (east), down
    """
    no_of_sides = int(
        get_input_from_user(
            "Please enter number of sides the island will have: ",
            "value must be 'positive integer', you entered",
            "[0-9]+",
        )
    )
    length_of_one_side = float(
        get_input_from_user(
            " Please enter length of one side in pixels: ",
            "value must be ' positive float', you entered",
            "[0-9.]+",
        )
    )
    no_of_levels = int(
        get_input_from_user(
            "Please enter number of levels: ",
            "value must be 'positive integer', you entered",
            "[0-9]+",
        )
    )
    init(length_of_one_side, no_of_sides)
    total_length = 0
    for i in range(no_of_sides):
        total_length += draw_fractal_curve_1(length_of_one_side, no_of_levels)
        turtle.left(360 / no_of_sides)
    print("Total length : " + str(total_length))
    input("Hit enter to continue")
    turtle.reset()
    init(length_of_one_side, no_of_sides)
    total_length = 0
    for i in range(no_of_sides):
        total_length += draw_fractal_curve_2(length_of_one_side, no_of_levels)
        turtle.left(360 / no_of_sides)

    print("Total length : " + str(total_length))
    input("Hit enter to end!")


def get_input_from_user(input_prompt, error_message, reg_ex) -> str:
    """
    method to ask user to input information until a valid value is received
     :pre: pos (0,0), heading (east), down
    :post: pos (0, 0), heading (east), down
    :param input_prompt: display message about what to enter
    :param error_message: error message to be shown if the info entered by user is incorrect
    :param reg_ex: regular expression to validate the input
    :return: the valid input string
    """
    is_not_valid_input = True
    no_of_sides = 0
    pattern = re.compile(reg_ex)
    while is_not_valid_input:
        no_of_sides = input(input_prompt)
        if pattern.fullmatch(no_of_sides):
            is_not_valid_input = False
        else:
            print(error_message + " '" + str(no_of_sides) + "'")
    return no_of_sides


if __name__ == "__main__":
    main()
