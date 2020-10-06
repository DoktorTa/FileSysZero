from FAT321612.FATObject import FATFileSys


class FATReader:
    __mount_fs = None
    file_system: FATFileSys

    def __int__(self, mount_fs):
        self.__mount_fs = mount_fs

    def __parse_super_block(self):
        pass

    def check_num_fs(self):

        root_dir_sector = (((self.data.bpb_root_ent_cnt * 32)
                            + (self.data.bpb_byte_in_sector - 1))
                           // self.data.bpb_byte_in_sector)



        if self.data.bpb_total_sector_16_12 != 0:
            total_sector = self.data.bpb_total_sector_16_12
        else:
            total_sector = self.data.bpb_total_sector_32

        all_fat_size = self.data.bpb_num_fat * fat_size
        data_sector = total_sector - (self.data.bpb_reversed_sector
                                      + all_fat_size
                                      + root_dir_sector)
        count_of_clusters = data_sector // self.data.bpb_sector_in_claster


        return all_fat_size, root_dir_sector

    @staticmethod
    def v1__calculation_fat_size(BPB_FATSz16: int, BPB_FATSz32: int) -> int:
        if BPB_FATSz16 != 0:
            return BPB_FATSz16
        else:
            return BPB_FATSz32

    def v2__calculation_fat_size(self):
        if self.file_system.BPB_FATSz16 != 0:
            self.file_system.fat_size = self.file_system.BPB_FATSz16
        else:
            self.file_system.fat_size = self.file_system.BPB_FATSz32

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
