import time

from state import State
from algo import GuidedAgent, UnsolvablePuzzleException
from .cli_input import Manager as CliManager


class Manager(CliManager):
    def __init__(self):
        self.colour_dict: dict[str, int] = {}
        self.number_dict: dict[int, str] = {}
        self.colour_count = 0

    def run(self):
        self._welcome()
        num_of_tubes = self._get_num("Enter the number of tubes: ")
        max_length = self._get_num("Enter the max number of balls per tube: ")

        balls = self._get_tubes(num_of_tubes, max_length)
        puzzle = State(balls, max_length)
        self.state = puzzle
        agent = GuidedAgent()
        start_time = time.time()
        try:
            moves = agent.solve(puzzle)
            end_time = time.time()
        except UnsolvablePuzzleException:
            end_time = time.time()
            self._announce_time(end_time, start_time)
            print("The puzzle is unsolvable.")
            return

        end_time = time.time()
        self._announce_time(start_time, end_time)
        self._display_solution(moves)

    def _welcome(self):
        print("Welcome to the Sorting Puzzle Manager! This programme runs the guided DFS algorithm.")


if __name__ == "__main__":
    manager = Manager()
    manager.run()
