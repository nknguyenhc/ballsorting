import sys

from algo import MctsAgent
from identification import Identifier
from state import State
from .unk import UnkManager


class Manager(UnkManager):
    def solve(self, image_path: str, max_length: int = 4) -> None:
        identifier = Identifier()
        tubes, colour_names = identifier.identify_unk(image_path)
        num_of_colours = len(tubes) - 2
        self._build_dicts(colour_names)
        state = State(tubes, max_length)
        agent = MctsAgent(state, num_of_colours)
        self._run(state, agent)
    
    def _build_dicts(self, colour_names: list[str]) -> None:
        for i, colour_name in enumerate(colour_names):
            self.number_dict[i] = colour_name
            self.colour_dict[colour_name] = i
        self.colour_count = len(colour_names)


def main():
    manager = Manager()
    image_path = sys.argv[1]
    manager.solve(image_path)


if __name__ == '__main__':
    main()
