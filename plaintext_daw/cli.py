import os
import sys
import wave

import numpy as np
import yaml

from plaintext_daw.models import Instrument, Note, Pattern, Sample, Song


def print_usage():
    print("Usage:")
    print("  plaintext-daw <FILE>: render project file to wav")

def cli_entry_point():
    if len(sys.argv) == 2:
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
        for pattern in song.patterns:
            for note in pattern.notes:
                # Open the sample
                sample_path = pattern.instrument.samples[note.value]['path']
                f = wave.open(os.path.join(song_dir, sample_path))
                # Read metadata
                samples = f.getnframes()
                data = f.readframes(samples)
                channels = f.getnchannels()
                sample_width = f.getsampwidth()
                sample_rate = f.getframerate()
                f.close()
                # Convert to normalized np array
                audio_int16 = np.frombuffer(data, dtype=np.int16)
                audio_float32 = audio_int16.astype(np.float32)
                max_int16 = 2**15
                audio_normalized = audio_float32 / max_int16
                print(audio_normalized)
                # Convert back to raw audio
                audio_raw = audio_normalized * max_int16
                audio_raw_int16 = audio_raw.astype(np.int16)
                # Write to file
                os.makedirs('out', exist_ok=True)
                f_out = wave.open(os.path.join('out',sample_path.split('/')[-1]), 'wb')
                f_out.setnchannels(channels)
                f_out.setsampwidth(sample_width)
                f_out.setframerate(sample_rate)
                f_out.writeframes(audio_raw_int16)
    else:
        print_usage()
