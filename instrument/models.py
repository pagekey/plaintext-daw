# -*- coding: utf-8 -*-
# @Time    : 2023/1/30 22:49
# @Author  : LTstrange

from dataclasses import dataclass
from typing import Dict, List, Tuple
import re


@dataclass
class Sin:
    base_freq: float
    effect: str = ''
    harmonic: int = 5


class Config:
    name: str
    effects: Dict[str, Tuple[List[str], List[str]]]  # effect_name, list of param, list of (builtin) effect
    notes: Dict[str, Sin]

    def set_name(self, name):
        self.name = name

    def set_effects(self, effects):
        self.effects = dict()
        for effect_key in effects:
            effect_value = effects[effect_key]
            effect_name, param = re.match(r'([a-zA-Z]+)\((.*)\)', effect_key).groups()
            param = [p.strip() for p in param.split(',')]
            effect_value = [e.strip() for e in effect_value.split('|')]
            self.effects[effect_name] = (param, effect_value)

    def set_notes(self, notes: Dict[str, str]) -> Sin:
        for note_key in notes:
            node_def = notes[note_key]
            effect, values = re.match(r'([a-zA-Z]+)\((.*)\)', node_def).groups()
            values = [v.strip() for v in values.split(',')]
            params, effects = self.effects[effect]

            assert len(values) == len(params)
            params = dict(zip(params, values))
            print(params)
            for e in effects:
                if r := re.match(r'([a-zA-Z]+)\((.*)\)', e):
                    func, formal_param = r.groups()
                    formal_param = [params[p.strip()] if p.strip() in params else p for p in formal_param.split(',')]
                    if func == 'sin':
                        Sin(*[float(formal_param[0]), '', int(formal_param[1])])
                else:
                    raise "This isn't a `func`, should not happen."
                exit()

        exit()
