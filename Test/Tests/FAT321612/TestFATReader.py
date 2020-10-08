import unittest
from FAT321612 import FATReader


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


if __name__ == '__main__':
    unittest.main()
