
from plaintext_daw.models import Instrument, Clip
from plaintext_daw.models.instrument import InstrumentSource


class TestInstrument:
    def test_init(self):
        obj = Instrument()
        assert isinstance(obj, Instrument)
        assert obj.source == InstrumentSource.IN_PLACE

    def test_from_dict(self):
        obj = Instrument.from_dict({
            'source': 'LOCAL_FILE',
            'clips': {'a': {}},
        })
        assert obj.source == InstrumentSource.LOCAL_FILE
        assert isinstance(obj.clips['a'], Clip)
