import wave
import numpy as np
import yaml

from models import Sin, Config

sample_rate = 44100  # hz
sample_width = 2  # bytes


def fade_in_out(note, in_rate=0.1, out_rate=0.9):
    note_length = len(note)

    fade_in_end = int(note_length * in_rate)
    fade_out_start = int(note_length * out_rate)
    in_rate = np.arange(0, 1, 1 / fade_in_end)
    out_rate = np.arange(1, 0, -1 / (note_length - fade_out_start))

    note[:fade_in_end] *= in_rate
    note[fade_out_start:] *= out_rate

    return note


def gen_note(note: Sin, d) -> np.ndarray:
    t = np.arange(0, d, 1 / sample_rate)
    A_sum = 0
    note_wave = np.zeros_like(t)
    for i in range(0, note.harmonic):
        A_sum += 1 / (2 ** i)
        note_wave += 1 / (2 ** i) * np.sin(2 ** i * note.base_freq * 2 * np.pi * t)

    return fade_in_out(note_wave / A_sum)


def read_yaml(filename: str) -> Config:
    with open(filename, 'r') as raw_yaml:
        config = yaml.load(raw_yaml, Loader=yaml.SafeLoader)

    instrument = config['instrument']
    config = Config()
    config.set_name(instrument['name'])
    config.set_effects(instrument['effects'])
    # load notes
    config.set_notes(instrument['notes'])

    return config


def save_song(filename: str, song: np.ndarray):
    raw_song = (song * 2 ** 15).astype(np.int16)
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(sample_width)
        f.setframerate(sample_rate)
        f.writeframes(raw_song)
        print(f"Saved in {filename}")


if __name__ == '__main__':
    notes_dict = read_yaml("instrument.yml")
    print(notes_dict)
    exit()

    notes_dict['z'] = Note(0, 0)

    # cooley's reel
    note_arr = [('D', 2),
                ('E', 1), ('B', 1), ('C', .5), ('B', .5), ('A', 1), ('B', 2), ('E', 1), ('B', 1),
                ('B', 2), ('A', 1), ('B', 1), ('d', 1), ('B', 1), ('A', 1), ('G', 1),
                ('F', 1), ('D', 1), ('A', 1), ('D', 1), ('B', 1), ('D', 1), ('A', 1), ('D', 1),
                ('F', 1), ('D', 1), ('A', 1), ('D', 1), ('d', 1), ('A', 1), ('F', 1), ('D', 1),
                ]
    song = np.zeros(sample_rate // 4)
    for n in note_arr:
        song = np.concatenate(
            [song,
             gen_note(notes_dict[n[0]], n[1] / 4)]
        )

    song = np.concatenate([song, np.zeros(sample_rate // 4)])

    save_song("example.wav", song)
