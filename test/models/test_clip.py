import numpy as np

from plaintext_daw.models import Clip


class TestClip:
    def test_init(self):
        obj = Clip()
        assert isinstance(obj, Clip)
        assert obj.path == ''

    def test_from_dict(self):
        obj = Clip.from_dict({
            'path': 'mysound.wav',
            'start': 2,
        }, '.')
        assert obj.path == 'mysound.wav'
        assert obj.start == 2

    def test_to_np(self):
        clip = Clip.from_dict({
            'path': 'test/data/piano/Piano-A0.ogg.wav',
            'start': 2,
        }, '.')
        clip_np = clip.to_np()
        assert isinstance(clip_np[0], np.ndarray)
        assert isinstance(clip_np[1], int)
        assert isinstance(clip_np[2], int)
        assert isinstance(clip_np[3], int)
