import time

from state import State
from algo import Agent, UnsolvablePuzzleException


class Manager:
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
        validity = puzzle.find_invalid()
        if validity:
            self._raise_invalid(validity)
            return
        self.state = puzzle
        agent = Agent()
        start_time = time.time()
        try:
            moves = agent.solve(puzzle)
        except UnsolvablePuzzleException:
            end_time = time.time()
            self._announce_time(start_time, end_time)
            print("The puzzle is unsolvable.")
            return

        end_time = time.time()
        self._announce_time(start_time, end_time)
        self._display_solution(moves)

    def _welcome(self):
        print("Welcome to the Sorting Puzzle Manager!")

    def _get_num(self, message: str) -> int:
        while True:
            try:
                return int(input(message))
            except ValueError:
                print("Please enter a valid number.")

    def _get_tubes(self, num_of_tubes: int, max_length: int) -> list[list[int]]:
        tubes: list[list[int]] = []
        for i in range(num_of_tubes):
            tube = self._get_tube(i, max_length)
            print(f"Tube {i + 1}: {tube}")
            tubes.append(tube)
        return tubes

    def _get_tube(self, tube_num: int, max_length: int) -> list[int]:
        while True:
            response = input(f"Tube {tube_num + 1}: ")
            tube = response.strip().split(" ")
            if len(tube) > max_length:
                print(f"Tube {tube_num + 1} has too many balls.")
                continue

            number_tube: list[int] = []
            for ball in tube:
                if not ball:
                    continue
                if ball not in self.colour_dict:
                    self.colour_dict[ball] = self.colour_count
                    self.number_dict[self.colour_count] = ball
                    self.colour_count += 1
                number_tube.append(self.colour_dict[ball])

            return number_tube
    
    def _raise_invalid(self, validity: tuple[int, int]):
        colour_num, num = validity
        colour = self.number_dict[colour_num]
        print(f"Colour {colour} has the wrong number of balls: got {num}")

    def _announce_time(self, start_time: float, end_time: float):
        print(f"Took {end_time - start_time:.3f} seconds")

    def _display_solution(self, moves: list[tuple[int, int]]):
        for move in moves:
            from_tube, to_tube = move
            colour = self.number_dict[self.state.get_ball(from_tube)]
            next_state = self.state.move(move)
            n = self.state.balls_moved(next_state)
            try:
                input(
                    f"{n} {colour}, {from_tube + 1} -> {to_tube + 1}.")
            except KeyboardInterrupt:
                return
            self.state = next_state
        print("Done")


if __name__ == "__main__":
    manager = Manager()
    manager.run()
