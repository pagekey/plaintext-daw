from enum import Enum
from typing import Dict

from .clip import Clip


class InstrumentSource(Enum):
    IN_PLACE = 1 # in the config, no need to load an external file
    # TODO add support for these eventually
    LOCAL_FILE = 2 # present somewhere on filesystem
    GIT = 3 # can be loaded with Git, either via ssh or https depending on the url

class Instrument:
    
    def __init__(
        self,
        source: InstrumentSource=InstrumentSource.IN_PLACE,
        clips: Dict[str, Clip]={}
    ):
        self.source = source
        self.clips = clips

    @staticmethod
    def from_dict(dict):
        return Instrument(
            source=InstrumentSource[dict['source']] if 'source' in dict else None,
            clips={key: Clip.from_dict(elem) for key, elem in dict['clips'].items()} if 'clips' in dict else None,
        )
