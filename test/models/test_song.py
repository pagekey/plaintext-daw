from plaintext_daw.models.song import Instrument, Pattern, Sample, Song


class TestSong:
    def test_init(self):
        song = Song()
        assert isinstance(song, Song)
        assert song.output == ''

    def test_from_dict(self):
        song = Song.from_dict({
            'output': 'hello.wav',
            'bpm': 120,
            'sample_rate': 48000,
            'samples': [{}],
            'instruments': [{}],
            'patterns': [{}], 
        })
        assert song.output == 'hello.wav'
        assert song.bpm == 120
        assert song.sample_rate == 48000
        assert isinstance(song.samples[0], Sample)
        assert isinstance(song.instruments[0], Instrument)
        assert isinstance(song.patterns[0], Pattern)
