from enum import Enum
import os
import numpy as np

from plaintext_daw.models.synth import gen_sine

from ..lib import wav_to_np


class ClipType(Enum):
    WAV = 0
    SINE = 1

class Clip:

    def __init__(
        self,
        type: ClipType = None,
        path: str = '',
        start: int = 0,
        frequency: float = 0,
        config_dir: str = '.',
    ):
        self.type = type if type is not None else ClipType.WAV # TODO make all the default like this or else they won't work
        self.path = path
        self.start = start
        self.frequency = frequency
        self.config_dir = config_dir
    
    @staticmethod
    def from_dict(dict, config_dir):
        return Clip(
            type=ClipType[dict['type']] if 'type' in dict else None,
            path=dict['path'] if 'path' in dict else None,
            start=dict['start'] if 'start' in dict else None,
            frequency=dict['frequency'] if 'frequency' in dict else None,
            config_dir=config_dir,
        )

    def to_np(self):
        if self.type == ClipType.WAV:
            wav_path = os.path.join(self.config_dir, self.path)
            return wav_to_np(wav_path)
        elif self.type == ClipType.SINE:
            # TODO actually get these from somewhere
            # need to re-arch
            nchannels = 1
            sample_width = 2
            sample_rate = 44100
            np_out = gen_sine(self.frequency, 5, 1)
            return np_out, nchannels, sample_width, sample_rate
        else:
            raise ValueError('ClipType not yet supported:', str(self.type))
