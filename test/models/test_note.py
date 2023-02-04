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

    def test_start_end_sample_simple(self):
        note = Note(value='a', start_beat=0, length=1)
        # regardless of anything else, if it starts on beat 0, it starts on sample 0
        assert note.get_start_sample(44100, 60) == 0
        assert note.get_end_sample(44100, 60) == 44100

    def test_start_end_sample_complex(self):
        note = Note(value='a', start_beat=0.5, length=2)
        assert note.get_start_sample(44100, 60) == 44100 * 0.5
        assert note.get_end_sample(44100, 60) == 44100*2.5

        assert note.get_start_sample(48000, 60) == 48000*0.5
        assert note.get_end_sample(48000, 60) == 48000*2.5
        note.length = 3
        assert note.get_start_sample(48000, 60) == 48000*0.5
        assert note.get_end_sample(48000, 60) == 48000*3.5
