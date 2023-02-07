import os
from plaintext_daw.lib import wav_to_np

from plaintext_daw.models.clip import Clip
from plaintext_daw.models.synth import gen_sine


class ResourceManager:
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def get_clip(self, config):
        # check config here, fail if invalid
        if 'type' not in config:
            raise ValueError('Type is required for clip')
        if config['type'] == 'wav':
            # load the binary data (WAV)
            data, channels, sample_width, sample_rate = wav_to_np(os.path.join(self.working_dir, config['path']))
        elif config['type'] == 'synth':
            for required_field in ['frequency', 'sample_rate', 'length']:
                if required_field not in config:
                    raise ValueError(f'{required_field} is required for Clip')
            data = gen_sine(config['frequency'], 1, config['length'], config['sample_rate'])
            channels = 1
            sample_width = 2
            sample_rate = config['sample_rate']
        else:
            raise ValueError('Invalid clip type:', config['type'])

        clip = Clip(
            data=data,
            channels=channels,
            sample_width=sample_width,
            sample_rate=sample_rate,
        )
        return clip