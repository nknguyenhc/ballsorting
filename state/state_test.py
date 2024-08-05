import unittest
from .state import State

class TestState(unittest.TestCase):
    state = State(
        [
            [1, 2, 3],
            [2, 3, 3, 3],
            [1, 2, 3],
            [1, 3, 2],
            [],
        ],
        4,
    )

    def test_action(self):
        self.assertCountEqual(
            self.state.actions(),
            [(0, 2), (1, 0), (1, 2), (2, 0), (0, 4), (1, 4), (2, 4), (3, 4)],
        )
    
    def test_move(self):
        self.assertEqual(
            self.state.move((0, 2)),
            State(
                [
                    [1, 2],
                    [2, 3, 3, 3],
                    [1, 2, 3, 3],
                    [1, 3, 2],
                    [],
                ],
                4,
            ),
        )

        self.assertEqual(
            self.state.move((1, 0)),
            State(
                [
                    [1, 2, 3, 3],
                    [2, 3, 3],
                    [1, 2, 3],
                    [1, 3, 2],
                    [],
                ],
                4,
            ),
        )

        self.assertEqual(
            self.state.move((0, 4)),
            State(
                [
                    [1, 2],
                    [2, 3, 3, 3],
                    [1, 2, 3],
                    [1, 3, 2],
                    [3],
                ],
                4,
            ),
        )


if __name__ == '__main__':
    unittest.main()
