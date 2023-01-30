from plaintext_daw.models import Sample


class TestSample:
    def test_init(self):
        obj = Sample()
        assert isinstance(obj, Sample)
        assert obj.path == ''

    def test_from_dict(self):
        obj = Sample.from_dict({
            'path': 'mysound.wav',
            'start': 2,
        })
        assert obj.path == 'mysound.wav'
        assert obj.start == 2
