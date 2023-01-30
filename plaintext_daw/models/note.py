class Note:
    
    def __init__(
        self,
        value: str = '',
        length: int = 1,
    ):
        self.value = value
        self.length = length

    @staticmethod
    def from_dict(dict):
        return Note(
            value=dict['value'] if 'value' in dict else None,
            length=dict['length'] if 'length' in dict else None,
        )
