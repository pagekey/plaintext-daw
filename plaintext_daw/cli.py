import os
import sys

import yaml

from plaintext_daw.models import Instrument, Note, Pattern, Sample, Song
from plaintext_daw.gui import gui


def print_usage():
    print("Usage:")
    print("  plaintext-daw <FILE>: render project file to wav")
    print("  plaintext-daw gui:    open a GUI")


def cli_entry_point():
    if len(sys.argv) == 2:
        if sys.argv[1] == "gui":
            exit(gui())

        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print("Error: %s not found" % file_path, file=sys.stderr)
            sys.exit(1)
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
        for pattern in song.patterns:
            for note in pattern.notes:
                print(note)
    else:
        print_usage()
