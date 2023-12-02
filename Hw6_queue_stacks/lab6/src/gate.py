import aircraft
from aircraft import Aircraft
from queue import Queue
from passenger import Passenger
from stack import Stack

"""
class to simulate gate functions 
author: Prateek Sharma
"""


class Gate:
    __slots__ = (
        "_line1",
        "_line2",
        "_line3",
        "_line4",
        "_stack_on_plane",
        "_gate_capacity",
        "_current_count_of_passengers",
        "_aircraft",
        "_no_of_flights",
    )
    _line1: Queue
    _line2: Queue
    _line3: Queue
    _line4: Queue
    _stack_on_plane: Stack
    _gate_capacity: int
    _current_count_of_passengers: int
    _aircraft: Aircraft
    _no_of_flights: int

    def get_current_count_of_passengers(self) -> int:
        """
        getter method for count of passengers on the gate at the moment
        :return: current count of passengers
        """
        return self._current_count_of_passengers

    def __init__(self, gate_capacity: int, max_passengers: int) -> None:
        """
        constructor
        :param gate_capacity: no of people allowed at a time
        :param max_passengers: capacity of aircraft
        """
        self._line1 = Queue()
        self._line2 = Queue()
        self._line3 = Queue()
        self._line4 = Queue()
        self._gate_capacity = gate_capacity
        self._current_count_of_passengers = 0
        self._aircraft = Aircraft(max_passengers)
        self._no_of_flights = 0

    def get_no_of_flights(self) -> int:
        """
        getter method
        :return: no of flights till now
        """
        return self._no_of_flights

    def line_up(self, passenger: Passenger) -> bool:
        """
        method simulating the line up feature at the gate
        passengers queued up as per the first digit of their ticket number
        :param passenger: passenger object
        :return: true if still capacity left at the gate, else false
        """
        if passenger.get_ticket_number()[0] == "1":
            self._line1.enqueue(passenger)
        elif passenger.get_ticket_number()[0] == "2":
            self._line2.enqueue(passenger)
        elif passenger.get_ticket_number()[0] == "3":
            self._line3.enqueue(passenger)
        elif passenger.get_ticket_number()[0] == "4":
            self._line4.enqueue(passenger)
        self.increment_current_count_of_passengers()
        return self._current_count_of_passengers < self._gate_capacity

    def increment_current_count_of_passengers(self) -> None:
        """
        method to increment the count by 1
        """
        self._current_count_of_passengers += 1

    def decrementing_current_count_of_passengers(self) -> None:
        """
        method to decrement the count by 1
        """
        self._current_count_of_passengers -= 1

    def start_boarding(self) -> None:
        """
        method simulating the flight boarding style, i.e., Zone 4 will board first then Zone3 and so on
        """
        for line_no in (4, 3, 2, 1):
            self.board_line(line_no)
        if self._aircraft.get_current_no_of_passengers_on_aircraft() > 0:
            print("There are no more passengers at the gate.")
            self._aircraft.start_de_boarding()
        self._no_of_flights = self._aircraft.get_successful_flights()

    def board_line(self, line_no: int) -> None:
        """
        method implementing the zone boarding logic
        :param line_no: zone for which boarding needs to be done
        """
        line = Queue()
        if line_no == 4:
            line = self._line4
        elif line_no == 3:
            line = self._line3
        elif line_no == 2:
            line = self._line2
        elif line_no == 1:
            line = self._line1
        while not line.is_empty():
            if self._aircraft.get_current_no_of_passengers_on_aircraft() == 0:
                print("Passengers are boarding the aircraft...")
            is_aircraft_empty = self._aircraft.start_seating(line.peek())
            line.dequeue()
            self.decrementing_current_count_of_passengers()
            if not is_aircraft_empty:
                print("The aircraft is full.")
                self._aircraft.start_de_boarding()
