import os
import sys

import yaml

from plaintext_daw.models import Song


def print_usage():
    print("Usage:")
    print("  plaintext-daw <FILE>: render project file to wav")

def cli_entry_point():
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            print("Error: %s not found" % file_path, file=sys.stderr)
            sys.exit(1)
        with open(file_path, 'r') as f:
            raw_yaml = f.read()
        config = yaml.load(raw_yaml, Loader=yaml.SafeLoader)
        song = Song(**config['song'])
        print(song)
    else:
        print_usage()
