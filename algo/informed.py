from state import State
import time
from sortedcontainers import SortedList

class UnsolvablePuzzleException(Exception):
    def __init__(self):
        super().__init__("The puzzle is unsolvable.")

class InformedNode:
    def __init__(self, state: State,
                 h: int | None = None,
                 action: tuple[int, int] | None = None,
                 parent: "InformedNode" = None,
                 ):
        self.state = state
        self.h = h if h is not None else self._h(state)
        # assert self.h == self._h(state), f"Failed for {state=} {action=} {self.h=} {self._h(state)=}"
        self.action = action
        self.parent = parent
    
    def _h(self, state: State):
        count = 0
        num_balls = 0
        for tube in state.balls:
            num_balls += len(tube)
            for i in range(len(tube) - 1):
                if tube[i] == tube[i + 1]:
                    count += 1
        max_links = num_balls // state.max_length * (state.max_length - 1)
        return max_links - count
    
    def __eq__(self, node: "InformedNode"):
        return self.h == node.h
    
    def __lt__(self, node: "InformedNode"):
        return node.h < self.h
    
    def __lte__(self, node: "InformedNode"):
        return node.h <= self.h
    
    def __gt__(self, node: "InformedNode"):
        return node.h > self.h
    
    def __gte__(self, node: "InformedNode"):
        return node.h >= self.h
    
    def next_nodes(self) -> list["InformedNode"]:
        nodes: list[InformedNode] = []
        for action in self.state.actions():
            from_tube, to_tube = action
            colour = self.state.balls[from_tube][-1]
            next_state = self.state.move(action)
            if len(next_state.balls[from_tube]) > 0 and next_state.balls[from_tube][-1] == colour:
                if len(self.state.balls[to_tube]) > 0:
                    h = self.h
                else:
                    h = self.h + 1
            else:
                if len(self.state.balls[to_tube]) > 0:
                    h = self.h - 1
                else:
                    h = self.h
            nodes.append(InformedNode(next_state, h, action, self))
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
        frontier.add(InformedNode(puzzle))
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
