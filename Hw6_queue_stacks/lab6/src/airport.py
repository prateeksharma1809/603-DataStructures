from gate import Gate
from queue import Queue
from passenger import Passenger


"""
class to simulate airport functions 
author: Prateek Sharma
"""


class Airport:
    __slots__ = (
        "_max_passenger_on_aircraft",
        "_gate_capacity",
        "_passenger_queue",
        "_gate",
        "_file_name",
    )
    _gate_capacity: int
    _max_passenger_on_aircraft: int
    _passenger_queue: Queue
    _gate: Gate
    _file_name: str

    # constructor
    def __init__(self, file_name: str) -> None:
        self._gate_capacity = -1
        self._max_passenger_on_aircraft = -1
        self._passenger_queue = Queue()
        self._gate = None
        self._file_name = file_name

    def start_airport(self) -> int:
        """
        method to initialize the gate object with its capacity
        :return no of flights that took all passengers from A to B
        """
        self._gate = Gate(self._gate_capacity, self._max_passenger_on_aircraft)
        self.start_processing_passengers()
        return self._gate.get_no_of_flights()

    def start_processing_passengers(self) -> None:
        """
        start to allow passengers into the gate as per the capacity decided by fire code
        """
        while not self._passenger_queue.is_empty():
            if self._gate.get_current_count_of_passengers() == 0:
                print("Passengers are lining up at the gate...")
            passenger = self._passenger_queue.peek()
            print(passenger)
            is_gate_empty = self._gate.line_up(passenger)
            if not is_gate_empty:
                print("The gate is full; remaining passengers must wait.")
                self._gate.start_boarding()
            self._passenger_queue.dequeue()
        if (
            self._passenger_queue.is_empty()
            and self._gate.get_current_count_of_passengers() > 0
        ):
            print("The last passenger is in line!")
            self._gate.start_boarding()

    def take_user_inputs(self) -> None:
        """
        method to take inputs from user for gate capacity and max passengers allowed on aircraft
        """
        is_continue, input_no, gate_capacity, max_passenger_on_aircraft = True, 1, 0, 0
        while is_continue:
            if input_no == 1:
                gate_capacity = input(
                    "Enter fire-code mandated maximum number of passengers allowed at an airline gate: "
                )
            elif input_no == 2:
                max_passenger_on_aircraft = input(
                    "Enter maximum passenger capacity of an AiRIT aircraft: "
                )
            input_no, is_continue = self.process_inputs(
                gate_capacity, input_no, is_continue, max_passenger_on_aircraft
            )

    def process_inputs(
        self,
        gate_capacity: str,
        input_no: int,
        is_continue: bool,
        max_passenger_on_aircraft: str,
    ) -> (int, bool):
        """
        method to validate user inputs and show error message if wrong input is provided
        :param gate_capacity: user entered value for gate capacity
        :param input_no: deciding factor for which value needs to be processed
        1 for gate capacity and 2 from max passengers
        :param is_continue: flag which decides if the user need to re enter correct value
        :param max_passenger_on_aircraft: capacity of plane
        :return: is_continue and input_no
        """
        if input_no == 1 and not gate_capacity.isdigit():
            print(
                "fire-code mandated maximum number value must be 'positive integer', you entered"
                + gate_capacity
            )
        elif input_no == 1 and gate_capacity.isdigit():
            input_no = 2
            self._gate_capacity = int(gate_capacity)
        elif input_no == 2 and not max_passenger_on_aircraft.isdigit():
            print(
                "maximum passenger capacity of an AiRIT aircraft value must be 'positive integer', you entered"
                + max_passenger_on_aircraft
            )
        elif input_no == 2 and max_passenger_on_aircraft.isdigit():
            self._max_passenger_on_aircraft = int(max_passenger_on_aircraft)
            is_continue = False
            print(
                "Gate capacity: "
                + str(self._gate_capacity)
                + "\nAircraft capacity: "
                + str(self._max_passenger_on_aircraft)
            )
        return input_no, is_continue

    def read_passengers_from_file(self) -> int:
        """
        reads data from given file in instance variable file name
        :return: count of passengers
        """
        print("Reading passenger data from " + self._file_name)
        self._passenger_queue = Queue()
        total_passengers = 0
        with open(self._file_name) as file:
            for line in file:
                total_passengers += 1
                details = line.strip().split(",")
                passenger = Passenger(details[0], details[1], details[2] == "True")
                self._passenger_queue.enqueue(passenger)
        return total_passengers
