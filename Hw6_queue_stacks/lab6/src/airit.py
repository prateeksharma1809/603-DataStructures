"""
CSCI-603 Lab 6: AiRIT

a new airline dedicated to getting
students to their Spring Break destination free of charge

author: Prateek Sharma
"""

import os
import sys

from airport import Airport


def run_simulation(file_name: str) -> None:
    """
    method to start the simulation of airport
    :param file_name: file from command line
    """
    airport = Airport(file_name)
    airport.take_user_inputs()
    total_passengers = airport.read_passengers_from_file()
    print("Beginning simulation...")
    total_flights = airport.start_airport()
    print(
        "Simulation complete. Statistics: "
        + str(total_flights)
        + " flights, "
        + str(total_passengers)
        + " passengers are at their destination"
    )


def main() -> None:
    """
    main function to start the program
    """
    if len(sys.argv) != 2:
        print("Usage: python3 airit.py {filename}")
    elif not os.path.exists(sys.argv[-1]):
        print("File not found: " + sys.argv[-1])
    else:
        run_simulation(sys.argv[-1])


if __name__ == "__main__":
    main()
