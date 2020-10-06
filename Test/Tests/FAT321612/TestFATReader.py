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


if __name__ == '__main__':
    unittest.main()
