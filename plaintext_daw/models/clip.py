import numpy as np


class Clip:

    def __init__(
        self,
        data: np.ndarray,
        channels: int,
        sample_width: int,
        sample_rate: int,
    ):
        self.type = type
        self.data = data
        self.channels = channels
        self.sample_width = sample_width
        self.sample_rate = sample_rate
