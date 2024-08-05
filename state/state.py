class State:
    def __init__(self, balls: list[list[int]], max_length: int):
        """Instantiates a new state with the given tubes of balls.
        Each tube must have equal max length.
        Each colour is represented by a number.
        """
        self.balls = balls
        self.max_length = max_length
        self.hash: int | None = None
    
    def move(self, move: tuple[int, int]) -> "State":
        """Moves the top ball from the from_tube to the to_tube.
        This function does not check the validity of the move.
        """
        from_tube, to_tube = move
        new_balls = [tube.copy() for tube in self.balls]
        new_balls[to_tube].append(new_balls[from_tube].pop())
        return State(new_balls, self.max_length)
    
    def actions(self):
        """Returns a list of all possible moves from this state."""
        actions = []
        for from_tube, tube in enumerate(self.balls):
            for to_tube, other_tube in enumerate(self.balls):
                if from_tube == to_tube:
                    continue
                if len(other_tube) == self.max_length or len(tube) == 0:
                    continue
                if len(other_tube) == 0 or other_tube[-1] == tube[-1]:
                    actions.append((from_tube, to_tube))
        return actions
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        
        return self.max_length == other.max_length and self.balls == other.balls
    
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
