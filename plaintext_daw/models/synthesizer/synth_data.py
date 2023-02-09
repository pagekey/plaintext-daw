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


class Range:
    def __init__(self, duration: float):
        """
        duration: time in ms
        """
        self.duration = duration  # time in ms


class Envelope:
    def __call__(self, wave: Wave, time_range: Range):
        raise NotImplementedError




class Clip:
    def __init__(self, source: Wave, envelope: Envelope, sample_rate, time_range: Range = None):
        self.source = source
        self.envelope = envelope
        self.sample_rate = sample_rate
        self.time_range = time_range


@dataclass
class RawClip:
    data: np.ndarray
