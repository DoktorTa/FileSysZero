import logging
import struct
import functools
import operator

from FAT321612.FATObject import FATFileSys


class FATReader:
    __mount_fs = None
    file_system: FATFileSys

    def __int__(self, mount_fs):
        self.__mount_fs = mount_fs

    def __parse_super_block(self):
        len_super_block = 512
        super_block = self.__read_block(0, len_super_block)
        super_block_part_one = super_block[1:40]
        super_block_part_two = super_block[36:90]
        # print(super_block_part_one)
        # print('two', super_block_part_two)
        super_block_struct = struct.unpack('<H8chBhb2hB3h3i', super_block_part_one)
        self.__change_first_part_super_block(super_block_struct)
        self.__parse_fat32_super_block(super_block_part_two)
        self._calculation_num_fat_and_root_dir_sector()
        # print(self.file_system.__dict__)

    def __parse_fat32_super_block(self, super_block_part_two):
        # print(len(super_block_part_two))
        part_two_super_block = struct.unpack('<i2hi2h12c3BI11c8c', super_block_part_two)
        self.__change_second_part_super_block(part_two_super_block)

    def __change_second_part_super_block(self, super_block_struct: tuple):
        self.file_system.BPB_FATSz32 = super_block_struct[0]
        self.file_system.BPB_ExtFlags = super_block_struct[1]
        self.file_system.BPB_FSVer = super_block_struct[2]
        self.file_system.BPB_RootClus = super_block_struct[3]
        self.file_system.BPB_FSInfo = super_block_struct[4]
        self.file_system.BPB_BkBootSec = super_block_struct[5]
        self.file_system.BPB_Reserved = functools.reduce(
            operator.add, (super_block_struct[6:18])).decode('ascii')
        self.__change_third_part_super_block(super_block_struct[18:])

    def __change_third_part_super_block(self, super_block_struct: tuple):
        self.file_system.BS_DrvNum = super_block_struct[0]
        self.file_system.BS_Reserved1 = super_block_struct[1]
        self.file_system.BS_BootSig = super_block_struct[2]
        self.file_system.BS_VolID = super_block_struct[3]
        self.file_system.BS_VolLab = functools.reduce(
            operator.add, (super_block_struct[4:15])).decode('ascii')
        self.file_system.BS_FilSysType = functools.reduce(
            operator.add, (super_block_struct[15:24])).decode('ascii')

    def __change_first_part_super_block(self, super_block_struct: tuple):
        self.file_system = FATFileSys()

        self.file_system.BS_jmpBoot = super_block_struct[0]
        self.file_system.BS_OEMName = functools.reduce(
            operator.add, (super_block_struct[1:9])).decode('ascii')
        self.file_system.BPB_BytsPerSec = super_block_struct[9]
        self.file_system.BPB_SecPerClus = super_block_struct[10]
        self.file_system.BPB_RsvdSecCnt = super_block_struct[11]
        self.file_system.BPB_NumFATs = super_block_struct[12]
        self.file_system.BPB_RootEntCnt = super_block_struct[13]
        self.file_system.BPB_TotSec16 = super_block_struct[14]
        self.file_system.BPB_Media = super_block_struct[15]
        self.file_system.BPB_FATSz16 = super_block_struct[16]
        self.file_system.BPB_SecPerTrk = super_block_struct[17]
        self.file_system.BPB_NumHeads = super_block_struct[18]
        self.file_system.BPB_HiddSec = super_block_struct[19]
        self.file_system.BPB_TotSec32 = super_block_struct[20]

    def _calculation_num_fat_and_root_dir_sector(self):
        """
            Функция вычисляет номер фс fat и устанавливет его для обьекта,
            а тк же вычисляет и возврашает колличество секторов корневого
            каталога.
            :return: Количество секторов, занимаемых корневым каталогом.
        """

        root_dir_sector = self.__calculation_number_sectors_root(
            self.file_system.BPB_RootEntCnt, self.file_system.BPB_BytsPerSec)

        total_sector = self.__calculation_total_sector(
            self.file_system.BPB_TotSec16, self.file_system.BPB_TotSec32)

        self.file_system.fat_size = self.__calculation_fat_size(
            self.file_system.BPB_FATSz16, self.file_system.BPB_FATSz32)

        self.file_system.all_fat_size = self.__calculation_all_fat_size(
            self.file_system.BPB_NumFATs, self.file_system.fat_size)

        data_sector = self.__calculation_data_sector(
            total_sector, self.file_system.all_fat_size, root_dir_sector,
            self.file_system.BPB_RsvdSecCnt)

        count_of_clusters = self.__calculation_count_of_clusters(
            data_sector, self.file_system.BPB_SecPerClus)

        self.file_system.set_fat_version(self.__choice_fs(count_of_clusters))

        logging.info(f"{self.file_system.FAT_VERSION=}")

        return root_dir_sector

    @staticmethod
    def __calculation_count_of_clusters(data_sector: int, BPB_SecPerClus: int) -> int:
        """
            :return: Колличество всех кластеров данных в системе.
        """
        return data_sector // BPB_SecPerClus

    @staticmethod
    def __calculation_data_sector(total_sector: int, all_fat_size: int,
                                  root_dir_sector: int, BPB_ResvdSecCnt: int) -> int:
        """
            :return: Колличество всех секторов с данными.
        """
        no_data_sector = (BPB_ResvdSecCnt + all_fat_size + root_dir_sector)
        return total_sector - no_data_sector

    @staticmethod
    def __calculation_number_sectors_root(
            BPB_RootEntCnt: int, BPB_BytsPerSec: int) -> int:
        """
            :return: Количество секторов, занимаемых корневым каталогом.
        """
        records_dir_in_root = (BPB_RootEntCnt * 32)
        bytes_in_root = (BPB_BytsPerSec - 1) + records_dir_in_root
        return bytes_in_root // BPB_BytsPerSec

    @staticmethod
    def __calculation_all_fat_size(BPB_NumFATs: int, fat_size: int) -> int:
        return BPB_NumFATs * fat_size

    @staticmethod
    def __calculation_total_sector(BPB_TotSec16: int, BPB_TotSec32: int) -> int:
        """
            :return: Количество всех секторов во всех четырех областях тома.
        """
        if BPB_TotSec16 != 0:
            return BPB_TotSec16
        else:
            return BPB_TotSec32

    @staticmethod
    def __calculation_fat_size(BPB_FATSz16: int, BPB_FATSz32: int) -> int:
        """
            :return: Размер одной таблицы FAT.
        """
        if BPB_FATSz16 != 0:
            return BPB_FATSz16
        else:
            return BPB_FATSz32

    @staticmethod
    def __choice_fs(count_of_clusters: int) -> str:
        """
        Возвращает название файловой системы в зависимости от колличества
            кластеров.

        65526 < FAT32, 4085 < FAT16 < 65525, FAT12 < 4085

        :param count_of_clusters: колличество кластеров в файловой системе
        :return: название файловой системы строкой "FAT32", "FAT16", "FAT12".
        """
        count_of_clusters_fat_12 = 4085
        count_of_clusters_fat_16 = 65525

        if count_of_clusters < count_of_clusters_fat_12:
            return "FAT12"
        elif count_of_clusters < count_of_clusters_fat_16:
            return "FAT16"
        else:
            return "FAT32"

    def __read_block(self, seek_block: int, len_block: int) -> bytes:
        return b"z"
        self.__mount_fs.seek(seek_block)
        return self.__mount_fs.read(len_block)
