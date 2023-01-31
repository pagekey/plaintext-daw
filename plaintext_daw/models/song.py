import os
from typing import List

import numpy as np

from ..lib import np_to_wav, wav_to_np
from .instrument import Instrument
from .pattern import Pattern
from .clip import Clip


class Song:

    def __init__(
        self,
        path: str = '',
        bpm: int = 100,
        sample_rate: int = 44100,
        clips: List[Clip] = [],
        instruments: List[Instrument] = [],
        patterns: List[Pattern] = [],
    ):
        self.path = path
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.clips = clips
        self.instruments = instruments
        self.patterns = patterns

    @staticmethod
    def from_dict(dict):
        return Song(
            path=dict['path'] if 'path' in dict else None,
            bpm=dict['bpm'] if 'bpm' in dict else None,
            sample_rate=dict['sample_rate'] if 'sample_rate' in dict else None,
            clips=[Clip.from_dict(elem) for elem in dict['clips']] if 'clips' in dict else None,
            instruments={key: Instrument.from_dict(elem) for key, elem in dict['instruments'].items()} if 'instruments' in dict else None,
            patterns=[Pattern.from_dict(elem) for elem in dict['patterns']] if 'patterns' in dict else None,
        )

    def render(self, out_filename: str):
        song_data = np.empty(1)

        for pattern in self.patterns:
            for note in pattern.notes:
                # Open the sample
                instrument = self.instruments[pattern.instrument]
                clip_path = instrument.clips[note.value].path
                clip_np, channels, sample_width, sample_rate = wav_to_np(os.path.join(self.path, clip_path))
                # Put it in the song at the right place
                # Compute start/end based on metadata
                # Extend length of song if not yet long enough
                # Add sample into the song at the right place
                song_data = np.concatenate([song_data, clip_np])

        np_to_wav(song_data, channels, sample_width, sample_rate, out_filename)
