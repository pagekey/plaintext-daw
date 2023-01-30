from typing import List

from .instrument import Instrument
from .note import Note


class Pattern:
    
    def __init__(
        self,
        name: str = '',
        instrument: Instrument = Instrument(),
        notes: List[Note] = [],
        start: int = 0,
        repeat: int = 0,
    ):
        self.name = name
        self.instrument = instrument
        self.notes = notes
        self.start = start
        self.repeat = repeat

    @staticmethod
    def from_dict(dict):
        return Pattern(
            name=dict['name'] if 'name' in dict else None,
            instrument=Instrument.from_dict(dict['instrument']) if 'instrument' in dict else None,
            notes=[Note.from_dict(elem) for elem in dict['notes']] if 'notes' in dict else None,
            start=dict['start'] if 'start' in dict else None,
            repeat=dict['repeat'] if 'repeat' in dict else None,
        )
