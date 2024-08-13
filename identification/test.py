import numpy as np

from .load import DataLoader
from .model import TubeIdentifier

def train_test_split(
    images: list[np.ndarray], target: np.ndarray, ratio: float = 0.8
) -> tuple[list[np.ndarray], np.ndarray, list[np.ndarray], np.ndarray]:
    num = len(images)
    indices = np.random.permutation(num)
    split = int(num * ratio)
    train_indices, test_indices = indices[:split], indices[split:]
    train_images, train_target = [images[i] for i in train_indices], target[train_indices]
    test_images, test_target = [images[i] for i in test_indices], target[test_indices]
    return train_images, train_target, test_images, test_target

def evaluate(model: TubeIdentifier, images: list[np.ndarray], target: np.ndarray) -> float:
    predictions = model.predict(images)
    accuracy = np.mean(predictions == target)
    return accuracy

def main():
    images, target = DataLoader().load()
    input_dim = images[0].shape[0]
    output_dim = np.max(target) + 1

    model = TubeIdentifier(input_dim, output_dim)
    train_images, train_target, test_images, test_target = train_test_split(images, target)
    model.train(train_images, train_target)

    accuracy = evaluate(model, test_images, test_target)
    print(f'Accuracy: {accuracy}')


if __name__ == "__main__":
    main()
