from state import State
from algo import MctsAgent

class UnkManager:
    def __init__(self):
        self.colour_dict: dict[str, int] = {}
        self.number_dict: dict[int, str] = {}
        self.colour_count = 0
    
    def _run(self, state: State, agent: MctsAgent) -> None:
        initial_state = state.clone()
        while not state.is_terminal():
            action = agent.next_move(state, fresh=state == initial_state)
            if action is None:
                try:
                    input("Ran out of action. Restart ...")
                except KeyboardInterrupt:
                    return
                state = initial_state.clone()
                continue
            next_state = state.move(action)
            from_tube, to_tube = action
            n = state.balls_moved(next_state)
            colour = self.number_dict[state.get_ball(from_tube)]
            try:
                input(f"{n} {colour}, {from_tube + 1} -> {to_tube + 1}")
            except KeyboardInterrupt:
                return
            state = next_state
            if state.is_uncertain(from_tube):
                colour = self._reveal_colour(from_tube)
                if colour is None:
                    return
                state = state.assign(from_tube, self.colour_dict[colour])

    def _reveal_colour(self, tube: int) -> str | None:
        while True:
            try:
                colour = input(f"Top ball at tube {tube + 1} is unknown. Please input its colour: ")
            except KeyboardInterrupt:
                return None
            if colour not in self.colour_dict:
                if not self._warn(colour):
                    continue
                self.colour_dict[colour] = self.colour_count
                self.number_dict[self.colour_count] = colour
                self.colour_count += 1
            return colour
    
    def _warn(self, colour: str) -> bool:
        response = input(f"Colour {colour} not previously found. Proceed (y/n)? ")
        if response == "y" or response == "yes":
            return True
        else:
            print("Colour not added")
            return False
