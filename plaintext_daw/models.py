from dataclasses import dataclass
from typing import List, Dict


@dataclass
class Note:
    value: str
    length: int

@dataclass
class Sample:
    path: str

@dataclass
class Instrument:
    samples: Dict[str, Sample]

@dataclass
class Pattern:
    name: str
    instrument: Instrument
    notes: List[Note]
    start: int
    repeat: int

@dataclass
class Sample:
    path: str
    start: int

@dataclass
class Song:
    output: str
    bpm: int
    sample_rate: int
    samples: List[Sample]
    instruments: List[Instrument]
    patterns: List[Pattern]
