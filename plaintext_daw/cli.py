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


def cli_entry_point(args=sys.argv):
    if len(args) == 2:
        if args[1] == "gui":
            exit(gui())
        else:
            file_path = args[1]
            if not os.path.exists(file_path):
                print("Error: %s not found" % file_path, file=sys.stderr)
                sys.exit(1)
            song_dir = os.path.dirname(file_path)
            with open(file_path, 'r') as f:
                raw_yaml = f.read()
            config = yaml.load(raw_yaml, Loader=yaml.SafeLoader)
            song = Song.from_dict(config['song'])
            # Process notes
            song_data = np.empty(1)

            for pattern in song.patterns:
                for note in pattern.notes:
                    # Open the sample
                    instrument = song.instruments[pattern.instrument]
                    sample_path = instrument.samples[note.value]['path']
                    sample_np, channels, sample_width, sample_rate = wav_to_np(os.path.join(song_dir, sample_path))
                    # Put it in the song at the right place
                    # Compute start/end based on metadata
                    # Extend length of song if not yet long enough
                    # Add sample into the song at the right place
                    song_data = np.concatenate([song_data, sample_np])

            np_to_wav(song_data, channels, sample_width, sample_rate, 'song.wav')
    else:
        print_usage()
