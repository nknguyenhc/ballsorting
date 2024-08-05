import unittest
from .sorting import Agent, UnsolvablePuzzle
from state import State

class TestAgent(unittest.TestCase):
    def assert_puzzle_solved(self, puzzle: State, moves: list[tuple[int, int]]):
        print(f"{puzzle=}, {moves=}")
        state = puzzle
        for move in moves:
            self.assertTrue(move in state.actions())
            state = state.move(move)
        self.assertTrue(state.is_terminal())

    def test_1_move(self):
        agent = Agent()
        puzzle = State(
            [
                [1, 1, 1],
                [2, 2, 2, 2],
                [1],
            ],
            4,
        )
        moves = agent.solve(puzzle)
        self.assert_puzzle_solved(puzzle, moves)
    
    def test_4_moves(self):
        agent = Agent()
        puzzle = State(
            [
                [1, 1, 2, 1],
                [2, 2, 2],
                [1],
            ],
            4,
        )
        moves = agent.solve(puzzle)
        self.assert_puzzle_solved(puzzle, moves)
    
    def test_unsolvable(self):
        agent = Agent()
        puzzle = State(
            [
                [1, 1, 2],
                [2, 2, 2],
                [1],
            ],
            3,
        )
        with self.assertRaises(UnsolvablePuzzle):
            agent.solve(puzzle)


if __name__ == '__main__':
    unittest.main()
