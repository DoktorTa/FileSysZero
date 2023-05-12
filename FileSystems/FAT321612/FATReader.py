import logging
from typing import List, Tuple

from FileSystems.FAT321612.FATObject import FATFileSys, FATFile, FATLongName, FSInfo
from FileSystems.FAT321612.FATStructParsers import FATStructParsers


class FATReader:
    __mount_fs = None
    file_system: FATFileSys
    __struct_parsers: FATStructParsers

    def __init__(self, mount_fs):
        self.__mount_fs = mount_fs
        self.__struct_parsers = FATStructParsers()
        # self.__parse_super_block()

    def __parse_super_block(self):
        len_super_block = 512
        super_block = self.__read_block(0, len_super_block)
        super_block_part_one = super_block[1:36]

        self.file_system = FATFileSys()
        self.__struct_parsers.parse_first_part_super_block(self.file_system, super_block_part_one)

        super_block_part_two = super_block[36:64]

        # Для расчета номера версии файловой системы, мне необходимо использовать поле BPB_FATSz32,
        # данное поле существует только у FAT32, поэтому мы изначально парсим ФС как FAT32 (А так же ради оптимизации)
        # в случае если ФС не FAT32 нам нужно занулить часть значений которые были распаршены
        # ввиду того, что они не существуют на ФС FAT16 и FAT12.

        self.__struct_parsers.parse_second_part_super_block(self.file_system, super_block_part_two)
        if self.file_system.FAT_VERSION == "FAT32":
            super_block_part_three = super_block[64:90]
            self.__struct_parsers.parse_third_part_super_block(self.file_system, super_block_part_three)
            self.__read_fs_info()
        else:
            super_block_part_two = super_block[36:62]
            self.__zeroing_out_erroneous_entries()
            self.__struct_parsers.parse_second_part_super_block(self.file_system, super_block_part_two)

        # Для FAT32 всегда 0
        root_dir_sector = self._calculation_num_fat_and_root_dir_sector()


        fat_seek_b = self.file_system.BPB_RsvdSecCnt * self.file_system.BPB_BytsPerSec
        print(fat_seek_b)
        # print(self.file_system.__dict__)

    def __read_fs_info(self):
        seek_fs_info = self.file_system.BPB_FSInfo * self.file_system.BPB_BytsPerSec
        fs_info_block = self.__read_block(seek_fs_info, FSInfo.LEN_FS_INFO)
        self.file_system.fs_info = self.__struct_parsers.parse_fs_info(fs_info_block, FSInfo())

    def __zeroing_out_erroneous_entries(self):
        self.file_system.BPB_FATSz32 = 0
        self.file_system.BPB_ExtFlags = 0
        self.file_system.BPB_FSVer = 0
        self.file_system.BPB_RootClus = 0
        self.file_system.BPB_FSInfo = 0
        self.file_system.BPB_BkBootSec = 0
        self.file_system.BPB_Reserved = 0

    def get_root(self):
        """
            Получить количество секторов
            Получить смешение корневого
            перейти на смещение
            прочесть кластер
            декремента количества секторов
            распарсить сектор как каталог
        :return:
        """

        # fat_table = self.__read_block(fat_seek, self.file_system.fat_size)
        # self.file_system.FAT_TABLE = self.__convert_byte_sequence_to_list_clusters(fat_table)

        pass

    def parse_directory(self, one_cluster_dir: bytes) -> list:
        """
            Изначально вам покажется что я путаюсь с тем что есть файл, а что директория
            но это не так, видите ли, каждая директория в FAT является файлом, с
            единственным отличием, флагом директории вместо флага файла.
        :param one_cluster_dir:
        :return:
        """
        files_in_dir: List[Tuple[FATFile, List[FATLongName]]] = []
        long_name_group: List[FATLongName] = []
        block_file_in_cluster: list = \
            [one_cluster_dir[i: i + 32] for i in range(0, len(one_cluster_dir), 32)]

        for fat_file in block_file_in_cluster:
            # file_struct: tuple = struct.unpack('11c3B7HI', fat_file)

            if file_struct[self.POS_FILE_ATTR_IN_FILE_STRUCT] == FATFile.ATTRFile.ATTR_LONG_NAME \
                    and file_struct[self.POS_FILE_SIZE_IN_FILE_STRUCT] == 0:
                long_name_group.append(self.__parse_long_name(file_struct))
            else:
                files_in_dir.append((self.__parse_file(file_struct), long_name_group))

        return files_in_dir

    def __ask_eoc_label(self) -> None:
        """
            Устанавливает метку для конечного кластера файла.
        """
        if self.file_system.FAT_VERSION == 'FAT12':
            self.file_system.EOC_LABEL = 0x0FFF
        elif self.file_system.FAT_VERSION == 'FAT16':
            self.file_system.EOC_LABEL = 0x0FFFF
        elif self.file_system.FAT_VERSION == 'FAT32':
            self.file_system.EOC_LABEL = 0x0FFFFFFF

    def __ask_error_label(self) -> None:
        """
            Устанавливает метку для поврежденного кластера файла.
        """
        if self.file_system.FAT_VERSION == 'FAT12':
            self.file_system.ERROR_LABEL = 0x0FF7
        elif self.file_system.FAT_VERSION == 'FAT16':
            self.file_system.ERROR_LABEL = 0x0FFF7
        elif self.file_system.FAT_VERSION == 'FAT32':
            self.file_system.ERROR_LABEL = 0x0FFFFFF7

    def get_next_group_clusters(self, num_start_cluster: int, len_sequence: int) -> (list, str):
        """
            Строит последовательность из кластеров, по которой можно прочесть файл.
            Так как файлы могут занимать множество кластеров, то за один раз можно
            построить только последовательность ограниченной длинны.
        :return:
        """
        error: str = ''

        cluster_sequence: list = []
        for i in range(len_sequence):
            next_cluster: int = self.file_system.FAT_TABLE[num_start_cluster]
            num_start_cluster = next_cluster

            if next_cluster == self.file_system.ERROR_LABEL:
                error = 'Last label is error.'
                break
            elif next_cluster == self.file_system.EOC_LABEL:
                break

            cluster_sequence.append(next_cluster)

        return cluster_sequence, error

    def __convert_byte_sequence_to_list_clusters(self, byte_sequence: bytes) -> list:
        """
            Данный метод в данной версии способе работать только лишь с FAT32.

            Преобразует байтовый массив фат таблицы, в лист содержавший в себе кластеры.
        :param byte_sequence: байтовый массив фат таблицы
        :return: лист содержавший в себе кластеры
        """

        len_cluster: int = 0

        if self.file_system.FAT_VERSION == 'FAT32':
            len_cluster = 8

        byte_sequence_str: str = byte_sequence.hex()

        # Данное генераторное выражение делит одну большую строку с кластерами на лист
        # в котором содержатся кластеры.
        list_clusters: list = \
            [byte_sequence_str[num_start_byte_claster:num_start_byte_claster + len_cluster]
             for num_start_byte_claster in range(0, len(byte_sequence_str), len_cluster)]

        # Поскольку все кластеры, это строка, то этот метод преобразовывает их в число,
        # так же, первые четыре байта кластера не играют роли поэтому их нельзя учитывать
        # в приведении.
        list_clusters = [int(claster[1:], 16) for claster in list_clusters]

        return list_clusters

    def get_offset_in_fat_table(self, num_claster: int, num_fat=0):
        """
        this_fat_sec_num - это номер сектора FAT, который содержит запись для кластера N в первой FAT.
        num_fat_seek - используется для получения номера сектора во последующих FAT
        """

        if self.file_system.FAT_VERSION == "FAT16":
            fat_offset = num_claster * 2
        elif self.file_system.FAT_VERSION == "FAT32":
            fat_offset = num_claster * 4
        else:  # FAT12
            fat_offset = num_fat + (num_fat // 2)

        num_fat_seek = self.file_system.fat_size * num_fat
        this_fat_sec_num = self.file_system.BPB_RsvdSecCnt + (fat_offset // self.file_system.BPB_BytsPerSec)
        this_fat_sec_num += + num_fat_seek
        this_fat_ent_offset = fat_offset % self.file_system.BPB_BytsPerSec

    def _calculation_num_fat_and_root_dir_sector(self):
        """
            Функция вычисляет номер фс fat и устанавливает его для объекта,
            а так же вычисляет и возвращает количество секторов корневого
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
            :return: Количество всех кластеров данных в системе.
        """
        return data_sector // BPB_SecPerClus

    @staticmethod
    def __calculation_data_sector(total_sector: int, all_fat_size: int,
                                  root_dir_sector: int, BPB_ResvdSecCnt: int) -> int:
        """
            :return: Количество всех секторов с данными.
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


if __name__ == '__main__':
    with open(r"A:\ProgrammingLanguages\InDeveloping\Python\FileSysZero\Test\TestResources\FAT321612\testFAT32.img", "r") as file:
        f = FATReader(file)
