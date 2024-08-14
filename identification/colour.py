import json
from PIL import Image
from PIL.ImageFile import ImageFile

class ColourIdentifier:
    def __init__(self,
        path: str = 'data/colours.json',
        distance_threshold: int = 20,
        balls_per_tube: int = 4,
        colour_name_path: str = 'data/colour_names.json',
    ):
        with open(path, 'r') as f:
            self.colours = json.load(f)
        self._validate_colours()
        self.distance_threshold = distance_threshold
        self.balls_per_tube = balls_per_tube
        with open(colour_name_path, 'r') as f:
            self.colour_names = json.load(f)
        self._validate_colour_names()
    
    def _validate_colour_names(self) -> None:
        for colour in self.colour_names:
            if "name" not in colour or "rgb" not in colour:
                raise ValueError(f'"name" or "rgb" key not found in colour: {colour}')
            if not isinstance(colour["name"], str):
                raise ValueError(f'Invalid name: {colour["name"]}')
            if not isinstance(colour["rgb"], list):
                raise ValueError(f'Invalid rgb: {colour["rgb"]}')
            if len(colour["rgb"]) != 3:
                raise ValueError(f'Invalid rgb length: {len(colour["rgb"])}, expected 3')
            for rgb in colour["rgb"]:
                if not isinstance(rgb, int) or rgb < 0 or rgb > 255:
                    raise ValueError(f'Invalid rgb value: {rgb}')
    
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
    
    def identify_colours(self, image_path: str, num_of_tubes: int) -> tuple[list[list[int]], list[str]]:
        if str(num_of_tubes) not in self.colours:
            raise ValueError(f'Invalid number of tubes: {num_of_tubes}')
        data = self.colours[str(num_of_tubes)]
        image = Image.open(image_path)
        tubes: list[list[int]] = []
        colours: list[tuple[int, int, int]] = []
        for i in range(num_of_tubes):
            tube = self._identify_tube(image, data["positions"][i], data["distance"], colours)
            tubes.append(tube)
        colour_names = self._get_colour_names(colours)
        return tubes, colour_names
    
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
    
    def _get_colour_names(self, colours: list[tuple[int, int, int]]) -> list[str]:
        colour_names: list[str] = []
        for colour in colours:
            colour_names.append(self._get_colour_name(colour))
        return colour_names
    
    def _get_colour_name(self, colour: tuple[int, int, int]) -> str:
        min_distance = float('inf')
        colour_name = ''
        for model_colour in self.colour_names:
            distance = self._calculate_distance(colour, model_colour["rgb"])
            if distance < min_distance:
                min_distance = distance
                colour_name = model_colour["name"]
        return colour_name


if __name__ == '__main__':
    ci = ColourIdentifier()
    print(ci.identify_colours('data/1.png', 7))
