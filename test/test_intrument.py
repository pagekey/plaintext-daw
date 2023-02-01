# -*- coding: utf-8 -*-
# @Time    : 2023/2/1 18:55
# @Author  : LTstrange
import numpy as np

from instrument.models import Instrument, Note


class TestInstrument:
    def test_init(self):
        instrument = Instrument()
        assert instrument.name is None
        assert instrument.effects == dict()
        assert instrument.notes == dict()

    def test_read_from_yaml(self):
        instrument = Instrument.read_yaml("instrument/instrument.yml")
        assert instrument.name is not None
        assert len(instrument.notes) != 0

    def test_set_name(self):
        instrument = Instrument()
        instrument.set_name("abc")
        assert instrument.name == "abc"

    def test_set_effect(self):
        effects = {"Note(base)": "sin(base, 5) | fade_in_out(*)"}
        instrument = Instrument()
        instrument.set_effects(effects)

        assert instrument.effects == {"Note": (["base", ], ["sin(base, 5)", "fade_in_out(*)"])}

    def test_set_notes(self):
        instrument = Instrument()
        # need to define effects before defining notes.
        effects = {"Note(base)": "sin(base, 5) | fade_in_out(*)"}
        instrument.set_effects(effects)

        notes = {"C": "Note(65.406)"}
        instrument.set_notes(notes)

        assert instrument.notes == {"C": Note(["65.406"], "Note")}

    def test_render_notes(self):
        instrument = Instrument()
        effects = {"Note(base)": "sin(base, 5) | fade_in_out(*)"}
        instrument.set_effects(effects)

        notes = {"C": "Note(65.406)"}
        instrument.set_notes(notes)

        # need to define effects and notes before rendering
        note_C = instrument.render_note("C", 2)

        assert len(note_C) == 44100 * 2
        assert type(note_C) == np.ndarray
