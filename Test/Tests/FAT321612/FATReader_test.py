import pytest
# from pytest_mock import mocker

from FileSystems.FAT321612 import FATReader, FATObject
from FileSystems.FAT321612.FATObject import FATFile


class TestFATReader:

    @pytest.mark.parametrize("count_cluster, name_fs",
                             [(65526, "FAT32"), (101200, "FAT32"),
                              (65524, "FAT16"), (4085, "FAT16"),
                              (4084, "FAT12"), (257, "FAT12")])
    def test_choice_fs(self, count_cluster: int, name_fs: str):
        fat = FATReader.FATReader
        assert fat._FATReader__choice_fs(count_cluster) == name_fs

    @pytest.mark.parametrize("fat_sz16, fat_sz32, fat_size", [(0, 2, 2), (2, 0, 2)])
    def test_calculation_fat_size(self, fat_sz16: int, fat_sz32: int, fat_size: int):
        fat = FATReader.FATReader
        assert fat._FATReader__calculation_fat_size(fat_sz16, fat_sz32) == fat_size

    @pytest.mark.parametrize("BPB_TotSec16, BPB_TotSec32, count_sec", [(0, 2, 2), (2, 0, 2)])
    def test_calculation_total_sector(self, BPB_TotSec16: int,
                                      BPB_TotSec32: int, count_sec: int):
        fat = FATReader.FATReader
        assert fat._FATReader__calculation_total_sector(BPB_TotSec16, BPB_TotSec32) == count_sec

    def test_calculation_all_fat_size(self):
        fat = FATReader.FATReader
        assert fat._FATReader__calculation_all_fat_size(2, 484600) == 969200

    @pytest.mark.parametrize("BPB_RootEntCnt, BPB_BytsPerSec, root_sec",
                             [(512, 512, 32), (0, 512, 0)])
    def test_calculation_number_sectors_root(self, BPB_RootEntCnt: int,
                                             BPB_BytsPerSec: int, root_sec: int):
        fat = FATReader.FATReader
        assert fat._FATReader__calculation_number_sectors_root(BPB_RootEntCnt, BPB_BytsPerSec) == root_sec

    def test_calculation_data_sector(self):
        fat = FATReader.FATReader
        assert fat._FATReader__calculation_data_sector(1000, 8, 12, 2) == 978

    def test_calculation_count_of_clusters(self):
        fat = FATReader.FATReader
        assert fat._FATReader__calculation_count_of_clusters(64, 8) == 8

    def test_calculation_num_fat_and_root_dir_sector(self):
        fat32_obj = FATObject.FATFileSys()
        fat32_obj.BPB_RootEntCnt = 0
        fat32_obj.BPB_BytsPerSec = 512
        fat32_obj.BPB_TotSec16 = 0
        fat32_obj.BPB_TotSec32 = 2097152
        fat32_obj.BPB_FATSz16 = 0
        fat32_obj.BPB_FATSz32 = 2048
        fat32_obj.BPB_NumFATs = 2
        fat32_obj.BPB_RsvdSecCnt = 32
        fat32_obj.BPB_SecPerClus = 8

        fat16_obj = FATObject.FATFileSys()
        fat16_obj.BPB_RootEntCnt = 512
        fat16_obj.BPB_BytsPerSec = 512
        fat16_obj.BPB_TotSec16 = 0
        fat16_obj.BPB_TotSec32 = 102400
        fat16_obj.BPB_FATSz16 = 100
        fat16_obj.BPB_FATSz32 = 4362368
        fat16_obj.BPB_NumFATs = 2
        fat16_obj.BPB_RsvdSecCnt = 4
        fat16_obj.BPB_SecPerClus = 4

        fat12_obj = FATObject.FATFileSys()
        fat12_obj.BPB_RootEntCnt = 512
        fat12_obj.BPB_BytsPerSec = 512
        fat12_obj.BPB_TotSec16 = 24576
        fat12_obj.BPB_TotSec32 = 0
        fat12_obj.BPB_FATSz16 = 16
        fat12_obj.BPB_FATSz32 = 556335232
        fat12_obj.BPB_NumFATs = 2
        fat12_obj.BPB_RsvdSecCnt = 8
        fat12_obj.BPB_SecPerClus = 8

        fat_values = ["FAT32", "FAT16", "FAT12"]
        fat_obj = [fat32_obj, fat16_obj, fat12_obj]

        for i in range(len(fat_values)):

            fat = FATReader.FATReader("")
            fat.file_system = fat_obj[i]
            x = fat._calculation_num_fat_and_root_dir_sector()
            assert fat.file_system.FAT_VERSION == fat_values[i]

    def test_parse_fat32_super_block(self):
        fat32_obj = FATObject.FATFileSys()

        fat32_obj.BPB_FATSz32 = 2048
        fat32_obj.BPB_ExtFlags = 0
        fat32_obj.BPB_FSVer = 0
        fat32_obj.BPB_RootClus = 2
        fat32_obj.BPB_FSInfo = 1
        fat32_obj.BPB_BkBootSec = 6
        fat32_obj.BPB_Reserved = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        fat32_obj.BS_DrvNum = 128
        fat32_obj.BS_Reserved1 = 0
        fat32_obj.BS_BootSig = 41
        fat32_obj.BS_VolID = 3379013315
        fat32_obj.BS_VolLab = 'NO NAME    '
        fat32_obj.BS_FilSysType = 'FAT32   '

        part_two_super_block = b'\x00\x08\x00\x00\x00\x00\x00\x00\x02\x00' \
                               b'\x00\x00\x01\x00\x06\x00\x00\x00\x00\x00' \
                               b'\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00)' \
                               b'\xc3\xa6g\xc9NO NAME    FAT32   '
        fat = FATReader.FATReader("")
        fat.file_system = FATObject.FATFileSys()
        fat._FATReader__parse_fat32_super_block(part_two_super_block)
        assert fat.file_system.__dict__ == fat32_obj.__dict__


    def test_get_next_group_clusters(self):
        fat = FATObject.FATFileSys()
        fat.EOC_LABEL = 0x0FFF
        fat.ERROR_LABEL = 0xFF7
        fat.FAT_TABLE = [1, 2, 3, 4, 5, 4095, 7, 8, 9, 4087]
        fatReader = FATReader.FATReader
        fatReader.file_system = fat

        answer_good_sq = [1, 2, 3, 4, 5]
        answer_error_sq = [7, 8, 9]

        good_sq = fatReader.get_next_group_clusters(fatReader, 0, 8)
        error_sq = fatReader.get_next_group_clusters(fatReader, 6, 8)

        assert good_sq == (answer_good_sq, '')
        assert error_sq == (answer_error_sq, 'Last label is error.')

    def test_convert_byte_sequence_to_list_clusters(self):
        fat = FATObject.FATFileSys()
        fat.set_fat_version("FAT32")
        byte_sequence_fat32 = \
            b'\x10\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04' \
            b'\x00\x00\x00\x05\x00\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x08' \
            b'\x00\x00\x00\x09\x00\x00\x00\x0a\x00\x00\x00\x0b\x50\x00\x00\x0c'
        list_fat32 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        fatReader = FATReader.FATReader
        fatReader.file_system = fat

        answer = fatReader._FATReader__convert_byte_sequence_to_list_clusters(fatReader, byte_sequence_fat32)

        assert answer == list_fat32

    def test_parse_directory(self):
        one_cluster_dir = \
            b"\x54\x45\x53\x54\x46\x49\x7e\x33\x54\x58\x54\x20\x00\x37\x0a\x93\x43\x51\x43\x51\x00\x00\x0a\x93\x43\x51\x21\x05\x00\x10\x00\x00" \
            b"\x54\x45\x53\x54\x46\x49\x7e\x34\x54\x58\x54\x20\x00\x38\x0a\x93\x43\x51\x43\x51\x00\x00\x0a\x93\x43\x51\x22\x05\x00\x10\x00\x00"

        file1 = FATFile()
        file1.DIR_NAME = 'TESTFI~3TXT'
        file1.DIR_Attr = 32
        file1.DIR_NTRes = 0
        file1.DIR_CrtTimeTenth = 55
        file1.DIR_CrtTime = 37642
        file1.DIR_CrtDate = 20803
        file1.DIR_LstAccDate = 20803
        file1.DIR_FstClusHI = 0
        file1.DIR_WrtTime = 37642
        file1.DIR_WrtDate = 20803
        file1.DIR_FstClusLO = 1313
        file1.DIR_FileSize = 4096

        file2 = FATFile()
        file2.DIR_NAME = 'TESTFI~4TXT'
        file2.DIR_Attr = 32
        file2.DIR_NTRes = 0
        file2.DIR_CrtTimeTenth = 56
        file2.DIR_CrtTime = 37642
        file2.DIR_CrtDate = 20803
        file2.DIR_LstAccDate = 20803
        file2.DIR_FstClusHI = 0
        file2.DIR_WrtTime = 37642
        file2.DIR_WrtDate = 20803
        file2.DIR_FstClusLO = 1314
        file2.DIR_FileSize = 4096

        fatReader = FATReader.FATReader

        dir = fatReader.parse_directory(fatReader, one_cluster_dir)

        assert file1 == dir[0]
        assert file2 == dir[1]
