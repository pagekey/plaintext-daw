import numpy as np
import pytest

from plaintext_daw.models.synth import Synth, SynthClip


class TestSynth:
    def test_init(self):
        instrument = Synth()
        assert instrument.name is None
        assert instrument.effects == dict()
        assert instrument.notes == dict()

    @pytest.mark.skip()
    def test_read_from_yaml(self):
        instrument = Synth.read_yaml("test/data/synth.yml")
        assert instrument.name is not None
        assert len(instrument.notes) != 0

    def test_set_name(self):
        instrument = Synth()
        instrument.set_name("abc")
        assert instrument.name == "abc"

    def test_set_effect(self):
        effects = {"Note(base)": "sin(base, 5) | fade_in_out(*)"}
        instrument = Synth()
        instrument.set_effects(effects)

        assert instrument.effects == {"Note": (["base", ], ["sin(base, 5)", "fade_in_out(*)"])}

    def test_set_notes(self):
        instrument = Synth()
        # need to define effects before defining notes.
        effects = {"Note(base)": "sin(base, 5) | fade_in_out(*)"}
        instrument.set_effects(effects)

        notes = {"C": "Note(65.406)"}
        instrument.set_notes(notes)

        assert instrument.notes == {"C": SynthClip(["65.406"], "Note")}

    def test_render_notes(self):
        instrument = Synth()
        effects = {"Note(base)": "sin(base, 5) | fade_in_out(*)"}
        instrument.set_effects(effects)

        notes = {"C": "Note(65.406)"}
        instrument.set_notes(notes)

        # need to define effects and notes before rendering
        note_C = instrument.render_note("C", 2)

        assert len(note_C) == 44100 * 2
        assert type(note_C) == np.ndarray
