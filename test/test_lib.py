from plaintext_daw.lib import np_to_mp3
from plaintext_daw.models.synth import gen_sine
import os


def test_convert_mp3():
    if os.path.exists("song.mp3"): os.remove("song.mp3")

    sample_rate = 44100
    signal = gen_sine(65.406, 5, 2, sample_rate)
    np_to_mp3(signal, sample_rate, "song.mp3")

    assert os.path.exists("song.mp3")
    if os.path.exists("song.mp3"): os.remove("song.mp3")
