class State:
    def __init__(self, balls: list[list[int]], max_length: int):
        """Instantiates a new state with the given tubes of balls.
        Each tube must have equal max length.
        Each colour is represented by a number.
        """
        self.balls = balls
        self.max_length = max_length
    
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
                if len(other_tube) == self.max_length:
                    continue
                if other_tube[-1] == tube[-1]:
                    actions.append((from_tube, to_tube))
        return actions
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        
        return self.max_length == other.max_length and self.balls == other.balls
