"""Functional tests for decompression-bomb checker"""
# pylint: disable=import-outside-toplevel

def zip_extract_all(filename: str):
    import zipfile
    with zipfile.ZipFile(filename) as archive:
        archive.extractall() # [decompression-bomb]

def tar_extract_all(filename: str):
    import tarfile
    with tarfile.TarFile(filename) as archive:
        archive.extractall() # [decompression-bomb]

def zip_extract_plain(filename: str):
    import zipfile
    with zipfile.ZipFile(filename) as archive:
        for file in archive.infolist():
            archive.extract(file) # [decompression-bomb]

def tar_extract_plain(filename: str):
    import tarfile
    with tarfile.TarFile(filename) as archive:
        for file in archive:
            archive.extract(file) # [decompression-bomb]

def zip_check_size_only(filename: str):
    import zipfile
    with zipfile.ZipFile(filename) as archive:
        for file in archive.infolist():
            if file.file_size < 1000000 :
                archive.extract(file) # [decompression-bomb]

def tar_check_size_only(filename: str):
    import tarfile
    with tarfile.TarFile(filename) as archive:
        for file in archive:
            if file.size < 1000000 :
                archive.extract(file) # [decompression-bomb]

def zip_check_count_only(filename: str):
    import zipfile
    with zipfile.ZipFile(filename) as archive:
        if len(archive.infolist()) < 1000:
            for file in archive.infolist():
                archive.extract(file) # [decompression-bomb]

def tar_check_count_only(filename: str):
    import tarfile
    with tarfile.TarFile(filename) as archive:
        if len(archive.getmembers()) < 1000:
            for file in archive:
                archive.extract(file) # [decompression-bomb]

def no_warning_zip_check_sum(filename: str):
    import zipfile
    with zipfile.ZipFile(filename) as archive:
        total = 0
        for file in archive.infolist():
            total+=file.file_size
            if total < 1000000 :
                archive.extract(file)

def no_warning_tar_check_sum(filename: str):
    import tarfile
    with tarfile.TarFile(filename) as archive:
        total = 0
        for file in archive:
            total+=file.size
            if total < 1000000 :
                archive.extract(file)

def no_warning_zip_check_sum_outside(filename: str):
    import zipfile
    with zipfile.ZipFile(filename) as archive:
        total = sum((file.file_size for file in archive.infolist()))
        if total < 1000000:
            for file in archive.infolist():
                archive.extract(file)

def no_warning_tar_check_sum_outside(filename: str):
    import tarfile
    with tarfile.TarFile(filename) as archive:
        total = sum((file.size for file in archive.getnames()))
        if total < 1000000:
            for file in archive:
                archive.extract(file)

def no_warning_zip_check_size_and_count(filename: str):
    import zipfile
    with zipfile.ZipFile(filename) as archive:
        if len(archive.infolist()) < 1000:
            for file in archive.infolist():
                if file.file_size < 1000000 :
                    archive.extract(file)

def no_warning_tar_check_size_and_count(filename: str):
    import tarfile
    with tarfile.TarFile(filename) as archive:
        if len(archive.getmembers()) < 1000:
            for file in archive.getmembers():
                if file.file_size < 1000000 :
                    archive.extract(file)

def no_warning_zip_check_size_outer_and_count(filename: str):
    import zipfile
    with zipfile.ZipFile(filename) as archive:
        largest= max((file.file_size for file in archive.filelist))
        if len(archive.infolist()) < 1000 and largest<1000000:
            for file in archive.infolist():
                archive.extract(file)

def no_warning_tar_check_size_outer_and_count(filename: str):
    import tarfile
    with tarfile.TarFile(filename) as archive:
        largest= max((file.size for file in archive))
        if len(archive) < 1000 and largest<1000000:
            for file in archive:
                archive.extract(file)
