from typing import List

from .instrument import Instrument
from .pattern import Pattern
from .sample import Sample


class Song:

    def __init__(
        self, 
        output: str = '',
        bpm: int = 100,
        sample_rate: int = 44100,
        samples: List[Sample] = [],
        instruments: List[Instrument] = [],
        patterns: List[Pattern] = [],
    ):
        self.output = output
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.samples = samples
        self.instruments = instruments
        self.patterns = patterns

    @staticmethod
    def from_dict(dict):
        return Song(
            output=dict['output'] if 'output' in dict else None,
            bpm=dict['bpm'] if 'bpm' in dict else None,
            sample_rate=dict['sample_rate'] if 'sample_rate' in dict else None,
            samples=[Sample.from_dict(elem) for elem in dict['samples']] if 'samples' in dict else None,
            instruments={key: Instrument.from_dict(elem) for key, elem in dict['instruments'].items()} if 'instruments' in dict else None,
            patterns=[Pattern.from_dict(elem) for elem in dict['patterns']] if 'patterns' in dict else None,
        )
