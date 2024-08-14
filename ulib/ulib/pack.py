"""Tools to pack folders and files.
:todo: 7za
"""
import logging
import os
import pathlib
import zipfile
from typing import Iterable

import zstandard


def pack_dir(src: pathlib.Path, dst: pathlib.Path, files: Iterable[str]):
    """Pack files into zip-file.
    :param src: Source folder
    :param dst: Destination folder
    :param files: List of files in src to pack (relative to src)
    :note: destinatio file will be <dst>/<src.name>.zip
    :todo: bz2, lzma
    :todo: exceptions
    """
    filelist = []
    for mask in files:
        filelist.extend([str(f.name) for f in src.glob(mask, case_sensitive=False)])
    if not filelist:
        return
    logging.debug("Zip %s => %s/", str(src), str(dst))
    cwd = os.getcwd()
    os.chdir(str(src))
    with zipfile.ZipFile(str(dst / src.name) + '.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as myzip:
        for f in filelist:
            myzip.write(f)
    os.chdir(cwd)


def pack_file(src: pathlib.Path, dst: pathlib.Path):
    """Pack file into file.
    :param src: Source file
    :param dst: Destination file w/o ext
    :todo: exceptions
    """
    logging.debug(f"Pack {src} => {dst}.zst")
    with open(str(src), "rb") as ifh, open(str(dst) + '.zst', "wb") as ofh:
        zstandard.ZstdCompressor().copy_stream(ifh, ofh)
