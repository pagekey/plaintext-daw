class Clip:

    def __init__(
        self,
        path: str = '',
        start: int = 0,
    ):
        self.path = path
        self.start = start
    
    @staticmethod
    def from_dict(dict):
        return Clip(
            path=dict['path'] if 'path' in dict else None,
            start=dict['start'] if 'start' in dict else None,
        )
