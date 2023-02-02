import os
import numpy as np

from ..lib import wav_to_np


class Clip:

    def __init__(
        self,
        path: str = '',
        start: int = 0,
        config_dir: str = '.',
    ):
        self.path = path
        self.start = start
        self.config_dir = config_dir
    
    @staticmethod
    def from_dict(dict, config_dir):
        return Clip(
            path=dict['path'] if 'path' in dict else None,
            start=dict['start'] if 'start' in dict else None,
            config_dir=config_dir,
        )

    def to_np(self):
        wav_path = os.path.join(self.config_dir, self.path)
        return wav_to_np(wav_path)
