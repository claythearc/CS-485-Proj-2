"""
CS 485 Project 2.
Determines File Types through the signatures of the given File.

By: Clayton Turner
Written for Python 3.6.5; however, it should work with any variation that supports f-strings.
"""

import binascii
import os

first_bytes = {
    "JPEG" : b"FFD8FFE000104A464946",
    "GIF" :  b"474946383761",
    "EXE" : b"4D5A",
    "BMP" : b"424D",
    "PDF" : b"25504446",
    "MSOFT 2003" : b"D0CF11E0A1B11AE1",
    "MSOFT 2007" : b"504B030414000600"
}


def is_ascii(content: bin) -> bool:
    """There are two ways to approach this:
     return any(ord(x) < 128 for x in binascii.unhexlify(content).decode("ascii")) or my way
    this way is slightly faster because it reduces function calls; however both are valid.
    """
    try:
        return binascii.unhexlify(content).decode("ascii")
    except UnicodeDecodeError:
        return False

def is_png(content: bin) -> bool:
    """
    Checks if a file is a PNG file or not, by
    first: checking if it starts with the PNG header,
    then: looks for the IHDR chunk
    then: looks for the IEND chunk
    finally: returns IEND and IHDR which is true IFF both are True.
    """
    IHDR, IEND = False, False
    if content.startswith(b"89504E47".lower()): # check the header of the file.
        for chunk in range(len(content) - 8):
            if b"49484452" in content[chunk:chunk+8]:
                IHDR = True
            if b"49454E44".lower() in content[chunk:chunk+8]:
                IEND = True
    return IHDR and IEND


FILE_PATH = input("Give relative path to folder with files, e.g ./samples: ")
if os.path.exists(FILE_PATH):
    for file in os.listdir(FILE_PATH):
        with open(f"./{FILE_PATH}/{file}", "rb") as f:
            flist = f.read()
            flist = binascii.hexlify(flist)
            for k, v in first_bytes.items():
                if flist.startswith(v.lower()):
                    print(f"File: {file} Type: {k}")
                    continue
            if is_ascii(flist): # check if the file is ascii or not for text
                print(f"File: {file} Type: TXT")
            elif is_png(flist): # check if the headers are right for PNG files
                print(f"File: {file} Type: PNG")
else:
    print(f"Path: {FILE_PATH} cannot be found.")