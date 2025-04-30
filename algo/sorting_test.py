import unittest
from .sorting import Agent, UnsolvablePuzzleException
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
        with self.assertRaises(UnsolvablePuzzleException):
            agent.solve(puzzle)
    
    def test_split_move(self):
        agent = Agent()
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
        agent = Agent()
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
    
    def test_timing(self):
        agent = Agent()
        puzzle = State(
            [
                [3, 2, 1, 0],
                [6, 4, 5, 4],
                [7, 8, 7, 3],
                [10, 9, 2, 8],
                [9, 11, 10, 7],
                [8, 1, 7, 0],
                [9, 4, 1, 0],
                [8, 6, 5, 2],
                [11, 9, 11, 11],
                [2, 3, 3, 4],
                [6, 5, 10, 5],
                [1, 0, 6, 10],
                [],
                [],
            ],
            4,
        )
        moves = agent.solve(puzzle)
        self.assert_puzzle_solved(puzzle, moves)
    
    def test_timing_2(self):
        agent = Agent()
        puzzle = State(
            [
                [3, 2, 1, 0],
                [2, 5, 4, 4],
                [7, 6, 3, 0],
                [10, 0, 9, 8],
                [5, 8, 2, 5],
                [10, 7, 4, 1],
                [5, 0, 9, 6],
                [10, 9, 9, 2],
                [6, 1, 8, 11],
                [3, 1, 8, 11],
                [10, 11, 7, 11],
                [4, 6, 3, 7],
                [],
                [],
            ],
            4,
        )
        moves = agent.solve(puzzle)
        self.assert_puzzle_solved(puzzle, moves)


if __name__ == '__main__':
    unittest.main()
