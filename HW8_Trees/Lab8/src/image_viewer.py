import sys
import tkinter as tk
from turtle import undo

from quadtree import QuadTree
from qtexception import QTException

# -c ../images/compressed/simple256x256.rit
__author__ = "Prateek Sharma"


def draw_image(pixels: list[str]):
    """
    method to draw the image
    :param:pixels:list of pixel values
    """

    root = tk.Tk()
    root.title("Grayscale Image")
    height = int(len(pixels) ** 0.5)
    width = int(len(pixels) ** 0.5)
    photo = tk.PhotoImage(width=width, height=height)
    counter = 0
    for y in range(height):
        for x in range(width):
            # Get the grayscale value
            gray = int(pixels[counter])
            counter += 1
            # Create the hexadecimal representation of the color (grayscale)
            hex_color = f"#{gray:02x}{gray:02x}{gray:02x}"
            # Put the fill color into the PhotoImage at its corresponding coordinate
            photo.put(hex_color, (x, y))
    canvas = tk.Canvas(root, width=width, height=height)
    canvas.pack()
    canvas.create_image((0, 0), image=photo, anchor="nw")
    root.mainloop()


def read_file(file_name: str) -> list[str]:
    """
    method to read file and populate the data into a list
    :param:filename: name of the file from which the pixels values to be read
    :return: list of the pixel values
    """
    pixels = []
    with open(file_name) as file:
        for line in file:
            value = line.strip()
            if not value.isdigit() and value != "-1":
                raise ValueError("integer value expected got ", value)
            pixels.append(value)
    return pixels


def main():
    """
    method called when running the program and throws an exception when incorrect no of arguments are passed in the command line
    or calls the draw image when file is uncompressed else create a quad tree and then calls draw image after uncompressing it
    """
    if len(sys.argv) == 2:
        pixels = read_file(sys.argv[1])
        draw_image(pixels)
    elif len(sys.argv) == 3 and sys.argv[1] == "-c":
        print("Uncompressing: ", sys.argv[2])
        pixels = read_file(sys.argv[2])
        quad_tree = QuadTree()
        quad_tree.uncompress(pixels)
        print(quad_tree)
        uncompressed_list = []
        for i in quad_tree:
            uncompressed_list.append(i)
        draw_image(uncompressed_list)
    else:
        raise QTException(
            """Usage: python image_viewer.py [-c] <filename>    
                -c Reads in a compressed image file. If this option is not present,
                    the file is considered to be uncompressed."""
        )


if __name__ == "__main__":
    main()
