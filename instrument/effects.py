# -*- coding: utf-8 -*-
# @Time    : 2023/1/31 15:45
# @Author  : LTstrange


import numpy as np


def fade_in_out(note: np.ndarray, in_rate=0.1, out_rate=0.9):
    assert type(note) == np.ndarray
    note_length = len(note)

    fade_in_end = int(note_length * in_rate)
    fade_out_start = int(note_length * out_rate)
    in_rate = np.arange(0, 1, 1 / fade_in_end)
    out_rate = np.arange(1, 0, -1 / (note_length - fade_out_start))

    note[:fade_in_end] *= in_rate
    note[fade_out_start:] *= out_rate

    return note


def sin(base_freq: float, harmonic: int, duration: float, sample_rate: int = 44100):
    base_freq = float(base_freq)
    harmonic = int(harmonic)
    duration = float(duration)
    sample_rate = int(sample_rate)

    t = np.arange(0, duration, 1 / sample_rate)
    amp_sum = 0
    note_wave = np.zeros_like(t)
    for i in range(0, harmonic):
        amp_sum += 1 / (2 ** i)
        note_wave += 1 / (2 ** i) * np.sin(2 ** i * base_freq * 2 * np.pi * t)

    return note_wave / amp_sum
