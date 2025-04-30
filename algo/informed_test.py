import unittest
from .informed import InformedAgent, UnsolvablePuzzleException
from state import State

class TestInformedAgent(unittest.TestCase):
    def assert_puzzle_solved(self, puzzle: State, moves: list[tuple[int, int]]):
        print(f"{puzzle=}, {moves=}")
        state = puzzle
        for move in moves:
            self.assertTrue(move)
            state = state.move(move)
        self.assertTrue(state.is_terminal())
    
    def test_1_move(self):
        agent = InformedAgent()
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
        agent = InformedAgent()
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
        agent = InformedAgent()
        puzzle = State(
            [
                [1, 1, 2],
                [2, 2, 2],
                [1],
            ],
            3,
        )
        with self.assertRaises(UnsolvablePuzzleException):
            agent.solve(puzzle)
    
    def test_split_move(self):
        agent = InformedAgent()
        puzzle = State(
            [
                [0, 0, 1, 1],
                [2, 2, 1],
                [2, 2, 1],
                [0, 0],
            ],
            4,
        )
        moves = agent.solve(puzzle)
        self.assert_puzzle_solved(puzzle, moves)
    
    def test_waiting_move(self):
        agent = InformedAgent()
        puzzle = State(
            [
                [0, 0, 1, 1],
                [0, 0, 1],
                [1, 2, 2],
                [2, 2],
            ],
            4,
        )
        moves = agent.solve(puzzle)
        self.assert_puzzle_solved(puzzle, moves)
        self.assertTrue(len(moves) <= 5)


if __name__ == '__main__':
    unittest.main()
