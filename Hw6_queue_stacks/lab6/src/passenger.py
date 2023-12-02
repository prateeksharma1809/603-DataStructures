"""
class for storing student passenger important pieces of information

1. Full Name        - A first name and last name.
2. Ticket Number    - A potentially variable length string comprising digits and possibly letters.
                        The first character is always a digit and indicates the passenger’s boarding
                        zone, which will be a number between 1 and 4.
3. Carry On         - Indicates whether or not the passenger has a carry-on bag that will
                        need to be stowed in the overhead compartment on the plane

author: Prateek Sharma
"""


class Passenger:
    __slots__ = "_full_name", "_ticket_number", "_has_carry_on"
    _full_name: str
    _ticket_number: str
    _has_carry_on: bool

    # constructor
    def __init__(self, full_name: str, ticket_number: str, has_carry_on: bool) -> None:
        """
        constructor
        :param full_name: A first name and last name.
        :param ticket_number: ticket number
        :param has_carry_on: true if passengers has a carry on
        """
        self._full_name = full_name
        self._has_carry_on = has_carry_on
        self._ticket_number = ticket_number

    # getter for full name
    def get_full_name(self) -> str:
        return self._full_name

    # getter for ticket number
    def get_ticket_number(self) -> str:
        return self._ticket_number

    # getter for carry on
    def get_carry_on(self) -> bool:
        return self._has_carry_on

    # method to convert object to its string representation
    def __str__(self) -> str:
        return (
            "	 "
            + self._full_name
            + ", ticket: "
            + self._ticket_number
            + ", carry_on: "
            + str(self._has_carry_on)
        )
