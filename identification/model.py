import torch
from torch import nn
import numpy as np
import os

class TubeIdentifierModel(nn.Module):
    def __init__(self, input_dim: int, output_dim: int):
        super().__init__()
        self.f = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, output_dim),
        )
    
    def forward(self, x):
        return self.f(x)


class TubeIdentifier:
    def __init__(self, input_dim: int, output_dim: int):
        self.model = TubeIdentifierModel(input_dim, output_dim)
    
    def save_model(self, path: str = 'data/model.pth'):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        torch.save(self.model.state_dict(), path)
    
    def load_model(self, path: str = 'data/model.pth'):
        assert os.path.exists(path), 'The model file does not exist.'
        self.model.load_state_dict(torch.load(path, weights_only=True))
    
    def train(self, images: list[np.ndarray], target: np.ndarray, epochs: int = 100):
        optimiser = torch.optim.Adam(self.model.parameters())
        loss_fn = nn.CrossEntropyLoss()

        images = torch.from_numpy(np.array(images)).float()
        target = torch.from_numpy(target).long()

        for i in range(epochs):
            optimiser.zero_grad()
            output = self.model.forward(images)
            loss = loss_fn.forward(output, target)
            loss.backward()
            optimiser.step()

            if i % 10 == 9:
                print(f'Epoch: {i + 1}, Loss: {loss.item()}')
    
    def predict(self, images: list[np.ndarray]) -> np.ndarray:
        images = torch.from_numpy(np.array(images)).float()
        return torch.argmax(self.model.forward(images), axis=1).numpy()
