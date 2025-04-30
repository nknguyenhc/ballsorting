from state import State
import time
from sortedcontainers import SortedList

class UnsolvablePuzzleException(Exception):
    def __init__(self):
        super().__init__("The puzzle is unsolvable.")

class InformedNode:
    def __init__(self, state: State,
                 g: int,
                 h: int | None = None,
                 action: tuple[int, int] | None = None,
                 parent: "InformedNode" = None,
                 ):
        self.state = state
        self.g = g
        self.h = h if h is not None else self._h(state)
        self.action = action
        self.parent = parent
    
    def _h(self, state: State):
        count = 0
        for tube in state.balls:
            for i in range(len(tube) - 1):
                if tube[i] != tube[i + 1]:
                    count += 1
        return count
    
    def __eq__(self, node: "InformedNode"):
        return self.g + self.h == node.g + node.h
    
    def __lt__(self, node: "InformedNode"):
        return node.g + node.h < self.g + self.h
    
    def __lte__(self, node: "InformedNode"):
        return node.g + node.h <= self.g + self.h
    
    def __gt__(self, node: "InformedNode"):
        return node.g + node.h > self.g + self.h
    
    def __gte__(self, node: "InformedNode"):
        return node.g + node.h >= self.g + self.h
    
    def next_nodes(self) -> list["InformedNode"]:
        nodes: list[InformedNode] = []
        for action in self.state.actions():
            from_tube, _ = action
            next_state = self.state.move(action)
            if all(ball == self.state.balls[from_tube][0] for ball in self.state.balls[from_tube]):
                h = self.h
            else:
                h = self.h - 1
            nodes.append(InformedNode(next_state, self.g + 1, h, action, self))
        return nodes

class InformedAgent:
    def __init__(self):
        self.visited_states: set[State] = set()
    
    def solve(self, puzzle: State) -> list[tuple[int, int]]:
        self.visited_states.clear()
        start_time = time.time()
        moves = self._solve(puzzle)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time:.3f} seconds")
        if moves is None:
            raise UnsolvablePuzzleException()
        return list(reversed(moves))
    
    def _solve(self, puzzle: State) -> list[tuple[int, int]] | None:
        frontier: SortedList[InformedNode] = SortedList()
        visited: set[State] = set()
        frontier.add(InformedNode(puzzle, 0))
        while len(frontier) > 0:
            node: InformedNode = frontier.pop()
            for next_node in node.next_nodes():
                if next_node.state in visited:
                    continue
                if next_node.state.is_terminal():
                    return self._backtrack(next_node)
                visited.add(next_node.state)
                frontier.add(next_node)
        return None
    
    def _backtrack(self, node: InformedNode) -> list[tuple[int, int]]:
        actions: list[tuple[int, int]] = []
        while node.action is not None:
            actions.append(node.action)
            node = node.parent
        return actions
