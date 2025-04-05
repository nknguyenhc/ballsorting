import unittest

from state import State
from .mcts import MctsAgent

class MctsTest(unittest.TestCase):
    def test_clear_board(self):
        state = State(
            [
                [0, 0, 0, 1],
                [0, 1, 1],
                [2, 1],
                [2, 2, 2],
            ],
            4
        )
        for _ in range(10):
            agent = MctsAgent(state, 3, time_limit=0.1)
            self.assertEqual(agent.next_move(state, fresh=True), (2, 1))
    
    def test_unclear_board(self):
        state = State(
            [
                [-1, 0, 0, 1],
                [0, 1, 1],
                [2, 1],
                [2, 2, 2],
            ],
            4
        )
        for _ in range(10):
            agent = MctsAgent(state, 3, time_limit=0.1)
            self.assertEqual(agent.next_move(state, fresh=True), (2, 1))
        
        state = State(
            [
                [-1, 0, 0, 1],
                [-1, 1, 1],
                [2, 1],
                [2, 2, 2],
            ],
            4
        )
        for _ in range(10):
            agent = MctsAgent(state, 3, time_limit=0.1)
            self.assertEqual(agent.next_move(state, fresh=True), (2, 1))
