import sys
import time

from algo import Agent, UnsolvablePuzzleException
from identification import Identifier
from state import State


class Manager:
    def solve(self, image_path: str, max_length: int = 4) -> None:
        identifier = Identifier()
        tubes = identifier.identify(image_path)
        puzzle = State(tubes, max_length)
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
        self._display_solution(moves, identifier)
    
    def _announce_time(self, start_time: float, end_time: float):
        print(f"Took {end_time - start_time:.3f} seconds")

    def _display_solution(self, moves: list[tuple[int, int]], identifier: Identifier) -> None:
        for move in moves:
            from_tube, to_tube = move
            ball = self.state.get_ball(from_tube)
            colour = identifier.get_colour_name(ball)
            next_state = self.state.move(move)
            n = self.state.balls_moved(next_state)
            try:
                input(f"{n} {colour}, {from_tube + 1} -> {to_tube + 1}.")
            except KeyboardInterrupt:
                return
            self.state = next_state
        print("Done")


def main():
    manager = Manager()
    image_path = sys.argv[1]
    manager.solve(image_path)


if __name__ == "__main__":
    main()
