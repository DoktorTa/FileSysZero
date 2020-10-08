class FATFileSys:
    FAT16_LEN_RECORD = 2
    FAT32_LEN_RECORD = 4

    FAT_VERSION = "FAT"
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

    # FAT1612
    BS_DrvNum: int
    BS_Reserved1: int
    BS_BootSig: int
    BS_VolID: int
    BS_VolLab: int
    BS_FilSysType: int

    # FAT32
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

    # Для улучшения кода некторые значения вычислены и сохранены.
    fat_size: int
    all_fat_size: int

    def set_fat_version(self, fat_version: str):
        if fat_version in "FAT12FAT16FAT32":
            self.FAT_VERSION = fat_version

    def __str__(self):
        string_info = f"{self.FAT_VERSION=}\n" \
                      f"{self.fat_size=}\n" \
                      f"{self.all_fat_size=}\n"
        return string_info
