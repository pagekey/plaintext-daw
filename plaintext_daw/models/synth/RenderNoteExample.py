import numpy as np

from plaintext_daw.models.synth.models import Note, Synth
from plaintext_daw.lib import np_to_wav


sample_rate = 44100  # hz
sample_width = 2  # bytes

if __name__ == '__main__':
    instrument = Synth.read_yaml("instrument.yml")

    # Spring Festival overture
    note_arr = [('z', 1), ('e', 1), ('e', .5), ('d', .5),
                ('c', 1), ('z', 1), ('e', 1), ('e', .5), ('d', .5),
                ('c', 1), ('z', 1), ('e', 1), ('e', .5), ('d', .5),
                ('c', 1), ('G', 1), ('E', 1), ('A', 1),
                ('G', 1.5), ('A', .5), ('G', 1), ('A', 1),
                ('G', 1.5), ('A', .5), ('G', 1), ('A', 1),
                ('G', 1.5), ('A', .5), ('G', 1), ('A', 1),
                ('G', 1), ('B', .5), ('A', .5), ('G', 1), ('B', .5), ('A', .5),
                ('G', 1), ('B', .5), ('A', .5), ('G', 1), ('B', .5), ('A', .5),
                ('G', .5), ('A', .5), ('G', .5), ('A', .5), ('G', .5), ('A', .5), ('G', .5), ('A', .5),
                ('G', .5), ('A', .5), ('G', .5), ('A', .5), ('G', .5), ('A', .5), ('G', .5), ('A', .5),
                ('G', 1), ('z', 1), ('G', 1), ('z', 1),
                ('G', 4)]

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
