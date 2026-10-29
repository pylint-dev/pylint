# checking file count and size before extracting
import zipfile

MAX_FILE_SIZE = 1000000
MAX_FILES = 1000

with zipfile.ZipFile('untrusted.zip') as archive:
    if len(archive.filelist) > MAX_FILES:
        print("Too many files")
    else:
        for file in archive.filelist:
            if file.file_size > MAX_FILE_SIZE:
                print("File is too large")
            else:
                archive.extract(file)

