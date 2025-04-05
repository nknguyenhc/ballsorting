from state import State
import math
import random
import time

class MctsNode:
    C = 1
    LOSE = -0.1
    WIN = 1

    def __init__(self,
                 agent: "MctsAgent",
                 state: State,
                 parent: "MctsNode" = None,
                 move: tuple[int, int] | None = None,
                 ):
        self.U = 0
        self.N = 0
        self.state = state
        self.parent = parent
        self.move = move
        self.agent = agent
    
    def ucb(self):
        if self.N == 0:
            return float('inf')
        return self.U / self.N + MctsNode.C * math.sqrt(math.log(self.parent.N) / self.N)
    
    def backprop(self, value: float):
        self.U += value
        self.N += 1
        if self.parent is not None:
            self.parent.backprop(value)

class MctsCertainNode(MctsNode):
    def __init__(self,
                 agent: "MctsAgent",
                 state: State,
                 parent: MctsNode | None = None,
                 move: tuple[int, int] | None = None,
                 ):
        super().__init__(agent, state, parent, move)
        self.children: list[MctsCertainNode | MctsUncertainNode] | None = None
    
    def search(self):
        leaf = self.select()
        child = leaf.expand()
        value = child.simulate()
        child.backprop(value)
    
    def select(self) -> "MctsCertainNode":
        if self.children is None or self.children == []:
            return self
        best_child = None
        for child in self.children:
            if best_child is None or child.ucb() > best_child.ucb():
                best_child = child
        return best_child.select()
    
    def expand(self) -> "MctsCertainNode":
        if self.children == []:
            return self
        self.children = []
        for action in self.state.actions():
            from_tube, _ = action
            next_state = self.state.move(action)
            if next_state.is_uncertain(from_tube):
                self.children.append(MctsUncertainNode(self.agent, next_state, from_tube, self, action))
            else:
                self.children.append(MctsCertainNode(self.agent, next_state, self, action))
        if self.children == []:
            return self
        idx = random.randint(0, len(self.children) - 1)
        child = self.children[idx]
        if isinstance(child, MctsCertainNode):
            return child
        else:
            return child.select()
    
    def simulate(self) -> float:
        if self.children == []:
            return MctsNode.WIN if self.state.is_terminal() else MctsNode.LOSE
        counts = list(self.agent.counts)
        total = self.agent.total
        state = self.state
        actions = state.actions()
        while len(actions) > 0:
            idx = random.randint(0, len(actions) - 1)
            action = actions[idx]
            from_tube, _ = action
            state = state.move(action)
            if not state.is_uncertain(from_tube):
                actions = state.actions()
                continue
            rand = random.randint(1, total)
            t = 0
            for colour, colour_count in enumerate(counts):
                t += colour_count
                if t >= rand:
                    break
            assert t >= rand and colour_count > 0, f"Failed with {counts=} {total=}"
            state = state.assign(from_tube, colour)
            counts[colour] -= 1
            total -= 1
            actions = state.actions()
        return MctsNode.WIN if self.state.is_terminal() else MctsNode.LOSE
    
    def best_move(self):
        assert self.children is not None and len(self.children) > 0
        best_child = None
        for child in self.children:
            if best_child is None or child.N > best_child.N:
                best_child = child
        return best_child.move

class MctsUncertainNode(MctsNode):
    def __init__(self,
                 agent: "MctsAgent",
                 state: State,
                 tube: int,
                 parent: MctsNode | None = None,
                 move: tuple[int, int] | None = None,
                 ):
        super().__init__(agent, state, parent, move)
        assert state.is_uncertain(tube)
        self.counts = tuple([count for count in self.agent.counts if count > 0])
        self.total = self.agent.total
        self.children = self._enumerate_children(tube)
        assert len(self.children) == len(self.counts)
    
    def _enumerate_children(self, tube: int) -> tuple[MctsCertainNode]:
        children: list[MctsCertainNode] = []
        for colour, colour_count in enumerate(self.agent.counts):
            if colour_count == 0:
                continue
            children.append(MctsCertainNode(self.agent, self.state.assign(tube, colour), self, None))
        return tuple(children)
    
    def select(self) -> MctsCertainNode:
        rand = random.randint(1, self.total)
        total = 0
        for i, colour_count in enumerate(self.counts):
            if total + colour_count < rand:
                total += colour_count
                continue
            return self.children[i].select()

class MctsAgent:
    def __init__(self,
                 initial_state: State,
                 num_colours: int,
                 time_limit: float = 1):
        self.balls = initial_state.clone().balls
        self.counts = self._build_counts(num_colours, initial_state.max_length)
        self.total = sum(self.counts)
        self.time_limit = time_limit
    
    def _build_counts(self, num_colours: int, max_length: int) -> list[int]:
        counts: list[int] = [max_length] * num_colours
        for tube in self.balls:
            for ball in tube:
                if ball != State.UNK:
                    counts[ball] -= 1
        return counts
    
    def _populate_state(self, state: State) -> None:
        assert len(state.balls) == len(self.balls)
        for i in range(len(state.balls)):
            assert len(self.balls[i]) == len(state.balls[i])
            for j in range(len(state.balls[i])):
                if state.balls[i][j] != State.UNK:
                    assert state.balls[i][j] == self.balls[i][j]
                elif self.balls[i][j] != State.UNK:
                    state.balls[i][j] = self.balls[i][j]
    
    def _update_belief(self, state: State) -> None:
        assert len(state.balls) == len(self.balls)
        for tube in range(len(state.balls)):
            for i in range(min(len(state.balls[tube]), len(self.balls[tube]))):
                if self.balls[tube][i] != State.UNK or state.balls[tube][i] == State.UNK:
                    continue
                self.balls[tube][i] = state.balls[tube][i]
                assert self.counts[state.balls[tube][i]] > 0
                self.counts[state.balls[tube][i]] -= 1
                self.total -= 1
    
    def next_move(self, state: State, fresh: bool = False) -> tuple[int, int]:
        """Returns the next best recommendation of a move.

        Parameters
        ---
        state: State
            The state to make a move on.
            This function will mutate the state.
        fresh: bool
            Whether this is a new game.
        """
        if fresh:
            self._populate_state(state)
        else:
            self._update_belief(state)
        root = MctsCertainNode(self, state)
        end_time = time.time() + self.time_limit
        while time.time() < end_time:
            root.search()
        # print(root.N)
        return root.best_move()
