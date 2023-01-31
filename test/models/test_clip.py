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
        })
        assert obj.path == 'mysound.wav'
        assert obj.start == 2
