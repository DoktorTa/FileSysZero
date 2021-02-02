import pytest
from pytest_mock import mocker

from FAT321612 import FATReader, FATObject


class TestFATReader:

    @pytest.mark.parametrize("count_cluster, name_fs",
                             [(65526, "FAT32"), (101200, "FAT32"),
                              (65524, "FAT16"), (4085, "FAT16"),
                              (4084, "FAT12"), (257, "FAT12")])
    def test_choice_fs(self, count_cluster: int, name_fs: str):
        fat = FATReader.FATReader()
        assert fat._FATReader__choice_fs(count_cluster) == name_fs

    @pytest.mark.parametrize("fat_sz16, fat_sz32, fat_size", [(0, 2, 2), (2, 0, 2)])
    def test_calculation_fat_size(self, fat_sz16: int, fat_sz32: int, fat_size: int):
        fat = FATReader.FATReader()
        assert fat._FATReader__calculation_fat_size(fat_sz16, fat_sz32) == fat_size

    @pytest.mark.parametrize("BPB_TotSec16, BPB_TotSec32, count_sec", [(0, 2, 2), (2, 0, 2)])
    def test_calculation_total_sector(self, BPB_TotSec16: int,
                                      BPB_TotSec32: int, count_sec: int):
        fat = FATReader.FATReader()
        assert fat._FATReader__calculation_total_sector(BPB_TotSec16, BPB_TotSec32) == count_sec

    def test_calculation_all_fat_size(self):
        fat = FATReader.FATReader()
        assert fat._FATReader__calculation_all_fat_size(2, 484600) == 969200

    @pytest.mark.parametrize("BPB_RootEntCnt, BPB_BytsPerSec, root_sec",
                             [(512, 512, 32), (0, 512, 0)])
    def test_calculation_number_sectors_root(self, BPB_RootEntCnt: int,
                                             BPB_BytsPerSec: int, root_sec: int):
        fat = FATReader.FATReader()
        assert fat._FATReader__calculation_number_sectors_root(BPB_RootEntCnt, BPB_BytsPerSec) == root_sec

    def test_calculation_data_sector(self):
        fat = FATReader.FATReader()
        assert fat._FATReader__calculation_data_sector(1000, 8, 12, 2) == 978

    def test_calculation_count_of_clusters(self):
        fat = FATReader.FATReader()
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

            fat = FATReader.FATReader()
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
        fat32_obj.BPB_Reserved = \
            '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

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
        fat = FATReader.FATReader()
        fat.file_system = FATObject.FATFileSys()
        fat._FATReader__parse_fat32_super_block(part_two_super_block)
        assert fat.file_system.__dict__ == fat32_obj.__dict__

    def test_parse_super_block_fat32(self, mocker):
        fat32_obj = FATObject.FATFileSys()

        fat32_obj.FAT_VERSION = "FAT32"
        fat32_obj.BS_jmpBoot = 36952
        fat32_obj.BS_OEMName = 'mkfs.fat'
        fat32_obj.BPB_BytsPerSec = 512
        fat32_obj.BPB_SecPerClus = 8
        fat32_obj.BPB_RsvdSecCnt = 32
        fat32_obj.BPB_NumFATs = 2
        fat32_obj.BPB_RootEntCnt = 0
        fat32_obj.BPB_TotSec16 = 0
        fat32_obj.BPB_Media = 248
        fat32_obj.BPB_FATSz16 = 0
        fat32_obj.BPB_SecPerTrk = 63
        fat32_obj.BPB_NumHeads = 255
        fat32_obj.BPB_HiddSec = 0
        fat32_obj.BPB_TotSec32 = 2097152

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

        fat32_obj.fat_size = 2048
        fat32_obj.all_fat_size = 4096

        block_fat32 = b'\xeb\x58\x90\x6d\x6b\x66\x73\x2e\x66\x61\x74\x00\x02\x08\x20\x00' \
                      b'\x02\x00\x00\x00\x00\xf8\x00\x00\x3f\x00\xff\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x20\x00\x00\x08\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00' \
                      b'\x01\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x80\x00\x29\xc3\xa6\x67\xc9\x4e\x4f\x20\x4e\x41\x4d\x45\x20\x20' \
                      b'\x20\x20\x46\x41\x54\x33\x32\x20\x20\x20\x0e\x1f\xbe\x77\x7c\xac' \
                      b'\x22\xc0\x74\x0b\x56\xb4\x0e\xbb\x07\x00\xcd\x10\x5e\xeb\xf0\x32' \
                      b'\xe4\xcd\x16\xcd\x19\xeb\xfe\x54\x68\x69\x73\x20\x69\x73\x20\x6e' \
                      b'\x6f\x74\x20\x61\x20\x62\x6f\x6f\x74\x61\x62\x6c\x65\x20\x64\x69' \
                      b'\x73\x6b\x2e\x20\x20\x50\x6c\x65\x61\x73\x65\x20\x69\x6e\x73\x65' \
                      b'\x72\x74\x20\x61\x20\x62\x6f\x6f\x74\x61\x62\x6c\x65\x20\x66\x6c' \
                      b'\x6f\x70\x70\x79\x20\x61\x6e\x64\x0d\x0a\x70\x72\x65\x73\x73\x20' \
                      b'\x61\x6e\x79\x20\x6b\x65\x79\x20\x74\x6f\x20\x74\x72\x79\x20\x61' \
                      b'\x67\x61\x69\x6e\x20\x2e\x2e\x2e\x20\x0d\x0a\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\xaa'

        mocker.patch('FAT321612.FATReader.FATReader._FATReader__read_block', return_value=block_fat32)

        fat = FATReader.FATReader()
        fat._FATReader__parse_super_block()

        assert fat.file_system.__dict__ == fat32_obj.__dict__


