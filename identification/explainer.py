import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn

from .load import DataLoader
from .model import TubeIdentifier

class Explainer:
    def __init__(self, grey_color: tuple[int, ...] = (0, 0, 0)):
        self.data_loader = DataLoader()
        input_dim, output_dim = self.data_loader.load_metadata()
        self.model = TubeIdentifier(input_dim, output_dim)
        self.model.load_model()
        self.output_dim = output_dim
        self.grey_color = np.array(grey_color)
    
    def explain(self,
                path: str,
                epochs: int = 1000,
                ):
        image = self.data_loader.load_image(path, flatten=False)
        cl = self.model.predict_single(image.reshape(-1))
        mask = torch.arange(0, self.output_dim, 1) != cl
        h, w, _ = image.shape
        inputs, images, pis = self._sample_around(image)
        probas = self.model.predict_probas(images)
        probas = torch.hstack((torch.sum(probas[:, mask], dim=1)[:, None], probas[:, ~mask]))
        inputs, pis, probas = self._upsample(inputs, pis, probas)
        g = nn.Linear(h * w, 2)
        optimizer = torch.optim.Adam(g.parameters(), lr=0.01)
        for i in range(epochs):
            optimizer.zero_grad()
            output = g(inputs)
            loss = torch.sum(pis * torch.sum(torch.square(probas - output), dim=1))
            loss.backward()
            optimizer.step()

            if i % 10 == 9:
                print(f"Epoch: {i + 1}, Loss: {loss.item()}")
        
        self._analyse(g, image)
    
    def _sample_around(self,
                       image: np.ndarray,
                       sample_size: int = 10000,
                       ) -> tuple[list[np.ndarray], list[np.ndarray], list[float]]:
        inputs: list[np.array] = []
        results: list[np.ndarray] = []
        pis: list[float] = []
        h, w, _ = image.shape
        num_pixels_to_change = np.random.choice(h * w, sample_size)
        for n in num_pixels_to_change:
            mask = np.random.choice(h * w, n, replace=False)
            input = np.ones(h * w)
            input[mask] = 0
            inputs.append(input)
            im = image.reshape(h * w, 3).copy()
            im[mask] = self.grey_color
            results.append(im.reshape(h, w, 3))
            pi = 1.0
            pis.append(pi)
        return inputs, results, pis
    
    def _upsample(self,
                  inputs: list[np.ndarray],
                  pis: list[float],
                  probas: torch.Tensor
                  ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        labels = np.argmax(probas.detach().numpy(), axis=1)
        assert np.count_nonzero(labels == 0) > 0
        upsample_size = np.count_nonzero(labels == 1) - np.count_nonzero(labels == 0)
        assert upsample_size > 0
        indices = np.where(labels == 0)[0]
        samples = np.random.choice(indices, upsample_size)
        inputs = torch.tensor(np.array(inputs)).float()
        inputs = torch.vstack((inputs[labels == 0], inputs[samples], inputs[labels == 1]))
        pis = torch.tensor(pis)
        pis = torch.concat((pis[labels == 0], pis[samples], pis[labels == 1]))
        probas = torch.vstack((probas[labels == 0], probas[samples], probas[labels == 1]))
        return inputs, pis, probas
    
    def _analyse(self,
                 g: nn.Linear,
                 image: np.ndarray,
                 weight_threshold: float = 0.001,
                 ):
        h, w, _ = image.shape
        params = list(g.parameters())[0].detach().numpy()[1].reshape(h, w)
        image[params < weight_threshold] = self.grey_color
        plt.imshow(image)
        plt.show()


def main():
    explainer = Explainer()
    explainer.explain("data/102.png")


if __name__ == '__main__':
    main()
