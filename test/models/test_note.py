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

    def test_beats_to_samples(self):
        beats = 1
        bpm = 60
        sample_rate = 44100
        assert Note.beats_to_samples(beats, bpm, sample_rate) == sample_rate
        assert Note.beats_to_samples(1, 200, 44100) == 147000
        assert Note.beats_to_samples(beats*2, bpm, sample_rate) == sample_rate*2
        assert Note.beats_to_samples(beats, bpm, sample_rate/2) == sample_rate/2

    def test_start_end_sample_simple(self):
        note = Note(value='a', start_beat=0, length=1)
        # regardless of anything else, if it starts on beat 0, it starts on sample 0
        assert note.get_start_sample(60, 44100) == 0
        assert note.get_end_sample(60, 44100) == 44100
        note.start_beat = 1
        note.length = 2
        assert note.get_start_sample(60, 44100) == 44100
        assert note.get_end_sample(60, 44100) == 44100*3
