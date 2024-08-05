from state import State

class UnsolvablePuzzle(Exception):
    def __init__(self):
        super().__init__("The puzzle is unsolvable.")

class Agent:
    def __init__(self):
        self.visited_states: set[State] = set()

    def solve(self, puzzle: State) -> list[tuple[int, int]]:
        """Solves the puzzle and returns a list of moves."""
        self.visited_states.clear()
        moves = self._solve(puzzle)
        if moves is None:
            raise UnsolvablePuzzle()
        return list(reversed(moves))
    
    def _solve(self, puzzle: State) -> list[tuple[int, int]] | None:
        if puzzle.is_terminal():
            return []
        
        if puzzle in self.visited_states:
            return None
        
        for action in puzzle.actions():
            new_state = puzzle.move(action)
            self.visited_states.add(puzzle)
            result = self._solve(new_state)
            if result is not None:
                result.append(action)
                return result
        
        return None
