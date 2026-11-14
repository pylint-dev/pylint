# Unconditinoally decompressing without checking for file sizes
import zipfile

with zipfile.ZipFile("untrusted.zip") as archive:
    for f in archive.filelist:
        archive.extract(f)
