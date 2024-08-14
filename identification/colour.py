import json
from PIL import Image
from PIL.ImageFile import ImageFile

class ColourIdentifier:
    def __init__(self,
        path: str = 'data/colours.json',
        distance_threshold: int = 20,
        balls_per_tube: int = 4,
    ):
        with open(path, 'r') as f:
            self.colours = json.load(f)
        self._validate_colours()
        self.distance_threshold = distance_threshold
        self.balls_per_tube = balls_per_tube
    
    def _validate_colours(self) -> None:
        for key in self.colours:
            if not key.isdigit():
                raise ValueError(f'Invalid key: {key}')
            data = self.colours[key]
            if "positions" not in data or "distance" not in data:
                raise ValueError(f'"positions" or "distance" key not found in data: {data}')
            if not isinstance(data["positions"], list):
                raise ValueError(f'Invalid positions: {data["positions"]}')
            if len(data["positions"]) != int(key):
                raise ValueError(f'Invalid number of positions: {len(data["positions"])}, expected {key}')
            for position in data["positions"]:
                if not isinstance(position, dict):
                    raise ValueError(f'Invalid position: {position}')
                if "x" not in position or "y" not in position:
                    raise ValueError(f'"x" or "y" key not found in position: {position}')
                if not isinstance(position["x"], float) or position["x"] <= 0 or position["x"] >= 1:
                    raise ValueError(f'Invalid x: {position["x"]}')
                if not isinstance(position["y"], float) or position["y"] <= 0 or position["y"] >= 1:
                    raise ValueError(f'Invalid y: {position["y"]}')
            if not isinstance(data["distance"], float):
                raise ValueError(f'Invalid distance: {data["distance"]}')
    
    def identify_colours(self, image_path: str, num_of_tubes: int) -> list[list[int]]:
        if str(num_of_tubes) not in self.colours:
            raise ValueError(f'Invalid number of tubes: {num_of_tubes}')
        data = self.colours[str(num_of_tubes)]
        image = Image.open(image_path)
        tubes: list[list[int]] = []
        colours: list[tuple[int, int, int]] = []
        for i in range(num_of_tubes):
            tube = self._identify_tube(image, data["positions"][i], data["distance"], colours)
            tubes.append(tube)
        return tubes
    
    def _identify_tube(
        self,
        image: ImageFile,
        position: dict[str, float],
        distance: float,
        colours: list[tuple[int, int, int]],
    ) -> list[int]:
        tube: list[int] = []
        for i in range(self.balls_per_tube):
            pixel: tuple[int, int, int] = image.getpixel((
                position["x"] * image.width,
                (position["y"] + distance * i) * image.height,
            ))
            colour = self._identify_colour(pixel, colours)
            if colour is None:
                return []
            tube.append(colour)
        tube.reverse()
        return tube
    
    def _identify_colour(self, pixel: tuple[int, int, int], colours: list[tuple[int, int, int]]) -> int | None:
        if self._calculate_distance(pixel, (0, 0, 0)) <= self.distance_threshold:
            return None
        for i, colour in enumerate(colours):
            if self._calculate_distance(pixel, colour) <= self.distance_threshold:
                return i
        colours.append(pixel)
        return len(colours) - 1

    def _calculate_distance(self, pixel: tuple[int, int, int], colour: tuple[int, int, int]) -> float:
        return sum((pixel[i] - colour[i]) ** 2 for i in range(3)) ** 0.5


if __name__ == '__main__':
    ci = ColourIdentifier()
    print(ci.identify_colours('data/1.png', 7))
