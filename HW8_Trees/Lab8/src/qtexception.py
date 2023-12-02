class QTException(Exception):
    """
    A class used to communicate errors with operations involving the Quadtree
    and the files it uses for uncompressing.
    """

    def __init__(self, message: str):
        super().__init__(message)
