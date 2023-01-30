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
