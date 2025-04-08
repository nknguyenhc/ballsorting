from state import State
from algo import MctsAgent
from .cli_input import Manager as CliManager
from .unk import UnkManager

class Manager(UnkManager, CliManager):
    def run(self):
        self._welcome()
        num_of_tubes = self._get_num("Enter the number of tubes: ")
        max_length = self._get_num("Enter the max number of balls per tube: ")
        num_colours = self._get_num("Enter number of colours: ")

        balls = self._get_tubes(num_of_tubes, max_length)
        state = State(balls, max_length)
        agent = MctsAgent(state, num_colours)
        self._run(state, agent)
    
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


if __name__ == '__main__':
    manager = Manager()
    manager.run()
