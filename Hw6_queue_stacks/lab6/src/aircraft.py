from passenger import Passenger
from queue import Queue
from stack import Stack


class Aircraft:
    __slots__ = (
        "_boarding_line",
        "_de_boarding_line",
        "_max_no_of_passengers_on_aircraft",
        "_current_no_of_passengers_on_aircraft",
        "_successful_flights",
    )
    _boarding_line: Stack
    _de_boarding_line: Queue
    _max_no_of_passengers_on_aircraft: int
    _current_no_of_passengers_on_aircraft: int
    _successful_flights: int

    def get_current_no_of_passengers_on_aircraft(self):
        return self._current_no_of_passengers_on_aircraft

    def get_successful_flights(self):
        return self._successful_flights

    def __init__(self, max_no_of_passengers_on_aircraft: int) -> None:
        self._boarding_line = Stack()
        self._de_boarding_line = Queue()
        self._max_no_of_passengers_on_aircraft = max_no_of_passengers_on_aircraft
        self._current_no_of_passengers_on_aircraft = 0
        self._successful_flights = 0

    def start_seating(self, passenger: Passenger) -> bool:
        print(passenger)
        self._boarding_line.push(passenger)
        self._current_no_of_passengers_on_aircraft += 1
        return (
            self._max_no_of_passengers_on_aircraft
            > self._current_no_of_passengers_on_aircraft
        )

    def start_de_boarding(self) -> None:
        self._successful_flights += 1
        print(
            "Ready for taking off ...\nThe aircraft has landed.\nPassengers are disembarking..."
        )
        while not self._boarding_line.is_empty():
            passenger = self._boarding_line.peek()
            if passenger.get_carry_on():
                self._de_boarding_line.enqueue(passenger)
            else:
                print(passenger)
            self._boarding_line.pop()
        while not self._de_boarding_line.is_empty():
            print(self._de_boarding_line.peek())
            self._de_boarding_line.dequeue()
        self._current_no_of_passengers_on_aircraft = 0
