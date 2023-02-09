import os

import numpy as np

from plaintext_daw.cli import cli_entry_point
from plaintext_daw.lib import np_to_wav
from plaintext_daw.models.synthesizer.synth import Synth


def test_song1_render_local():
    if os.path.exists('song.wav'): os.remove('song.wav')
    cli_entry_point(['plaintext-daw', 'render', 'test/data/song1/song.yml'])
    assert os.path.exists('song.wav')
    if os.path.exists('song.wav'): os.remove('song.wav')

def test_song2_render_git():
    if os.path.exists('song.wav'): os.remove('song.wav')
    cli_entry_point(['plaintext-daw', 'render', 'test/data/song2/song.yml'])
    assert os.path.exists('song.wav')
    if os.path.exists('song.wav'): os.remove('song.wav')

def test_synth(): # TODO integrate with existing CLI
    sample_rate = 44100  # hz
    sample_width = 2  # bytes

    instrument = Synth.read_yaml("test/data/synth.yml")

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
