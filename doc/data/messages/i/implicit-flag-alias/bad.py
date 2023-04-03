from enum import IntFlag


class FilePermissions(IntFlag):
    READ = 1
    WRITE = 2
    EXECUTE = 3  # [implicit-flag-alias]
