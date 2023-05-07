import struct
import operator
import functools

from FileSystems.FAT321612.FATObject import FATFileSys, FATFile, FATLongName


class FATStructParsers:
    POS_FILE_ATTR_IN_FILE_STRUCT = 11
    POS_FILE_SIZE_IN_FILE_STRUCT = 21

    def parse_long_name(self, fat_long_name: bytes) -> FATLongName:
        long_struct: tuple = struct.unpack('<B10c3B12cH4c', fat_long_name)
        return self.__parse_long_name(long_struct)

    def parse_file(self, fat_file: bytes) -> FATFile:
        file_struct: tuple = struct.unpack('11c3B7HI', fat_file)
        return self.__parse_file(file_struct)

    def parse_first_part_super_block(self, file_system: FATFileSys, super_block_part_one: bytes) -> FATFileSys:
        part_one_super_block: tuple = struct.unpack('<3c8chBhb2hB3h2i', super_block_part_one)
        return self.__parse_first_part_super_block(file_system, part_one_super_block)

    def parse_second_part_super_block(self, file_system: FATFileSys, super_block_part_two: bytes) -> FATFileSys:
        part_two_super_block: tuple = struct.unpack('<i2hi2h12c', super_block_part_two)
        return self.__parse_second_part_super_block(file_system, part_two_super_block)

    def parse_third_part_super_block(self, file_system: FATFileSys, super_block_part_three: bytes) -> FATFileSys:
        part_three_super_block: tuple = struct.unpack('<3BI11c8c', super_block_part_three)
        return self.__parse_third_part_super_block(file_system, part_three_super_block)

    def __parse_long_name(self, file_struct: tuple) -> FATLongName:
        long_name = FATLongName()

        long_name.LDIR_Ord = file_struct[0]
        long_name.LDIR_Name1 = functools.reduce(operator.add, file_struct[1:10]).decode('ascii')
        long_name.LDIR_Attr = file_struct[self.POS_FILE_ATTR_IN_FILE_STRUCT]
        long_name.LDIR_Type = file_struct[12]
        long_name.LDIR_Chksum = file_struct[13]
        long_name.LDIR_Name2 = functools.reduce(operator.add, file_struct[14:26]).decode('ascii')
        long_name.LDIR_FstClusLO = file_struct[27]
        long_name.LDIR_Name3 = functools.reduce(operator.add, file_struct[28:32]).decode('ascii')

        return long_name

    def __parse_file(self, file_struct: tuple) -> FATFile:
        fat_file = FATFile()
        fat_file.DIR_NAME = functools.reduce(operator.add, file_struct[0:11]).decode('ascii')
        fat_file.DIR_Attr = file_struct[self.POS_FILE_ATTR_IN_FILE_STRUCT]
        fat_file.DIR_NTRes = file_struct[12]
        fat_file.DIR_CrtTimeTenth = file_struct[13]
        fat_file.DIR_CrtTime = file_struct[14]
        fat_file.DIR_CrtDate = file_struct[15]
        fat_file.DIR_LstAccDate = file_struct[16]
        fat_file.DIR_FstClusHI = file_struct[17]
        fat_file.DIR_WrtTime = file_struct[18]
        fat_file.DIR_WrtDate = file_struct[19]
        fat_file.DIR_FstClusLO = file_struct[20]
        fat_file.DIR_FileSize = file_struct[self.POS_FILE_SIZE_IN_FILE_STRUCT]

        return fat_file

    def __parse_first_part_super_block(self, file_system: FATFileSys, super_block_struct: tuple) -> FATFileSys:
        file_system.BS_jmpBoot = functools.reduce(
            operator.add, (super_block_struct[0:3]))
        file_system.BS_OEMName = functools.reduce(
            operator.add, (super_block_struct[3:11])).decode('latin-1')
        file_system.BPB_BytsPerSec = super_block_struct[11]
        file_system.BPB_SecPerClus = super_block_struct[12]
        file_system.BPB_RsvdSecCnt = super_block_struct[13]
        file_system.BPB_NumFATs = super_block_struct[14]
        file_system.BPB_RootEntCnt = super_block_struct[15]
        file_system.BPB_TotSec16 = super_block_struct[16]
        file_system.BPB_Media = super_block_struct[17]
        file_system.BPB_FATSz16 = super_block_struct[18]
        file_system.BPB_SecPerTrk = super_block_struct[19]
        file_system.BPB_NumHeads = super_block_struct[20]
        file_system.BPB_HiddSec = super_block_struct[21]
        file_system.BPB_TotSec32 = super_block_struct[22]

        return file_system

    def __parse_second_part_super_block(self, file_system: FATFileSys, super_block_struct: tuple):
        file_system.BPB_FATSz32 = super_block_struct[0]
        file_system.BPB_ExtFlags = super_block_struct[1]
        file_system.BPB_FSVer = super_block_struct[2]
        file_system.BPB_RootClus = super_block_struct[3]
        file_system.BPB_FSInfo = super_block_struct[4]
        file_system.BPB_BkBootSec = super_block_struct[5]
        file_system.BPB_Reserved = functools.reduce(
            operator.add, (super_block_struct[6:18])).decode('latin-1')

        return file_system

    def __parse_third_part_super_block(self, file_system: FATFileSys, super_block_struct: tuple):
        file_system.BS_DrvNum = super_block_struct[0]
        file_system.BS_Reserved1 = super_block_struct[1]
        file_system.BS_BootSig = super_block_struct[2]
        file_system.BS_VolID = super_block_struct[3]
        file_system.BS_VolLab = functools.reduce(
            operator.add, (super_block_struct[4:15])).decode('latin-1')
        file_system.BS_FilSysType = functools.reduce(
            operator.add, (super_block_struct[15:24])).decode('latin-1')

        return file_system
