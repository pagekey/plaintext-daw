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
    
    def __init__(self):
        self.clips: Dict[str, Clip] = {},

    def get_repo_name(self):
        return self.repo.split('/')[-1].replace('.git', '')

    def get_clip(self, note):
        if not self.is_loaded():
            self.load()
        if note in self.clips:
            return self.clips[note]
        else:
            print(f'Warning: no note {note} for instrument {self.name}', file=sys.stderr)
            return None

    def is_loaded(self):
        if self.source == InstrumentSource.IN_PLACE:
            return True # nothing to do
        elif self.source == InstrumentSource.GIT:
            return self.clips is not None and os.path.exists(f'.ptd_cache/instruments/{self.get_repo_name()}')
        else:
            return False

    def load(self):
        if self.source is None:
            pass
        elif self.source == InstrumentSource.IN_PLACE:
            pass # nothing to do
        elif self.source == InstrumentSource.LOCAL_FILE:
            # TODO eventually copy into cache and throw err if clip not present
            # For now do nothing, assume all clips in instrument are present
            pass
        elif self.source == InstrumentSource.GIT:
            # Clone the git repo locally
            # Create cache dir relative to project file if not exists
            os.makedirs('.ptd_cache/instruments', exist_ok=True)
            orig_pwd = os.getcwd()
            os.chdir('.ptd_cache/instruments')
            # Clone the project nad checkout the right branch
            repo_name = self.get_repo_name()
            if not os.path.exists(repo_name):
                subprocess.check_call(f'git clone {self.repo}'.split())
            os.chdir(repo_name)
            if self.ref is not None and len(self.ref) > 0:
                subprocess.check_call(f'git checkout {self.ref}'.split())
            # Load the config
            with open(self.path, 'r') as f:
                config_dict = yaml.safe_load(f)
            os.chdir(orig_pwd)
            # Load clips from config
            self.clips = {key: Clip.from_dict(elem, f'.ptd_cache/instruments/{repo_name}/{os.path.dirname(self.path)}') for key, elem in config_dict['clips'].items()}
        else:
            raise ValueError('Unsupported instrument source:', str(self.source))
