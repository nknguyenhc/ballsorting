from PIL import Image
import numpy as np

class DataLoader:
    def __init__(self, new_height: int = 60):
        self.new_height = new_height

    def load(
        self,
        path: str = 'data',
        num: int = 168,
        extension: str = 'png',
        target: str = 'target.txt',
        save_compress: bool = False,
    ) -> tuple[list[np.ndarray], np.ndarray, int, int]:
        images: list[np.ndarray] = []
        for i in range(num):
            image = Image.open(f'{path}/{i + 1}.{extension}')
            aspect_ratio = image.size[0] / image.size[1]
            new_width = int(self.new_height * aspect_ratio)
            image = image.resize((new_width, self.new_height))
            if save_compress:
                image.save(f'{path}/resized-{i + 1}.{extension}')
            images.append(np.array(image).reshape(-1))
        
        with open(f'{path}/{target}', 'r') as f:
            lines = f.readlines()
        target = np.array([int(line) for line in lines])

        assert len(images) == len(target), 'The number of images and target must be the same.'
        input_dim = images[0].shape[0]
        output_dim = np.max(target) + 1
        return images, target, input_dim, output_dim

    def load_image(self, path: str) -> np.ndarray:
        image = Image.open(path)
        aspect_ratio = image.size[0] / image.size[1]
        new_width = int(self.new_height * aspect_ratio)
        image = image.resize((new_width, self.new_height))
        return np.array(image).reshape(-1)
    
    def load_metadata(
        self,
        path: str = 'data',
        image_file: str = '1.png',
        target: str = 'target.txt',
    ) -> tuple[np.ndarray, int]:
        image = Image.open(f'{path}/{image_file}')
        aspect_ratio = image.size[0] / image.size[1]
        new_width = int(self.new_height * aspect_ratio)
        image = image.resize((new_width, self.new_height))
        image = np.array(image).reshape(-1)
        input_dim = image.shape[0]

        with open(f'{path}/{target}', 'r') as f:
            lines = f.readlines()
        target = np.array([int(line) for line in lines])
        output_dim = np.max(target) + 1
        return input_dim, output_dim
