class FATFileSys:
    FAT16_LEN_RECORD = 2
    FAT32_LEN_RECORD = 4

    _FAT_version = "FAT"
    BS_jmpBoot: int
    BS_OEMName: int
    BPB_BytsPerSec: int
    BPB_SecPerClus: int
    BPB_RsvdSecCnt: int
    BPB_NumFATs: int
    BPB_RootEntCnt: int
    BPB_TotSec16: int
    BPB_Media: int
    BPB_FATSz16: int
    BPB_SecPerTrk: int
    BPB_NumHeads: int
    BPB_HiddSec: int
    BPB_TotSec32: int

    @property
    def get_version_fat(self):
        return self._FAT_version


class FAT1612FileSys(FATFileSys):
    BS_DrvNum: int
    BS_Reserved1: int
    BS_BootSig: int
    BS_VolID: int
    BS_VolLab: int
    BS_FilSysType: int


class FAT32FileSys(FATFileSys):
    BPB_FATSz32: int
    BPB_ExtFlags: int
    BPB_FSVer: int
    BPB_RootClus: int
    BPB_FSInfo: int
    BPB_BkBootSec: int
    BPB_Reserved: int
    BS_DrvNum: int
    BS_Reserved1: int
    BS_BootSig: int
    BS_VolID: int
    BS_VolLab: int
    BS_FilSysType: int