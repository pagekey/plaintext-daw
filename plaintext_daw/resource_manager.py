import os
from plaintext_daw.lib import wav_to_np

from plaintext_daw.models.clip import Clip
from plaintext_daw.models.instrument import Instrument, InstrumentSource
from plaintext_daw.models.note import Note
from plaintext_daw.models.pattern import Pattern
from plaintext_daw.models.song import Song
from plaintext_daw.models.synth import gen_sine


class ResourceManager:
    def __init__(self, working_dir, cache_dir='.ptd-cache'):
        self.working_dir = working_dir
        self.cache_dir = cache_dir

    @staticmethod
    def check_types(config, types):
        for type in types:
            if type not in config:
                raise ValueError(f'Required field {type} not found in config')

    def get_song(self, config):
        self.check_types(config, ['bpm', 'sample_rate', 'clips', 'instruments', 'patterns'])
        song = Song(config['bpm'], config['sample_rate'])
        for key, value in config['clips'].items():
            song.clips[key] = self.get_clip(value)
        for key, value in config['instruments'].items():
            song.instruments[key] = self.get_instrument(value)
        for key, value in config['patterns'].items():
            song.patterns[key] = self.get_pattern(value)
        return song

    def get_clip(self, config):
        # check config here, fail if invalid
        self.check_types(config, ['type'])
        if config['type'] == 'wav':
            # load the binary data (WAV)
            self.check_types(config, ['path'])
            data, channels, sample_width, sample_rate = wav_to_np(os.path.join(self.working_dir, config['path']))
        elif config['type'] == 'synth':
            self.check_types(config, ['frequency', 'sample_rate', 'length'])
            data = gen_sine(config['frequency'], 1, config['length'], config['sample_rate'])
            channels = 1
            sample_width = 2
            sample_rate = config['sample_rate']
        else:
            raise ValueError('Invalid clip type:', config['type'])

        clip = Clip(
            data=data,
            channels=channels,
            sample_width=sample_width,
            sample_rate=sample_rate,
        )
        return clip

    def get_instrument(self, config):
        if 'source' in config and config['source'] == 'GIT':
            self.check_types(config, ['source', 'repo', 'ref', 'path'])
            self.clone_repo(config['repo'], config['ref'])
            repo_name = os.path.basename(config['repo']).replace('.git', '')
            config_from_file = self.get_config_from_file(os.path.join(self.cache_dir, repo_name, config['path']))
            instrument = Instrument(
                source=InstrumentSource.GIT,
                repo=config['repo'],
                ref=config['ref'],
                path=config['path'],
            )
            return instrument
        else:
            self.check_types(config, ['clips'])
            instrument = Instrument()
            for key, value in config['clips'].items():
                instrument.clips[key] = self.get_clip(value)
            return instrument

    def get_pattern(self, config):
        self.check_types(config, ['instrument', 'start', 'repeat'])
        pattern = Pattern(config['instrument'], config['start'], config['repeat'])
        for note_dict in config['notes']:
            pattern.notes.append(self.get_note(note_dict))
        return pattern

    def get_note(self, config):
        self.check_types(config, ['value', 'start', 'length'])
        note = Note(config['value'], config['start'], config['length'])
        return note

    def clone_repo(self):
        pass

    def get_config_from_file(self):
        pass
