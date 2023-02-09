# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 15:14
# @Author  : LTstrange
from dataclasses import dataclass
from typing import List
import numpy as np

from primitive_wave import PrimitiveWave
from envelope import Envelope


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
