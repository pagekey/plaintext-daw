import os
from plaintext_daw.lib import wav_to_np

from plaintext_daw.models.clip import Clip


class ResourceManager:
    def __init__(self, working_dir):
        self.working_dir = working_dir

    def get_clip(self, config):
        # check config here, fail if invalid

        # load the binary data (WAV)
        data, channels, sample_width, sample_rate = wav_to_np(os.path.join(self.working_dir, config['path']))

        clip = Clip(
            path=config['path'],
            start=config['start'],
            data=data,
            channels=channels,
            sample_width=sample_width,
            sample_rate=sample_rate,
        )
        return clip
