import os
import shutil
import subprocess

from plaintext_daw.cli import cli_entry_point


def test_render():
    if os.path.exists('song.wav'): os.remove('song.wav')
    cli_entry_point(['plaintext-daw', 'render', 'test/data/song.yml'])
    assert os.path.exists('song.wav')
    if os.path.exists('song.wav'): os.remove('song.wav')
