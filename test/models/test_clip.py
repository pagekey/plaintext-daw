import numpy as np

from plaintext_daw.models import Clip


class TestClip:
    def test_init(self):
        obj = Clip('hi', 1, 2, 3)
        assert isinstance(obj, Clip)
        assert obj.data == 'hi'
        assert obj.channels == 1
        assert obj.sample_width == 2
        assert obj.sample_rate == 3
