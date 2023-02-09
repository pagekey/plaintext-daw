# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 16:09
# @Author  : LTstrange

from dataclasses import dataclass
import numpy as np
from enum import Enum
from typing import List


class WaveType(Enum):
    sine = 1


@dataclass
class PrimitiveWave:
    wave_type: WaveType

    def render(self, duration: float, sample_length: int) -> np.ndarray:
        raise NotImplementedError


class Wave:
    def __init__(self, primitive_waves: List[PrimitiveWave]):
        self.primitive_waves = primitive_waves

    def render(self, duration: float, sample_length: int):
        wave = np.zeros(sample_length)
        for primitive in self.primitive_waves:
            wave += primitive.render(duration, sample_length)

        return wave


@dataclass
class Sine(PrimitiveWave):
    wave_type = WaveType.sine
    base_freq: float

    def render(self, duration: float, sample_length: int):
        t = np.linspace(0, duration, sample_length)
        return np.sin(2 * np.pi * self.base_freq * t)
