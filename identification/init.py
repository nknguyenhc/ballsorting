from .load import DataLoader
from .model import TubeIdentifier

def main():
    images, target, input_dim, output_dim = DataLoader().load()

    model = TubeIdentifier(input_dim, output_dim)
    model.train(images, target)
    model.save_model()


if __name__ == "__main__":
    main()
