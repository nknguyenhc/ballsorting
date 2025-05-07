from typing import Iterator
from collections import defaultdict

from state import State
from .sorting import UnsolvablePuzzleException

class GuidedAgent:
    def __init__(self):
        self.visited_states: set[State] = set()

    def solve(self, puzzle: State) -> list[tuple[int, int]]:
        self.visited_states.clear()
        moves = self._solve(puzzle)
        if moves is None:
            raise UnsolvablePuzzleException()
        return list(reversed(moves))

    def _solve(self, puzzle: State) -> list[tuple[int, int]] | None:
        if puzzle.is_terminal():
            return []
        
        for actions, next_state in self._actions(puzzle):
            result = self._solve(next_state)
            if result is not None:
                result.extend(list(reversed(actions)))
                return result
        
        return None
    
    def _actions(self, state: State) -> Iterator[tuple[list[tuple[int, int]], State]]:
        """Returns the list of actionables and their next states.
        Each element is a tuple, where,
        1. The first element is a list of actions that, when applied on current state,
        returns the next state.
        2. The second element is the next state.
        """
        if state.from_tube is not None:
            return self._transfer_actions(state)
        for i, tube in enumerate(state.balls):
            if len(tube) == 0:
                return self._fill_actions(state, i)
        return self._transfer_actions(state)
    
    def _transfer_actions(self, state: State) -> Iterator[tuple[list[tuple[int, int]], State]]:
        actions = state.actions()
        self._sort_transfer_actions(state, actions)
        for action in actions:
            next_state = state.move(action)
            if next_state in self.visited_states:
                continue
            self.visited_states.add(next_state)
            yield [action], next_state
    
    def _sort_transfer_actions(self, state: State, actions: list[tuple[int, int]]):
        tube_scores = self._get_tube_scores(state)
        actions.sort(key=lambda action: -tube_scores[action[0]])
    
    def _get_tube_scores(self, state: State) -> list[int]:
        colour_scores: defaultdict[int, int] = defaultdict(int)
        for tube in state.balls:
            if len(tube) == state.max_length or len(tube) == 0:
                continue
            if all(ball == tube[0] for ball in tube):
                colour_scores[tube[0]] = 2
            else:
                colour_scores[tube[-1]] = max(colour_scores[tube[-1]], 1)

        tube_scores: list[int] = []
        for tube in state.balls:
            if all(ball == tube[0] for ball in tube):
                tube_scores.append(0)
                continue
            score = 0
            for i in range(len(tube) - 2, -1, -1):
                if colour_scores[tube[i]] == 0:
                    break
                score += colour_scores[tube[i]]
            tube_scores.append(score)
        return tube_scores
    
    def _fill_actions(self, state: State, index: int) -> Iterator[tuple[list[tuple[int, int]], State]]:
        colour_map: defaultdict[int, list[int]] = defaultdict(list)
        for i, tube in enumerate(state.balls):
            if len(tube) == 0:
                continue
            colour_map[tube[-1]].append(i)
        
        l: list[tuple[list[tuple[int, int]], State, int]] = []
        for _, tubes in colour_map.items():
            actions = [(tube, index) for tube in tubes]
            next_state = state
            for action in actions:
                next_state = next_state.move(action)
            if next_state in self.visited_states:
                continue
            self.visited_states.add(next_state)
            tube_scores = self._get_tube_scores(next_state)
            score = sum(tube_scores)
            l.append((actions, next_state, score))
        l.sort(key=lambda item: -item[2])
        for actions, next_state, _ in l:
            yield actions, next_state
