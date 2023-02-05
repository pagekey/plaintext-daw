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

    def get_start_sample(self, sample_rate, bpm):
        # sample_rate: samples per second
        # bpm: beats per minute
        bps = bpm / 60
        sec_per_beat = 1/bps
        samples_per_beat = sample_rate * sec_per_beat
        return int(samples_per_beat * self.start_beat)

    def get_end_sample(self, sample_rate, bpm):
        bps = bpm / 60
        sec_per_beat = 1/bps
        samples_per_beat = sample_rate * sec_per_beat
        len_sample = samples_per_beat * self.length
        start_sample = self.get_start_sample(sample_rate, bpm)
        return int(start_sample + len_sample)
