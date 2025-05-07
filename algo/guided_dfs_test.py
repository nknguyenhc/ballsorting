import unittest

from .guided_dfs import GuidedAgent
from .sorting import UnsolvablePuzzleException
from state import State

one_move = State(
    [
        [1, 1, 1],
        [2, 2, 2, 2],
        [1],
    ],
    4,
)

four_moves = State(
    [
        [1, 1, 2, 1],
        [2, 2, 2],
        [1],
    ],
    4,
)

unsolvable = State(
    [
        [1, 1, 2],
        [2, 2, 2],
        [1],
    ],
    3,
)

split_move = State(
    [
        [0, 0, 1, 1],
        [2, 2, 1],
        [2, 2, 1],
        [0, 0],
    ],
    4,
)

waiting_move = State(
    [
        [0, 0, 1, 1],
        [0, 0, 1],
        [1, 2, 2],
        [2, 2],
    ],
    4,
)

timing_1 = State(
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

timing_2 = State(
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

timing_3 = State(
    [
        [0, 2, 1, 0],
        [6, 5, 4, 3],
        [7, 2, 4, 1],
        [3, 0, 7, 8],
        [10, 8, 9, 2],
        [8, 2, 11, 9],
        [5, 11, 11, 8],
        [4, 10, 6, 3],
        [9, 10, 11, 4],
        [5, 0, 1, 6],
        [5, 1, 6, 10],
        [3, 7, 7, 9],
        [],
        [],
    ],
    4,
)

timing_unsolvable = State(
    [
        [2, 11, 4, 1],
        [2, 11, 4, 11],
        [9, 8, 4, 9],
        [1, 7, 10, 9],
        [10, 3, 12, 3],
        [8, 12, 10, 7],
        [7, 6, 10, 8],
        [5, 2, 12, 5],
        [9, 4, 6, 7],
        [3, 3, 11, 12],
        [8, 1, 1, 5],
        [5, 6, 6, 2],
        [],
        [],
    ],
    4,
)

class TestMoves(unittest.TestCase):
    def assert_correct_moves(self,
                             generated_moves: list[tuple[int, int]],
                             correct_moves: list[tuple[int, int]],
                             ):
        self.assertTrue(len(set(generated_moves)) == len(generated_moves),
                        f"Duplicate moves found in {generated_moves}")
        correct_moves = set(correct_moves)
        for move in generated_moves:
            self.assertTrue(move in correct_moves,
                            f"Generated move {move} not found in {correct_moves}")
    
    def try_state(self, state: State):
        agent = GuidedAgent()
        correct_moves = state.actions()
        for moves, _ in agent._actions(state):
            self.assert_correct_moves(moves, correct_moves)
    
    def test_1_move(self):
        self.try_state(one_move)
    
    def test_4_move(self):
        self.try_state(four_moves)
    
    def test_unsolvable(self):
        self.try_state(unsolvable)
    
    def test_split_move(self):
        self.try_state(split_move)
    
    def test_waiting_move(self):
        self.try_state(waiting_move)
    
    def test_timing_1(self):
        self.try_state(timing_1)
    
    def test_timing_2(self):
        self.try_state(timing_2)
    
    def test_timing_3(self):
        self.try_state(timing_3)
    
    def test_timing_unsolvable(self):
        self.try_state(timing_unsolvable)

class TestAgent(unittest.TestCase):
    def assert_puzzle_solved(self, puzzle: State, moves: list[tuple[int, int]]):
        # print(f"{puzzle=} {moves=}")
        state = puzzle
        for move in moves:
            self.assertTrue(move in state.actions())
            state = state.move(move)
        self.assertTrue(state.is_terminal())
    
    def try_state(self, state: State):
        agent = GuidedAgent()
        moves = agent.solve(state)
        self.assert_puzzle_solved(state, moves)
    
    def test_1_move(self):
        self.try_state(one_move)
    
    def test_4_move(self):
        self.try_state(four_moves)
    
    def test_unsolvable(self):
        agent = GuidedAgent()
        with self.assertRaises(UnsolvablePuzzleException):
            agent.solve(unsolvable)
    
    def test_split_move(self):
        self.try_state(split_move)
    
    def test_waiting_move(self):
        self.try_state(waiting_move)
    
    def test_timing_1(self):
        self.try_state(timing_1)
    
    def test_timing_2(self):
        self.try_state(timing_2)
    
    def test_timing_3(self):
        self.try_state(timing_3)
    
    def test_timing_unsolvable(self):
        agent = GuidedAgent()
        with self.assertRaises(UnsolvablePuzzleException):
            agent.solve(timing_unsolvable)


if __name__ == '__main__':
    unittest.main()
