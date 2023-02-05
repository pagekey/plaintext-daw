from dataclasses import dataclass
from typing import Dict, List, Tuple
import re

import numpy as np
import yaml


def fade_in_out(note: np.ndarray, in_rate=0.1, out_rate=0.9):
    # This fade_in_out function sound not good.
    # Will be modified soon.
    assert type(note) == np.ndarray
    note_length = len(note)

    fade_in_end = int(note_length * in_rate)
    fade_out_start = int(note_length * out_rate)
    in_rate = np.arange(0, 1, 1 / fade_in_end)
    out_rate = np.arange(1, 0, -1 / (note_length - fade_out_start))

    note[:fade_in_end] *= in_rate
    note[fade_out_start:] *= out_rate

    return note


def gen_sine(base_freq: float, harmonic: int, duration: float, sample_rate: int = 44100):
    # set up basic parameters
    base_freq = float(base_freq)
    harmonic = int(harmonic)
    duration = float(duration)
    sample_rate = int(sample_rate)

    # set up time
    t = np.arange(0, duration, 1 / sample_rate)
    amp_sum = 0  # record amplitude's sum
    note_wave = np.zeros_like(t)  # init np array
    for i in range(0, harmonic):
        # amp:  1 / (2 ** i), i= 0, 1, 2, ...
        # freq: (2 ** i) * base_freq, i= 0, 1, 2, ...
        amp_sum += 1 / (2 ** i)
        note_wave += 1 / (2 ** i) * np.sin(2 ** i * base_freq * 2 * np.pi * t)

    return note_wave / amp_sum


@dataclass
class SynthClip:
    params: List[str]  # parameters this note can provide
    effect: str  # effect name


class Synth:
    def __init__(self):
        self.name: str = None  # synth's name
        self.effects: Dict[
            str, Tuple[List[str], List[str]]] = dict()  # effect_name, list of formal_params, seq of effects
        self.notes: Dict[str, SynthClip] = dict()  # defined notes

    @staticmethod
    def read_yaml(filename: str):
        with open(filename, 'r') as raw_yaml:
            config = yaml.load(raw_yaml, Loader=yaml.SafeLoader)

        config = config['synth']
        synth = Synth()
        synth.set_name(config['name'])
        synth.set_effects(config['effects'] if 'effects' in config else None)
        # load notes
        synth.set_notes(config['notes'])

        return synth

    def set_name(self, name):
        self.name = name

    def set_effects(self, effects):
        if effects is None:  # there can be no addition effects. (Only builtin effects)
            return

        for effect_key, effect_seq in effects.items():  # for each effect in config file
            # separate out the name of effect and needed parameters
            effect_name, param = re.match(r'([a-zA-Z]+)\((.*)\)', effect_key).groups()
            param = [p.strip() for p in param.split(',')]
            # effect definition is a seq of effect, sep by '|'
            effect_seq = [e.strip() for e in effect_seq.split('|')]
            self.effects[effect_name] = (param, effect_seq)

    def set_notes(self, notes: Dict[str, str]):
        for note_key, note_def in notes.items():  # for each key definition
            # separate out the effect's name this note refer, and the value this note give
            effect_name, values = re.match(r'([a-zA-Z]+)\((.*)\)', note_def).groups()
            values = [v.strip() for v in values.split(',')]
            # make sure the effect name is already defined
            assert effect_name in set(self.effects.keys()).union(['sin', "fade_in_out"])
            params, effect_seq = self.effects[effect_name]
            assert len(params) == len(values)  # make sure the actual para and formal param matched there length
            self.notes[note_key] = SynthClip(values, effect_name)

    def render_note(self, note_name: str, duration: float) -> np.ndarray:
        note = self.notes[note_name]  # get note data
        formal_param, effect_seq = self.effects[note.effect]  # get effect data

        name_space = dict(zip(formal_param, note.params))  # set a simple namespace

        result = None
        for effect in effect_seq:  # apply each effect to generate np array
            name, param = re.match(r'([a-zA-Z_]+)\((.*)\)', effect).groups()  # separate out effect's name and params
            param = [p.strip() for p in param.split(',')]
            param = [name_space[p] if p in name_space else p for p in param]  # get param's value
            if name == "sin":  # apply effect
                param.append(duration)
                result = gen_sine(*param)
            elif name == 'fade_in_out':
                assert result is not None
                result = fade_in_out(result)
            else:
                raise "Not defined effect"
        return result
