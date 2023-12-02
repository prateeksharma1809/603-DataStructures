import turtle

# global constants for window dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

def init() -> None:
    """
    Initialize for drawing.  (-200, -200) is in the lower left and
    (200, 200) is in the upper right.
    :pre: pos (0,0), heading (east), up
    :post: pos (0,0), heading (east), up
    :return: None
    """
    turtle.setworldcoordinates(-WINDOW_WIDTH / 2, -WINDOW_WIDTH / 2,
                               WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    turtle.up()
    turtle.setheading(0)
    turtle.title('Sampler Quilt')
    turtle.speed(10)
    turtle.showturtle()

def draw_sampler_quilt(side_of_square_box):
    """
        Draw all 3 designs of the quilt.
        input - size of the side of outer box
        :pre: pos (0,0), heading (east), up
        :post: pos (80,25), heading (east), up
        :return: None
        """
    #move turtle to the right of the screen
    turtle.backward(WINDOW_WIDTH/3)

    #first design call
    draw_first_design(side_of_square_box)

    #set turtle to center
    turtle.backward(side_of_square_box/2)
    turtle.right(90)
    turtle.backward(side_of_square_box/2)
    turtle.right(90)
    turtle.forward(side_of_square_box)
    # secound design call
    draw_second_design(side_of_square_box)
    turtle.backward(side_of_square_box/8)
    turtle.left(90)
    turtle.forward(side_of_square_box/2-side_of_square_box/8)
    turtle.left(90)
    turtle.forward(3*side_of_square_box/2)
    draw_third_design(side_of_square_box)

def draw_first_design(side_of_square_box):
    """
    Draw 1st design of the quilt. turtle at the left,center of screen
    input - size of the side of outer box
    :pre: pos (-175,0), heading (east), up
    :post: pos (-150,25), heading (west), up
    :return: None
    """
    draw_rectangle(side_of_square_box)
    position_turtle_center_of_box(side_of_square_box)
    create_triangles(15)


def draw_second_design(side_of_square_box):
    """
    Draw 2nd design of the quilt.
    input - size of the side of outer box
    :pre: pos (-50,0), heading (east), up
    :post: pos (-6.25,18.75), heading (west), up
    :return: None
    """
    draw_rectangle(side_of_square_box)
    draw_outer_square(side_of_square_box)
    draw_inner_square(side_of_square_box)

def draw_third_design(side_of_square_box):
    """
    Draw 3rd design of the quilt.
    input - size of the side of outer box
    :pre: pos (75,0), heading (east), up
    :post: pos (80,25), heading (east), up
    :return: None
    """
    draw_rectangle(side_of_square_box)
    half_of_side = side_of_square_box/2 #25
    turtle.forward(half_of_side - side_of_square_box/10) #20
    turtle.right(90)
    for i in range(4):
        draw_maroon_rectangle(half_of_side, side_of_square_box)
    for i in range(4):
        draw_corner_triangles(half_of_side, side_of_square_box)



def draw_small_triangles(side_of_square_box):
    """
       Draw small triangles inside rectangle of 3rd design.
       input - size of the side of outer box
       :pre: relative pos (0,0), heading (east), up
       :post: relative pos (0,5), heading (east), up
       :return: None
       """
    turtle.pendown()
    turtle.fillcolor('orange')
    turtle.begin_fill()
    turtle.left(45)
    turtle.forward((side_of_square_box/10) * (2 ** 0.5))
    turtle.left(90)
    turtle.forward((side_of_square_box/10) * (2 ** 0.5))
    turtle.left(135)
    turtle.forward((side_of_square_box/5))
    turtle.end_fill()
    turtle.penup()
    turtle.left(90)
    turtle.forward((side_of_square_box/10))



def draw_corner_triangles(half_of_side, side_of_square_box):
    """
         Draw large triangles of grey at the corner of 3rd design.
         input - size of the side of outer box
         :pre: relative pos (0,0), heading (east), up
         :post: relative pos (25,-15), heading (north), up
         :return: None
         """
    turtle.right(45)
    turtle.fillcolor('grey')
    turtle.begin_fill()
    turtle.forward((half_of_side - side_of_square_box / 5) * (2 ** 0.5))
    turtle.right(135)
    turtle.forward(half_of_side - side_of_square_box / 5)
    turtle.end_fill()
    turtle.penup()
    turtle.backward(half_of_side)
    turtle.right(90)


def draw_maroon_rectangle(half_of_side, side_of_square_box):
    """
     Draw large rectangels of maroon in 3rd design.
     input side_of_square_box - size of the side of outer box
     input half_of_side - side_of_square_box/2
     :pre: relative pos (0,0), heading (east), up
     :post: relative pos (25,-15), heading (north), up
     :return: None
     """
    turtle.pendown()
    turtle.fillcolor("maroon")
    turtle.begin_fill()
    for i in range(2):
        turtle.forward(half_of_side - side_of_square_box / 5)  # 15
        turtle.left(90)
        turtle.forward((half_of_side - side_of_square_box / 10) / 2)  # 10
        turtle.left(90)
    turtle.end_fill()
    turtle.penup()
    for i in range(3):
        draw_small_triangles(side_of_square_box)
    turtle.right(90)
    turtle.forward(half_of_side - side_of_square_box / 5)
    turtle.left(90)
    turtle.forward((half_of_side - side_of_square_box / 10) / 2)
    turtle.left(90)





def draw_outer_square(side_of_square_box):
    """
     Draw outer square of light blue in 2nd design.
     input - size of the side of outer box
     :pre: relative pos (0,0), heading (east), up
     :post: relative pos (0,0), heading (east), up
     :return: None
     """
    turtle.forward(side_of_square_box/2)
    turtle.right(90)
    turtle.forward(side_of_square_box/4 - side_of_square_box/10)
    turtle.right(45)
    turtle.pendown()
    turtle.fillcolor("light blue")
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(side_of_square_box / (2*(2 ** 0.5)))
        turtle.left(90)
    turtle.end_fill()
    turtle.penup()
    turtle.forward(side_of_square_box / (4 * (2 ** 0.5)))
    turtle.left(45)


def draw_inner_square(side_of_square_box):
    """
     Draw inner square of blue color in 2nd design.
     input - size of the side of outer box
     :pre: relative pos (0,0), heading (east), up
     :post: relative pos (0,0), heading (east), up
     :return: None
     """
    turtle.pendown()
    turtle.fillcolor("blue")
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(side_of_square_box/4)
        turtle.left(90)
    turtle.end_fill()
    turtle.penup()
    turtle.left(180)
    for i in range(4):
        draw_bow_tie(side_of_square_box)

def draw_bow_tie(side_of_square_box):
    """
     Draw bow tie of maroon color in 2nd design.
     input - size of the side of outer box
     :pre: relative pos (0,0), heading (west), up
     :post: relative pos (12.5,0), heading (south), up
     :return: None
     """
    side = side_of_square_box / 4
    turtle.pendown()
    turtle.fillcolor("maroon")
    turtle.begin_fill()
    turtle.forward(side)
    turtle.right(135)
    turtle.forward((2*side)/((2**0.5)))
    turtle.left(135)
    turtle.forward(side)
    turtle.left(135)
    turtle.forward((2*side)/((2**0.5)))
    turtle.end_fill()
    turtle.penup()
    turtle.forward(side/(2**0.5))
    turtle.left(90)
    turtle.forward(side/(2**0.5))
    turtle.right(135)


def create_triangles(side):
    """
    Draw wind mill in 1st design.
    input - size of the side of triangle
    :pre: relative pos (0,0), heading (east), up
    :post: relative pos (0, 0), heading (west), up
    :return: None
    """
    create_red_triangle(side)
    turtle.right(180)
    create_red_triangle(side)
    turtle.right(90)
    create_red_triangle(side)
    turtle.right(180)
    create_red_triangle(side)
    create_maroon_trangle(side)
    create_maroon_trangle(side)
    turtle.right(90)
    create_maroon_trangle(side)
    create_maroon_trangle(side)
    turtle.color("black")
    turtle.penup()



def create_maroon_trangle(side):
    """
    Draw wind mill's maroon triangle in 1st design.
    input - size of the side of triangle
    :pre: relative pos (0,0), heading (east), up
    :post: relative pos (0, 0), heading (east), up
    :return: None
    """
    turtle.fillcolor('#551122')
    turtle.begin_fill()
    turtle.forward(side * (3 ** 0.5) / 2)
    turtle.right(90)
    turtle.forward(side / 2)
    turtle.right(120)
    turtle.forward(side)
    turtle.left(30)
    turtle.end_fill()


def create_red_triangle(side):
    """
    Draw wind mill's red triangle in 1st design.
    input - size of the side of triangle
    :pre: relative pos (0,0), heading (east), up
    :post: relative pos (0, 0), heading (east), up
    :return: None
    """
    turtle.pendown()
    turtle.fillcolor('red')
    turtle.begin_fill()
    for i in range(3):
        turtle.forward(side)
        turtle.left(120)
    turtle.end_fill()


def position_turtle_center_of_box(side_of_square_box):
    """
   positions the turtle to the center  of the box
    input - size of the side of square
    :pre: relative pos (0,0), heading (east), up
    :post: relative pos (25, 25), heading (east), up
    :return: None
    """
    turtle.forward(side_of_square_box/2)
    turtle.right(90)
    turtle.forward(side_of_square_box/2 - side_of_square_box/10)


def draw_rectangle(side):
    """
  draws the outside of the box in which the design goes
   input - size of the side of square
   :pre: relative pos (0,0), heading (east), up
   :post: relative pos (5, 0), heading (north), up
   :return: None
   """
    turtle.pendown()
    for i in range(4):
        turtle.forward(side)
        turtle.left(90)
    turtle.forward(side/10)
    turtle.left(90)
    for i in range(4):
        turtle.forward(side)
        turtle.left(90)
        turtle.forward(side/10)
        turtle.left(90)
        turtle.forward(side/10)
        turtle.left(90)
    turtle.penup()


def main() -> None:
    """
    The main function.
    :pre: (relative) pos (0,0), heading (east), pen up
    :post: (relative) pos (80,25), heading (east), pen up
    :return: None
    """
    init()
    draw_sampler_quilt(50)
    turtle.mainloop()

if __name__ == "__main__":
    main()