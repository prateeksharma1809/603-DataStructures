from typing import Iterator, Any

from qtnode import QTNode


__author__ = "Prateek Sharma"


class QuadTree:
    """
    Represents a Quadtree in the tree for an image compressed using the Rich Image Tool file format.
    """

    QUAD_SPLIT = "-1"

    __slots__ = "_root", "_size", "_uncompressed_image"
    _root: "QTNode"
    _size: int
    _uncompressed_image: list[list]

    def __init__(self, root=None, size: int = 0):
        self._root = root
        self._size = size
        self._uncompressed_image = None

    def uncompress(self, compressed_data: list[str]) -> None:
        """
        method to which uncompress a given compressed list of data into a tree format and then convert
        it to an uncompressed list of pixels
        :param: compressed_data: list of compressed data, where 1 index is size and rest is the data
        :return: list[str]-> uncompressed data
        """
        self._size = int(compressed_data[0])
        if not self.is_power_of_two(self._size):
            raise ValueError("Not a square")
        self._root = self.parse(compressed_data[1:])
        self._uncompressed_image = self.create_uncompressed_list()

    def parse(self, tokens: list[str]) -> "QTNode":
        """
        method to create a tree out of the compressed list of data
        :param:tokens: list of values compressed
        :return: QTNode-root of the tree
        """
        if len(tokens) <= 0:
            raise ValueError("Data is corrupted")
        elif len(tokens) == 1:
            self.check_errors_in_token_value(tokens[0])
            return QTNode(tokens[0])
        else:
            node, tokens = self.__parser(tokens)
            if node is None:
                raise ValueError("Data is corrupted")
            return node

    def __parser(self, tokens: list[str]) -> ("QTNode", list[str]):
        """
        recursive method to create a tree out of the compressed list of data
        :param:tokens: list of values compressed
        :return: QTNode-root of the tree
        """
        if tokens is None or len(tokens) <= 0:
            return None, tokens
        elif int(tokens[0]) != -1:
            self.check_errors_in_token_value(tokens[0])
            return QTNode(tokens[0]), tokens[1:]
        else:
            ul, tokens = self.__parser(tokens[1:])
            ur, tokens = self.__parser(tokens)
            ll, tokens = self.__parser(tokens)
            lr, tokens = self.__parser(tokens)
            if ul is None or ur is None or ll is None or lr is None:
                raise ValueError("file data is corrupted!")
            return QTNode(QuadTree.QUAD_SPLIT, ul, ur, ll, lr), tokens

    def pre_order(self, root: QTNode) -> str:
        """
        method to generate a pre order string for the str method
        :param: root: root of the tree
        :return : string representation of the tree
        """
        if root is None:
            return ""
        string = root.get_value() + " "
        string += self.pre_order(root.get_upper_left())
        string += self.pre_order(root.get_upper_right())
        string += self.pre_order(root.get_lower_left())
        string += self.pre_order(root.get_lower_right())
        return string

    def check_errors_in_token_value(self, param) -> None:
        """
        method to check the errors in the size variable or the pixel values
        if invalid raises an exception
        :param:param value that needs to be checked
        """
        if int(param) > 255 or int(param) < -1:
            raise ValueError(param, "not a valid value for pixel")

    def __str__(self) -> str:
        """
        overriden str method to be called when print is called with the class object
        """
        return "Quadtree: " + self.pre_order(self._root)

    def is_power_of_two(self, n: int) -> bool:
        """
        check if the param passes is power of 2
        :param:n -> value to be checked
        :return: bool true if param is power of 2, or vice versa
        """
        if n == 0:
            return False
        while n != 1:
            if n % 2 != 0:
                return False
            n = n // 2
        return True

    def create_uncompressed_list(self) -> list[list[str]]:
        """
        method to call the recursive method for generating a 2 d array of the tree uncompressing
        :return uncompressed pixels list
        """
        row_length = int(self._size**0.5)
        return self.paint_array(self._root, row_length)
        # image_array_1d = self.convert_2d_to_1d_array(image_array_2d)
        # return image_array_1d

    def paint_array(self, root: "QTNode", size: int) -> list[[str]]:
        """
        recursive method for generating a 2 d array of the uncompressed tree
        :param: root: current node
        :param:size: current size of the pixel block
        :return uncompressed pixels list 2d
        """
        if int(root.get_value()) != -1:
            new_list = [[None for _ in range(size)] for _ in range(size)]
            for i in range(0, size):
                for j in range(0, size):
                    new_list[i][j] = root.get_value()
            return new_list
        else:
            list1 = self.paint_array(root.get_upper_left(), size // 2)
            list2 = self.paint_array(root.get_upper_right(), size // 2)
            list3 = self.paint_array(root.get_lower_left(), size // 2)
            list4 = self.paint_array(root.get_lower_right(), size // 2)
            return self.merge_list(list1, list2, list3, list4)

    def merge_list(
        self,
        list1: list[[str]],
        list2: list[[str]],
        list3: list[[str]],
        list4: list[[str]],
    ) -> list[[str]]:
        """
        helper method to combine n/2*n/2 array into n*n array
        :param:list1,list2,list3,list4 ->lists to be combined
        :return: list[[str]] a 2d list created by merging all the 4 lists
        """
        size = len(list1)
        new_array = [[None for _ in range(size * 2)] for _ in range(size * 2)]
        for i in range(size):
            for j in range(size):
                new_array[i][j] = list1[i][j]
                new_array[i][j + size] = list2[i][j]
                new_array[i + size][j] = list3[i][j]
                new_array[i + size][j + size] = list4[i][j]
        return new_array

    class _Iter(Iterator):
        __slots__ = "x_cursor", "y_cursor", "the_list"
        x_cursor: int
        y_cursor: int
        the_list: list[list[str]]

        def __next__(self) -> Any:
            if self.x_cursor >= len(self.the_list):
                raise StopIteration()
            else:
                # print(self.x_cursor, self.y_cursor)
                result = self.the_list[self.x_cursor][self.y_cursor]
                self.y_cursor += 1
                if self.y_cursor >= len(self.the_list[0]):
                    self.x_cursor += 1
                    self.y_cursor = 0
                return result

    def __iter__(self) -> Iterator[Any]:
        result = QuadTree._Iter()
        result.the_list = self._uncompressed_image
        result.x_cursor = 0
        result.y_cursor = 0
        return result

    # def convert_2d_to_1d_array(self, image_array_2d: list[[str]]) -> list[str]:
    #     """
    #     helper method to convert a 2d array to 1d array
    #     :param:image_array_2d: 2d list of pixels
    #     :return:1d list of pixels
    #     """
    #     new_list = []
    #     for i in range(len(image_array_2d)):
    #         for j in range(len(image_array_2d)):
    #             new_list.append(image_array_2d[i][j])
    #     return new_list
