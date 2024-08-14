import sys

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
        try:
            moves = agent.solve(puzzle)
        except UnsolvablePuzzleException:
            print("The puzzle is unsolvable.")
            return
        
        self._display_solution(moves, identifier)
    
    def _display_solution(self, moves: list[tuple[int, int]], identifier: Identifier) -> None:
        for move in moves:
            from_tube, to_tube = move
            ball = self.state.get_ball(from_tube)
            colour = identifier.get_colour_name(ball)
            input(f"{colour}, {from_tube + 1} -> {to_tube + 1}.")
            self.state = self.state.move(move)
        print("Done")

def main():
    manager = Manager()
    image_path = sys.argv[1]
    manager.solve(image_path)


if __name__ == "__main__":
    main()
