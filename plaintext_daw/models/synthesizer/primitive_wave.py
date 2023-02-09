# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 16:09
# @Author  : LTstrange
import math
from dataclasses import dataclass
from enum import Enum


class WaveType(Enum):
    sine = 1


@dataclass
class PrimitiveWave:
    wave_type: WaveType


class Sine(PrimitiveWave):
    wave_type = WaveType.sine
    base_freq: float
