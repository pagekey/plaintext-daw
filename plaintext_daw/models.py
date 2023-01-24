from dataclasses import dataclass
from typing import List


@dataclass
class Note:
    type: str
    value: str
    length: int

@dataclass
class Instrument:
    type: str

@dataclass
class Pattern:
    type: str
    instrument: Instrument
    notes: List[Note]

@dataclass
class Sample:
    type: str
    path: str
    start: int

@dataclass
class Song:
    type: str
    output: str
    bpm: int
    sample_rate: int
    samples: List[Sample]
    patterns: List[Pattern]
