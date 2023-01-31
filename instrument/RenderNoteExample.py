import numpy as np
from models import Note, Instrument
from plaintext_daw.lib import np_to_wav

sample_rate = 44100  # hz
sample_width = 2  # bytes

if __name__ == '__main__':
    instrument = Instrument.read_yaml("instrument.yml")

    # cooley's reel
    note_arr = [('D', 2),
                ('E', 1), ('B', 1), ('C', .5), ('B', .5), ('A', 1), ('B', 2), ('E', 1), ('B', 1),
                ('B', 2), ('A', 1), ('B', 1), ('d', 1), ('B', 1), ('A', 1), ('G', 1),
                ('F', 1), ('D', 1), ('A', 1), ('D', 1), ('B', 1), ('D', 1), ('A', 1), ('D', 1),
                ('F', 1), ('D', 1), ('A', 1), ('D', 1), ('d', 1), ('A', 1), ('F', 1), ('D', 1),
                ]

    # start padding
    song = np.zeros(sample_rate // 4)

    # generate song
    for n in note_arr:
        song = np.concatenate(
            [song,
             instrument.render_note(n[0], n[1] / 4)]
        )

    # end padding
    song = np.concatenate([song, np.zeros(sample_rate // 4)])

    np_to_wav(song, 1, sample_width, sample_rate, "example.wav")
