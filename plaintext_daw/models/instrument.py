import os
import subprocess
import uuid
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
        name: str = str(uuid.uuid4()),
        repo: str = '',
        ref: str = '',
        path: str = '',
        source: InstrumentSource=InstrumentSource.IN_PLACE,
        clips: Dict[str, Clip]={},
    ):
        self.name = name
        self.repo = repo
        self.ref = ref
        self.path = path
        self.source = source
        self.clips = clips

    @staticmethod
    def from_dict(dict):
        return Instrument(
            name=dict['name'] if 'name' in dict else None,
            repo=dict['repo'] if 'repo' in dict else None,
            ref=dict['ref'] if 'ref' in dict else None,
            path=dict['path'] if 'path' in dict else None,
            source=InstrumentSource[dict['source']] if 'source' in dict else None,
            clips={key: Clip.from_dict(elem) for key, elem in dict['clips'].items()} if 'clips' in dict else None,
        )

    def get_repo_name(self):
        return self.repo.split('/')[-1].replace('.git', '')

    def is_loaded(self):
        if self.source == InstrumentSource.IN_PLACE:
            return True # nothing to do
        elif self.source == InstrumentSource.GIT:
            return os.path.exists(f'.ptd_cache/instruments/{self.get_repo_name()}')
        else:
            return False

    def load(self):
        if self.source == InstrumentSource.IN_PLACE:
            pass # nothing to do
        elif self.source == InstrumentSource.GIT:
            # Clone the git repo locally
            # Create cache dir relative to project file if not exists
            os.makedirs('.ptd_cache/instruments', exist_ok=True)
            orig_pwd = os.getcwd()
            os.chdir('.ptd_cache/instruments')
            repo_name = self.get_repo_name()
            if not os.path.exists(repo_name):
                subprocess.check_call(f'git clone {self.repo}'.split())
            os.chdir(repo_name)
            if self.ref is not None and len(self.ref) > 0:
                subprocess.check_call(f'git checkout {self.ref}'.split())
            os.chdir(orig_pwd)
        else:
            raise ValueError('Load instrument source not yet supported:', str(self.source))
