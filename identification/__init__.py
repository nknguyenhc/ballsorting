from .load import DataLoader
from .model import TubeIdentifier

data_loader = DataLoader()
input_dim, output_dim = data_loader.load_metadata()
model = TubeIdentifier(input_dim, output_dim)
model.load_model()
