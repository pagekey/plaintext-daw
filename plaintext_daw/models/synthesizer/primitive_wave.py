# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 16:09
# @Author  : LTstrange
import math
from dataclasses import dataclass
from enum import Enum

import numpy as np


class WaveType(Enum):
    sine = 1


@dataclass
class PrimitiveWave:
    wave_type: WaveType

    def render(self, duration: float, sample_length: int) -> np.ndarray:
        raise NotImplementedError


@dataclass
class Sine(PrimitiveWave):
    wave_type = WaveType.sine
    base_freq: float

    def render(self, duration: float, sample_length: int):
        t = np.linspace(0, duration, sample_length)
        return np.sin(2 * np.pi * self.base_freq * t)
