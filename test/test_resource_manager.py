import numpy as np
import pytest

from plaintext_daw.resource_manager import ResourceManager


class TestResourceManager:

    def setup_method(self, test_method):
        self.rm = ResourceManager('.')

    def test_working_dir(self):
        assert self.rm.working_dir == '.'

    def test_get_clip_no_type(self):
        with pytest.raises(ValueError):
            self.rm.get_clip({})
        with pytest.raises(ValueError):
            self.rm.get_clip({'type': 'something crazy'})

    def test_get_clip_wav(self):
        # Good config
        wav_path = 'test/data/song1/piano/Piano-A0.ogg.wav'
        config = {
            'type': 'wav',
            'path': wav_path,
        }
        clip = self.rm.get_clip(config)
        assert isinstance(clip.data, np.ndarray)
        assert clip.channels == 1
        assert clip.sample_width == 2
        assert clip.sample_rate == 44100

        # Missing fields

    def test_get_clip_synth(self):
        # Good config
        config = {
            'type': 'synth',
            'frequency': 16.35,
            'sample_rate': 5000,
            'length': 2,
        }
        clip = self.rm.get_clip(config)
        assert isinstance(clip.data, np.ndarray)
        assert len(clip.data) == 5000 * 2 # sample_rate * length
        assert clip.channels == 1
        assert clip.sample_width == 2
        assert clip.sample_rate == 5000

        # Missing fields
        for missing_field in ['frequency', 'sample_rate', 'length']:
            bad_cfg = config.copy()
            del bad_cfg[missing_field]
            with pytest.raises(ValueError):
                self.rm.get_clip(bad_cfg)


    def test_get_instrument(self):
        pass
