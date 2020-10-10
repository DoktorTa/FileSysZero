import unittest
from FAT321612 import FATReader, FATObject


class TestFATReader(unittest.TestCase):
    def test_choice_fs(self):
        fat = FATReader.FATReader()
        self.assertEqual(fat._FATReader__choice_fs(65526), "FAT32")
        self.assertEqual(fat._FATReader__choice_fs(101200), "FAT32")
        self.assertEqual(fat._FATReader__choice_fs(65524), "FAT16")
        self.assertEqual(fat._FATReader__choice_fs(4085), "FAT16")
        self.assertEqual(fat._FATReader__choice_fs(4084), "FAT12")
        self.assertEqual(fat._FATReader__choice_fs(257), "FAT12")

    def test_calculation_fat_size(self):
        fat = FATReader.FATReader()
        self.assertEqual(fat._FATReader__calculation_fat_size(0, 2), 2)
        self.assertEqual(fat._FATReader__calculation_fat_size(2, 0), 2)

    def test_calculation_total_sector(self):
        fat = FATReader.FATReader()
        self.assertEqual(fat._FATReader__calculation_total_sector(0, 2), 2)
        self.assertEqual(fat._FATReader__calculation_total_sector(2, 0), 2)

    def test_calculation_all_fat_size(self):
        fat = FATReader.FATReader()
        self.assertEqual(fat._FATReader__calculation_all_fat_size(2, 484600),
                         969200)

    def test_calculation_number_sectors_root(self):
        fat = FATReader.FATReader()
        self.assertEqual(
            fat._FATReader__calculation_number_sectors_root(512, 512), 32)
        self.assertEqual(
            fat._FATReader__calculation_number_sectors_root(0, 512), 0)

    def test_calculation_data_sector(self):
        fat = FATReader.FATReader()
        self.assertEqual(
            fat._FATReader__calculation_data_sector(1000, 8, 12, 2), 978)

    def test_calculation_count_of_clusters(self):
        fat = FATReader.FATReader()
        self.assertEqual(
            fat._FATReader__calculation_count_of_clusters(64, 8), 8)

    def test_calculation_num_fat_and_root_dir_sector(self):
        fat32_obj = FATObject.FATFileSys()
        fat32_obj.BPB_RootEntCnt = 0
        fat32_obj.BPB_BytsPerSec = 512
        fat32_obj.BPB_TotSec16 = 0
        fat32_obj.BPB_TotSec32 = 2097152
        fat32_obj.BPB_FATSz16 = 0
        fat32_obj.BPB_FATSz32 = 32768
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
            self.assertEqual(fat.file_system.FAT_VERSION, fat_values[i])


if __name__ == '__main__':
    unittest.main()
