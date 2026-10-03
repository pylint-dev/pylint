# pylint: disable=missing-function-docstring

"""
Regression tests for StopIteration raised when using limit-inference-results=0
"""


def get_youtube_link(song_name: str, song_artists):
    with open("possible errors.txt", "ab") as file:
        file.write(f"{', '.join(song_artists)} - {song_name}".encode())
