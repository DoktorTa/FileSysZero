from DedFs.DedFSObject import *


class DedFSCreate:
    fs: DedFSFileSys

    def __init__(self):
        self.fs = DedFSFileSys()

    def load_MBR(self, parameters: bytes) -> None:
        self.fs.MBR = parameters

    def generate_zero_file(self, count_zero: int, file_path) -> None:
        with open(file_path, 'wb') as file_zero:
            file_zero.write(self.fs.MBR)
            file_zero.write(b'\x00' * count_zero)
