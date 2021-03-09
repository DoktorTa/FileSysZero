from DedFs.DedFSObject import DedFSFileSys, DedFSFile


class DedFSRead:
    def __init__(self):
        pass

    def __parse_file(self, file_block: bytes) -> DedFSFile:
        file = DedFSFile()
        file.NAME_F = file_block[0:32]
        file.FILE_MOD = file_block[32:33]

