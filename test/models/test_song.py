from plaintext_daw.models import Instrument, Pattern, Sample, Song


class TestSong:
    def test_init(self):
        song = Song()
        assert isinstance(song, Song)
        assert song.bpm == 100

    def test_from_dict(self):
        song = Song.from_dict({
            'bpm': 120,
            'sample_rate': 48000,
            'samples': [{}],
            'instruments': {'piano': {}},
            'patterns': [{}], 
        })
        assert song.bpm == 120
        assert song.sample_rate == 48000
        assert isinstance(song.samples[0], Sample)
        assert isinstance(song.instruments['piano'], Instrument)
        assert isinstance(song.patterns[0], Pattern)
