# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 22:49
# @Author  : LTstrange

from dataclasses import dataclass
from typing import Dict, List, Tuple
import re
import yaml
from effects import sin, fade_in_out


@dataclass
class Note:
    params: List[str]  # parameters this note can provide
    effect: str  # effect name


class Instrument:
    name: str  # instrument's name
    effects: Dict[str, Tuple[List[str], List[str]]]  # effect_name, list of formal_params, seq of effects
    notes: Dict[str, Note]  # defined notes

    @staticmethod
    def read_yaml(filename: str):
        with open(filename, 'r') as raw_yaml:
            config = yaml.load(raw_yaml, Loader=yaml.SafeLoader)

        config = config['instrument']
        instrument = Instrument()
        instrument.set_name(config['name'])
        instrument.set_effects(config['effects'])
        # load notes
        instrument.set_notes(config['notes'])

        return instrument

    def set_name(self, name):
        self.name = name

    def set_effects(self, effects):
        self.effects = dict()
        for effect_key, effect_seq in effects.items():  # for each effect in config file
            # separate out the name of effect and needed parameters
            effect_name, param = re.match(r'([a-zA-Z]+)\((.*)\)', effect_key).groups()
            param = [p.strip() for p in param.split(',')]
            # effect definition is a seq of effect, sep by '|'
            effect_seq = [e.strip() for e in effect_seq.split('|')]
            self.effects[effect_name] = (param, effect_seq)

    def set_notes(self, notes: Dict[str, str]) -> Note:
        self.notes = dict()
        for note_key, note_def in notes.items():
            effect_name, values = re.match(r'([a-zA-Z]+)\((.*)\)', note_def).groups()
            values = [v.strip() for v in values.split(',')]
            assert effect_name in self.effects
            params, effect_seq = self.effects[effect_name]
            assert len(params) == len(values)
            self.notes[note_key] = Note(values, effect_name)

    def render_note(self, note_name: str, duration: float):
        note = self.notes[note_name]
        formal_param, effect_seq = self.effects[note.effect]

        name_space = dict(zip(formal_param, note.params))

        result = None
        for effect in effect_seq:
            name, param = re.match(r'([a-zA-Z_]+)\((.*)\)', effect).groups()
            param = [p.strip() for p in param.split(',')]
            param = [name_space[p] if p in name_space else p for p in param]
            if name == "sin":
                param.append(duration)
                result = sin(*param)
            elif name == 'fade_in_out':
                assert result is not None
                result = fade_in_out(result)
            else:
                raise
        return result
