from enum import Enum
from typing import Dict

from .sample import Sample


class InstrumentSource(Enum):
    IN_PLACE = 1 # in the config, no need to load an external file
    # TODO add support for these eventually
    LOCAL_FILE = 2 # present somewhere on filesystem
    GIT = 3 # can be loaded with Git, either via ssh or https depending on the url

class Instrument:
    
    def __init__(
        self,
        source: InstrumentSource=InstrumentSource.IN_PLACE,
        samples: Dict[str, Sample]={}
    ):
        self.source = source
        self.samples = samples

    @staticmethod
    def from_dict(dict):
        return Instrument(
            source=InstrumentSource[dict['source']] if 'source' in dict else None,
            samples=[Sample.from_dict(elem) for elem in dict['samples']] if 'samples' in dict else None,
        )
