import subprocess

from plaintext_daw.cli import cli_entry_point


def test_render():
    cli_entry_point(['plaintext-daw', 'test/data/song.yml'])
