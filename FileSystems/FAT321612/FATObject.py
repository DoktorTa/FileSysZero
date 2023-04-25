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
    # BS_DrvNum: int = 0
    # BS_Reserved1: int = 0
    # BS_BootSig: int = 0
    # BS_VolID: int = 0
    # BS_VolLab: int = 0
    # BS_FilSysType: int = 0

    # Для улучшения кода некоторые значения вычислены и сохранены.
    fat_size: int = 0
    all_fat_size: int = 0

    FAT_TABLE: list = []

    EOC_LABEL: int = 0
    ERROR_LABEL: int = 0

    def set_fat_version(self, fat_version: str):
        if fat_version in "FAT12FAT16FAT32":
            self.FAT_VERSION = fat_version

    def __str__(self):
        string_info = f"{self.FAT_VERSION=}\n" \
                      f"{self.fat_size=}\n" \
                      f"{self.all_fat_size=}\n"
        return string_info


class FATFile:
    DIR_NAME: str = ''
    DIR_Attr: int = 0
    DIR_NTRes: int = 0
    DIR_CrtTimeTenth: int = 0
    DIR_CrtTime: int = 0
    DIR_CrtDate: int = 0
    DIR_LstAccDate: int = 0
    DIR_FstClusHI: int = 0
    DIR_WrtTime: int = 0
    DIR_WrtDate: int = 0
    DIR_FstClusLO: int = 0
    DIR_FileSize: int = 0

    DIR_NAME_LONG: str = ''

    class ATTRFile:
        # Указывает, что запись в файле закрывается неудачно.
        ATTR_READ_ONLY = 0b00000001

        # Указывает, что обычные списки каталогов не должны показывать этот файл.
        ATTR_HIDDEN = 0b00000010

        # Указывает, что это файловая система.
        ATTR_SYSTEM = 0b00000100

        # На томе, для которого установлен этот атрибут, должен быть только один «файл»,
        # и этот файл должен находиться в корневом каталоге. Это имя этого файла на самом деле является меткой для тома.
        ATTR_VOLUME_ID = 0b00001000

        # Показывает, что этот файл фактически является контейнером для других файлов.
        ATTR_DIRECTORY = 0b00010000

        # Бит установлен драйвером файловой системы FAT при создании, переименовании или записи файла.
        ATTR_ARCHIVE = 0b00100000

        # ATTR_READ_ONLY | ATTR_HIDDEN | ATTR_SYSTEM | ATTR_VOLUME_ID
        ATTR_LONG_NAME = 0b00001111

    # TODO: ух бля, сюда нужно что то поэлегантней.
    def __eq__(self, other):
        if isinstance(other, FATFile):
            answer: list = []
            answer.append(self.DIR_NAME == other.DIR_NAME)
            answer.append(self.DIR_Attr == other.DIR_Attr)
            answer.append(self.DIR_NTRes == other.DIR_NTRes)
            answer.append(self.DIR_CrtTimeTenth == other.DIR_CrtTimeTenth)
            answer.append(self.DIR_CrtTime == other.DIR_CrtTime)
            answer.append(self.DIR_CrtDate == other.DIR_CrtDate)
            answer.append(self.DIR_LstAccDate == other.DIR_LstAccDate)
            answer.append(self.DIR_FstClusHI == other.DIR_FstClusHI)
            answer.append(self.DIR_WrtTime == other.DIR_WrtTime)
            answer.append(self.DIR_WrtDate == other.DIR_WrtDate)
            answer.append(self.DIR_FstClusLO == other.DIR_FstClusLO)
            answer.append(self.DIR_FileSize == other.DIR_FileSize)
            answer.append(self.DIR_NAME_LONG == other.DIR_NAME_LONG)
            for eq in answer:
                if eq is False:
                    return False
            return True

    def __str__(self):
        answer = f"{self.DIR_NAME=}\n" \
                 f"{self.DIR_Attr=}\n" \
                 f"{self.DIR_NTRes=}\n" \
                 f"{self.DIR_CrtTimeTenth=}\n" \
                 f"{self.DIR_CrtTime=}\n" \
                 f"{self.DIR_CrtDate=}\n" \
                 f"{self.DIR_LstAccDate=}\n" \
                 f"{self.DIR_FstClusHI=}\n" \
                 f"{self.DIR_WrtTime=}\n" \
                 f"{self.DIR_WrtDate=}\n" \
                 f"{self.DIR_FstClusLO=}\n" \
                 f"{self.DIR_FileSize=}\n" \
                 f"{self.DIR_NAME_LONG=}\n"
        return answer


class FATLongName:
    LDIR_Ord: int = 0
    LDIR_Name1: str = ''
    LDIR_Attr: int = 0
    LDIR_Type: int = 0
    LDIR_Chksum: int = 0
    LDIR_Name2: str = ''
    LDIR_FstClusLO: int = 0
    LDIR_Name3: str = ''
