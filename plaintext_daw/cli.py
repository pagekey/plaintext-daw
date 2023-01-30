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
            # Load config
            song_dir = os.path.dirname(file_path)
            with open(file_path, 'r') as f:
                raw_yaml = f.read()
            config = yaml.load(raw_yaml, Loader=yaml.SafeLoader)
            config['song']['path'] = song_dir # not the best design move, but works for now
            song = Song.from_dict(config['song'])
            # Render song to file
            song.render('song.wav')
    else:
        print_usage()
