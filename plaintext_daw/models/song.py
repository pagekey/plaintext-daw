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
        # Aggregate notes into a single list
        # Eventually, this approach will need to be upgraded when patterns have an offset too
        # For now, it works
        all_notes = []
        for pattern in self.patterns:
            for note in pattern.notes:
                all_notes.append(note)
        
        # Figure out how many samples the final render will be
        # end_sample = max([n.get_end_sample(self.sample_rate, self.bpm) for n in all_notes])
        
        # Allocate an np array for the entire song
        song_data = np.zeros(1)
        for note in all_notes:
            # Get the raw audio data for this note
            instrument = self.instruments[pattern.instrument]
            clip_path = instrument.clips[note.value].path
            clip_np, channels, sample_width, sample_rate = wav_to_np(os.path.join(self.path, clip_path))
            # Compute sample start/end
            start = note.get_start_sample(self.sample_rate, self.bpm)
            end = start + len(clip_np)
            # If end is past the song end, pad out the rest of the song with zeros
            num_new_samples = end - len(song_data)
            if num_new_samples > 0:
                song_data = np.pad(song_data, (0, num_new_samples))
            # Put it in the song at the right place
            song_data[start:end] += clip_np

        np_to_wav(song_data, channels, sample_width, sample_rate, out_filename)
