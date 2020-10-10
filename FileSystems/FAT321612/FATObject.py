class FATFileSys:
    FAT16_LEN_RECORD = 2
    FAT32_LEN_RECORD = 4

    FAT_VERSION = "FAT"
    BS_jmpBoot: int = 0
    BS_OEMName: int = 0
    BPB_BytsPerSec: int = 0
    BPB_SecPerClus: int = 0
    BPB_RsvdSecCnt: int = 0
    BPB_NumFATs: int = 0
    BPB_RootEntCnt: int = 0
    BPB_TotSec16: int = 0
    BPB_Media: int = 0
    BPB_FATSz16: int = 0
    BPB_SecPerTrk: int = 0
    BPB_NumHeads: int = 0
    BPB_HiddSec: int = 0
    BPB_TotSec32: int = 0

    # FAT1612
    BS_DrvNum: int = 0
    BS_Reserved1: int = 0
    BS_BootSig: int = 0
    BS_VolID: int = 0
    BS_VolLab: int = 0
    BS_FilSysType: int = 0

    # FAT32
    BPB_FATSz32: int = 0
    BPB_ExtFlags: int = 0
    BPB_FSVer: int = 0
    BPB_RootClus: int = 0
    BPB_FSInfo: int = 0
    BPB_BkBootSec: int = 0
    BPB_Reserved: int = 0
    BS_DrvNum: int = 0
    BS_Reserved1: int = 0
    BS_BootSig: int = 0
    BS_VolID: int = 0
    BS_VolLab: int = 0
    BS_FilSysType: int = 0

    # Для улучшения кода некторые значения вычислены и сохранены.
    fat_size: int = 0
    all_fat_size: int = 0

    def set_fat_version(self, fat_version: str):
        if fat_version in "FAT12FAT16FAT32":
            self.FAT_VERSION = fat_version

    def __str__(self):
        string_info = f"{self.FAT_VERSION=}\n" \
                      f"{self.fat_size=}\n" \
                      f"{self.all_fat_size=}\n"
        return string_info
