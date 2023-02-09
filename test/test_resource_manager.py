from unittest.mock import call, patch
import numpy as np
import pytest

from plaintext_daw.resource_manager import ResourceManager


class TestResourceManager:

    def setup_method(self, test_method):
        self.rm = ResourceManager('.')

    def test_working_dir(self):
        assert self.rm.working_dir == '.'

    def test_check_types(self):
        config = {
            'foo': 'val1',
            'bar': 'val2',
        }
        ResourceManager.check_types(config, ['foo', 'bar'])
        with pytest.raises(ValueError, match='baz'):
            ResourceManager.check_types(config, ['foo', 'bar', 'baz'])

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

    @patch.object(ResourceManager, 'get_instrument')
    @patch.object(ResourceManager, 'get_pattern')
    @patch.object(ResourceManager, 'get_sample')
    def test_get_song(self, mock_get_sample, mock_get_pattern, mock_get_instrument):
        with pytest.raises(ValueError):
            self.rm.get_song({'bpm': 100})
        
        ins_dict = {
            'myins': {'field': 'hello'},
            'yourins': {'name': 'insurance??'},
        }
        pattern_dict = {
            'pattern': {'hey': 'there'},
            'other': {'angle': 'momentum'},
        }
        clip_dict = {
            'costco': {'pancake': 'wait'},
            'walmart': {'no': 'free samples'},
        }
        song = self.rm.get_song({
            'bpm': 100,
            'sample_rate': 44100,
            'instruments': ins_dict,
            'patterns': pattern_dict,
            'clips': clip_dict,
        })
        assert song.bpm == 100
        assert song.sample_rate == 44100
        mock_get_instrument.assert_has_calls([
            call(ins_dict['myins']),
            call(ins_dict['yourins']),
        ])
        mock_get_pattern.assert_has_calls([
            call(pattern_dict['pattern']),
            call(pattern_dict['other']),
        ])
        mock_get_sample.assert_has_calls([
            call(clip_dict['costco']),
            call(clip_dict['walmart']),
        ])

    def test_get_instrument(self):
        pass
