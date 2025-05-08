class ExpressMoveException(Exception):
    def __init__(self, move: tuple[int, int]):
        self.move = move

class State:
    UNK = -1

    def __init__(self, balls: list[list[int]], max_length: int, from_tube: int | None = None):
        """Instantiates a new state with the given tubes of balls.
        Each tube must have equal max length.
        Each colour is represented by a number.
        """
        self.balls = balls
        self.max_length = max_length
        self.hash: int | None = None
        self.from_tube = from_tube
    
    def move(self, move: tuple[int, int]) -> "State":
        """Moves the top ball from the from_tube to the to_tube.
        This function does not check the validity of the move.
        """
        from_tube, to_tube = move
        assert self.from_tube is None or from_tube == self.from_tube
        new_balls = [tube.copy() for tube in self.balls]
        colour = new_balls[from_tube][-1]
        while len(new_balls[from_tube]) > 0 \
                and len(new_balls[to_tube]) < self.max_length \
                and new_balls[from_tube][-1] == colour:
            new_balls[to_tube].append(new_balls[from_tube].pop())
        new_from_tube = from_tube if len(new_balls[from_tube]) > 0 and new_balls[from_tube][-1] == colour else None
        return State(new_balls, self.max_length, from_tube=new_from_tube)
    
    def is_valid_move(self, move: tuple[int, int], check_from_move: bool = True) -> bool:
        from_tube, to_tube = move
        if check_from_move and self.from_tube is not None and from_tube != self.from_tube:
            return False
        if len(self.balls[to_tube]) > 0 and self.balls[from_tube][-1] != self.balls[to_tube][-1]:
            return False
        if len(self.balls[to_tube]) == self.max_length:
            return False
        return True
    
    def actions(self) -> list[tuple[int, int]]:
        """Returns a list of all possible moves from this state."""
        try:
            return self._actions()
        except ExpressMoveException as e:
            return [e.move]
    
    def _actions(self) -> list[tuple[int, int]]:
        actions = []
        if self.from_tube is not None:
            self._actions_from_tube(self.from_tube, actions)
        else:
            for from_tube in range(len(self.balls)):
                self._actions_from_tube(from_tube, actions)
        return actions

    def _actions_from_tube(self, from_tube: int, actions: list[tuple]) -> None:
        """Appends all possible moves from the given tube to the actions list."""
        if len(self.balls[from_tube]) == 0:
            return
        uniform_from = all(ball == self.balls[from_tube][0] for ball in self.balls[from_tube])
        for to_tube, other_tube in enumerate(self.balls):
            if from_tube == to_tube:
                continue
            if len(other_tube) == self.max_length:
                continue
            if uniform_from and all(ball == self.balls[from_tube][0] for ball in other_tube):
                if len(other_tube) < len(self.balls[from_tube]):
                    continue
                raise ExpressMoveException((
                    max(from_tube, to_tube),
                    min(from_tube, to_tube),
                ))
            if len(other_tube) == 0 or other_tube[-1] == self.balls[from_tube][-1]:
                actions.append((from_tube, to_tube))
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        
        return self.max_length == other.max_length and self.balls == other.balls and self.from_tube == other.from_tube
    
    def is_terminal(self) -> bool:
        """Returns True if the puzzle is solved."""
        return all(
            all(ball == balls[0] for ball in balls) and len(balls) == self.max_length
            if len(balls) > 0 else True
            for balls in self.balls
        )
    
    def __hash__(self):
        if self.hash is None:
            self.hash = hash(tuple(map(tuple, self.balls)))
        return self.hash
    
    def __repr__(self):
        return f"State({self.balls}, {self.max_length})"
    
    def __str__(self):
        return self.__repr__()
    
    def get_ball(self, tube: int) -> int:
        """Returns the top ball of the given tube.
        Assuming that the tube is not empty.
        """
        return self.balls[tube][-1]
    
    def balls_moved(self, state: "State") -> int:
        for tube1, tube2 in zip(self.balls, state.balls):
            if len(tube1) != len(tube2):
                return abs(len(tube1) - len(tube2))
        return 0
    
    def is_uncertain(self, tube: int):
        return len(self.balls[tube]) > 0 and self.balls[tube][-1] == State.UNK
    
    def assign(self, tube: int, colour: int) -> "State":
        """Assign the top ball of this tube to the colour,
        returning a new copy.
        The tube must have ball and the top ball must be unknown.
        """
        assert self.is_uncertain(tube)
        new_balls = [t.copy() for t in self.balls]
        new_balls[tube][-1] = colour
        return State(new_balls, self.max_length, self.from_tube)
    
    def clone(self) -> "State":
        return State([t.copy() for t in self.balls], self.max_length, self.from_tube)
