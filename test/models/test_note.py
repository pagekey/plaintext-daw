from plaintext_daw.models import Note


class TestNote:
    def test_init(self):
        obj = Note()
        assert isinstance(obj, Note)
        assert obj.length == 1

    def test_from_dict(self):
        obj = Note.from_dict({
            'value': 'a',
            'start_beat': 5,
            'length': 0.5,
        })
        assert obj.value == 'a'
        assert obj.start_beat == 5
        assert obj.length == 0.5