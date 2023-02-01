# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 22:49
# @Author  : LTstrange

from dataclasses import dataclass
from typing import Dict, List, Tuple
import re

import numpy as np
import yaml
from .effects import sin, fade_in_out


@dataclass
class Note:
    params: List[str]  # parameters this note can provide
    effect: str  # effect name


class Instrument:
    def __init__(self):
        self.name: str = None  # instrument's name
        self.effects: Dict[
            str, Tuple[List[str], List[str]]] = dict()  # effect_name, list of formal_params, seq of effects
        self.notes: Dict[str, Note] = dict()  # defined notes

    @staticmethod
    def read_yaml(filename: str):
        with open(filename, 'r') as raw_yaml:
            config = yaml.load(raw_yaml, Loader=yaml.SafeLoader)

        config = config['instrument']
        instrument = Instrument()
        instrument.set_name(config['name'])
        instrument.set_effects(config['effects'] if 'effects' in config else None)
        # load notes
        instrument.set_notes(config['notes'])

        return instrument

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
            self.notes[note_key] = Note(values, effect_name)

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
                result = sin(*param)
            elif name == 'fade_in_out':
                assert result is not None
                result = fade_in_out(result)
            else:
                raise "Not defined effect"
        return result
