# -*- coding: utf-8 -*-
# @Time    : 2023/2/9 15:14
# @Author  : LTstrange
from dataclasses import dataclass
from typing import List


from primitive_wave import PrimitiveWave


class Wave:
    def __init__(self, primitive_waves: List[PrimitiveWave]):
        self.primitive_waves = primitive_waves


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
