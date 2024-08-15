from .load import DataLoader
from .model import TubeIdentifier
from .colour import ColourIdentifier

class Identifier:
    def __init__(self):
        self.data_loader = DataLoader()
        input_dim, output_dim = self.data_loader.load_metadata()
        self.model = TubeIdentifier(input_dim, output_dim)
        self.model.load_model()
        self.colour_identifier = ColourIdentifier()
    
    def identify(self, image_path: str) -> list[list[int]]:
        image = self.data_loader.load_image(image_path)
        print(f"Image loaded, shape {image.shape}")
        num_of_tubes = self.model.predict_single(image)
        print(f"Number of tubes: {num_of_tubes}")
        tubes, colour_names = self.colour_identifier.identify_colours(image_path, num_of_tubes)
        print(f"Puzzle: {tubes}")
        self.colour_names = colour_names
        return tubes
    
    def get_colour_name(self, ball: int) -> str:
        return self.colour_names[ball]
