from plaintext_daw.models import Instrument, Note, Pattern
from plaintext_daw.models.instrument import InstrumentSource


class TestPattern:
    def test_init(self):
        obj = Pattern()
        assert isinstance(obj, Pattern)
        assert obj.name == ''

    def test_from_dict(self):
        obj = Pattern.from_dict({
            'name': 'pattern1',
            'instrument': {'source': 'LOCAL_FILE'},
            'notes': [{}],
            'start': 5,
            'repeat': 2,
        })
        assert obj.name == 'pattern1'
        assert isinstance(obj.instrument, Instrument)
        assert obj.instrument.source == InstrumentSource.LOCAL_FILE
        assert isinstance(obj.notes[0], Note)
        assert obj.start == 5
        assert obj.repeat == 2
