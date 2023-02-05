class Note:
    
    def __init__(
        self,
        value: str = '',
        start_beat: float = 0,
        length: float = 1,
    ):
        self.value = value
        self.start_beat = start_beat
        self.length = length

    @staticmethod
    def from_dict(dict):
        return Note(
            value=dict['value'] if 'value' in dict else None,
            start_beat=dict['start_beat'] if 'start_beat' in dict else None,
            length=dict['length'] if 'length' in dict else None,
        )

    @staticmethod
    def beats_to_samples(beats, bpm, sample_rate):
        return int(beats*(bpm/60)*sample_rate)

    def get_start_sample(self, bpm, sample_rate):
        return Note.beats_to_samples(self.start_beat, bpm, sample_rate)

    def get_end_sample(self, bpm, sample_rate):
        beat = self.start_beat + self.length
        return Note.beats_to_samples(beat, bpm, sample_rate)
