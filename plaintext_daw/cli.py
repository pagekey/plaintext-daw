import os
import sys
import wave

import numpy as np
import yaml

from .gui import gui
from .lib import np_to_wav, wav_to_np
from .models import Instrument, Note, Pattern, Sample, Song


def print_usage():
    print("Usage:")
    print("  plaintext-daw <FILE>: render project file to wav")
    print("  plaintext-daw gui:    open a GUI")


def cli_entry_point():
    if len(sys.argv) == 2:
        if sys.argv[1] == "gui":
            exit(gui())
        else:
            file_path = sys.argv[1]
            if not os.path.exists(file_path):
                print("Error: %s not found" % file_path, file=sys.stderr)
                sys.exit(1)
            song_dir = os.path.dirname(file_path)
            with open(file_path, 'r') as f:
                raw_yaml = f.read()
            config = yaml.load(raw_yaml, Loader=yaml.SafeLoader)
            song = Song(**config['song'])
            # Hydrate
            song.samples = [Sample(**x) for x in song.samples]
            song.instruments = {key: Instrument(**value) for key, value in song.instruments.items()}
            song.patterns = [Pattern(**x) for x in song.patterns]
            for pattern in song.patterns:
                pattern.instrument = song.instruments[pattern.instrument]
                pattern.notes = [Note(**x) for x in pattern.notes]
            # Process notes
            song_data = np.empty(1)

            for pattern in song.patterns:
                for note in pattern.notes:
                    # Open the sample
                    sample_path = pattern.instrument.samples[note.value]['path']
                    sample_np, channels, sample_width, sample_rate = wav_to_np(os.path.join(song_dir, sample_path))
                    # Put it in the song at the right place
                    # Compute start/end based on metadata
                    # Extend length of song if not yet long enough
                    # Add sample into the song at the right place
                    song_data = np.concatenate([song_data, sample_np])

            np_to_wav(song_data, channels, sample_width, sample_rate, 'song.wav')
    else:
        print_usage()
