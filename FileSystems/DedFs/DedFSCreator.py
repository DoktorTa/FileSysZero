from DedFSObject import *


class DedFSCreate:
    fs: DedFSFileSys

    def __init__(self):
        self.fs = DedFSFileSys()

    def load_default_par(self):
        self.fs.BYTE_IN_SECTOR = 0x200
        self.fs.SECTOR_IN_CLUSTER = 0x1
        self.fs.MAGIC_NUMBER = '('

    def write_fs(self):
        pass

    def __write_end_MBR(self):
        len()
        last_magic = '55aa'
