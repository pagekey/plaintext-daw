import numpy as np

from plaintext_daw.resource_manager import ResourceManager


class TestResourceManager:

    def test_get_clip_wav(self):
        rm = ResourceManager('.')
        assert rm.working_dir == '.'
        wav_path = 'test/data/song1/piano/Piano-A0.ogg.wav'
        config = {
            'type': 'WAV',
            'path': wav_path,
            'start': 0,
        }
        clip = rm.get_clip(config)
        assert clip.path == wav_path
        assert clip.start == 0
        assert isinstance(clip.data, np.ndarray)
        assert clip.channels == 1
        assert clip.sample_width == 2
        assert clip.sample_rate == 44100

    def test_get_instrument(self):
        pass
