import os
import shutil

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
        }, '.')
        assert obj.source == InstrumentSource.LOCAL_FILE
        assert isinstance(obj.clips['a'], Clip)

    def test_from_git(self):
        if os.path.exists('.ptd_cache'):
            shutil.rmtree('.ptd_cache')
        instrument = Instrument.from_dict({
            'source': 'GIT',
            'name': 'piano',
            'repo': 'git@github.com:pagekeytech/plaintext-daw-instruments',
            'ref': 'master',
            'path': 'piano/instrument.yml',
        }, '.')
        assert instrument.source == InstrumentSource.GIT
        assert instrument.name == 'piano'
        assert instrument.repo == 'git@github.com:pagekeytech/plaintext-daw-instruments'
        assert instrument.path == 'piano/instrument.yml'
        assert instrument.is_loaded() == False
        instrument.load()
        assert instrument.is_loaded() == True
        assert os.path.exists('.ptd_cache')
        assert os.path.exists('.ptd_cache/instruments')
        assert os.path.exists('.ptd_cache/instruments/plaintext-daw-instruments')
        assert os.path.exists('.ptd_cache/instruments/plaintext-daw-instruments/piano/instrument.yml')
        assert os.path.exists('.ptd_cache/instruments/plaintext-daw-instruments/piano/samples/A4.wav')
