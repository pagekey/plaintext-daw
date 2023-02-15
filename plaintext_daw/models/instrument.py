import os
import subprocess
import sys
import uuid
from enum import Enum
from typing import Dict

import yaml

from .clip import Clip


class InstrumentSource(Enum):
    IN_PLACE = 1 # in the config, no need to load an external file
    LOCAL_FILE = 2 # config file present somewhere on filesystem
    GIT = 3 # can be loaded with Git, either via ssh or https depending on the url

class Instrument:
    
    def __init__(
        self, 
        source=InstrumentSource.IN_PLACE,
        type='wav',
        repo='',
        ref='',
        path='',
    ):
        self.clips: Dict[str, Clip] = {}
        self.source = source
        self.type = type
        self.repo = repo
        self.ref = ref
        self.path = path

    def get_clip(self, note):
        return self.clips[note.value]
