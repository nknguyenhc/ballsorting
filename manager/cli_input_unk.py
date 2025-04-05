from state import State
from algo import MctsAgent
from .cli_input import Manager as CliManager

class Manager(CliManager):
    def __init__(self):
        self.colour_dict: dict[str, int] = {}
        self.number_dict: dict[int, str] = {}
        self.colour_count = 0
    
    def run(self):
        self._welcome()
        num_of_tubes = self._get_num("Enter the number of tubes: ")
        max_length = self._get_num("Enter the max number of balls per tube: ")
        num_colours = self._get_num("Enter number of colours: ")

        balls = self._get_tubes(num_of_tubes, max_length)
        state = State(balls, max_length)
        agent = MctsAgent(state, num_colours)
        initial_state = state.clone()
        while not state.is_terminal():
            actions = state.actions()
            if len(actions) == 0:
                try:
                    input("Ran out of action. Restart ...")
                except KeyboardInterrupt:
                    return
                state  = initial_state.clone()
            action = agent.next_move(state, fresh=state == initial_state)
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
    
    def _get_tube(self, tube_num: int, max_length: int):
        while True:
            response = input(f"(? for unknown) Tube {tube_num + 1}: ")
            tube = response.strip().split()
            if len(tube) > max_length:
                print(f"Tube {tube_num + 1} has too many balls.")
                continue

            number_tube: list[int] = []
            for ball in tube:
                if not ball:
                    continue
                if ball == "?":
                    number_tube.append(State.UNK)
                    continue
                if ball not in self.colour_dict:
                    self.colour_dict[ball] = self.colour_count
                    self.number_dict[self.colour_count] = ball
                    self.colour_count += 1
                number_tube.append(self.colour_dict[ball])
            return number_tube
    
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


if __name__ == '__main__':
    manager = Manager()
    manager.run()
