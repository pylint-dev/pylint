from enum import IntFlag


class OverlappingFlags(IntFlag):
    COLOUR = 1
    SOUND = 2
    SUBTITLES = 3  # [implicit-flag-alias]
