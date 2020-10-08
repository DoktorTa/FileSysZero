from FAT321612.FATObject import FATFileSys


class FATReader:
    __mount_fs = None
    file_system: FATFileSys

    def __int__(self, mount_fs):
        self.__mount_fs = mount_fs

    def __parse_super_block(self):
        pass

    def check_num_fs(self):

        root_dir_sector = self.__calculation_number_sectors_root(
            self.file_system.BPB_RootEntCnt, self.file_system.BPB_BytsPerSec)

        total_sector = self.__calculation_total_sector(
            self.file_system.BPB_TotSec16, self.file_system.BPB_TotSec32)

        self.file_system.fat_size = self.__calculation_fat_size(
            self.file_system.BPB_FATSz16, self.file_system.BPB_FATSz32)

        self.file_system.all_fat_size = self.__calculation_all_fat_size(
            self.file_system.BPB_NumFATs, self.file_system.fat_size)

        data_sector = total_sector - (self.data.bpb_reversed_sector
                                      + all_fat_size
                                      + root_dir_sector)
        count_of_clusters = data_sector // self.data.bpb_sector_in_claster

        self.file_system.set_fat_version(self.__choice_fs(count_of_clusters))

        return all_fat_size, root_dir_sector

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
    def __calculation_total_sector(BPB_TotSec16: int, BPB_TotSec32: int)\
            -> int:
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
        self.__mount_fs.seek(seek_block)
        return self.__mount_fs.read(len_block)
