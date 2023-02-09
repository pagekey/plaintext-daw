# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 15:14
# @Author  : LTstrange
from dataclasses import dataclass
from typing import List
import numpy as np

from primitive_wave import PrimitiveWave


class Wave:
    def __init__(self, primitive_waves: List[PrimitiveWave]):
        self.primitive_waves = primitive_waves

    def render(self, duration: float, sample_length: int):
        wave = np.zeros(sample_length)
        for primitive in self.primitive_waves:
            wave += primitive.render(duration, sample_length)

        return wave


class Range:
    def __init__(self, duration: float):
        """
        duration: time in ms
        """
        self.duration = duration  # time in second


class Envelope:
    def __call__(self, wave: Wave, time_range: Range, sample_rate: float):
        raise NotImplementedError


class ADSR(Envelope):
    def __init__(self, attack: float, decay: float, sustain_level: float, release: float):
        """
        fade in/out envelope
        :param attack: The time for the amplitude to increase from 0 to 1.
        :param decay: The time for the amplitude to decrease from 1 to sustain.
        :param sustain_level: A fraction of the maximum amplitude (0 to 1).
        :param release: The time for the amplitude to decrease from sustain to 0.
        """
        self.attack = attack  # second
        self.decay = decay  # second
        self.sustain_level = sustain_level  # fraction
        self.release = release  # second

    def __call__(self, wave: Wave, time_range: Range, sample_rate: int):
        # Calculate the length of each stage in samples
        attack_samples = int(self.attack * sample_rate)
        decay_samples = int(self.decay * sample_rate)
        sustain = time_range.duration - self.attack - self.decay - self.release
        sustain_samples = int(sustain * sample_rate) if sustain > 0 else 0
        release_samples = int(self.release * sample_rate)

        sample_length = attack_samples + decay_samples + sustain_samples + release_samples

        # Initialize the envelope
        envelope = np.zeros(sample_length)

        # Attack stage
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        # Decay stage
        envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, self.sustain_level, decay_samples)

        # Sustain stage
        envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = self.sustain_level

        # Release stage
        envelope[-release_samples:] = np.linspace(self.sustain_level, 0, release_samples)

        wave_samples = wave.render(time_range.duration, sample_length)

        return wave_samples * envelope


class Clip:
    def __init__(self, source: Wave, envelope: Envelope, sample_rate, time_range: Range = None):
        self.source = source
        self.envelope = envelope
        self.sample_rate = sample_rate
        self.time_range = time_range

    def set_time_range(self, time_range: Range):
        self.time_range = time_range

    def render(self, sample_rate: float):
        if self.time_range is None:
            raise "No Time Range defined. use `Clip.set_time_range()`"
        return self.envelope(self.source, self.time_range, sample_rate)


@dataclass
class RawClip:
    data: np.ndarray
