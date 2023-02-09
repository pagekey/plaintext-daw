# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 15:14
# @Author  : LTstrange
from dataclasses import dataclass
from enum import Enum
from typing import List


class WaveType(Enum):
    sine = 1


class PrimitiveWave:
    wave_type: WaveType


@dataclass
class Wave:
    primitive_waves: List[PrimitiveWave]


@dataclass
class Range:
    length: float  # ms


class Envelope:
    ...


@dataclass
class Clip:
    wave: Wave
    envelope: Envelope


@dataclass
class RawClip:
    ...
