import pytest

from FileSystems.FAT321612 import FATReader
from FileSystems.FAT321612.FATObject import FATFileSys, FATFile, FATLongName, FSInfo
from FileSystems.FAT321612.FATStructParsers import FATStructParsers


class TestFATStructParsers:

    def test_parse_file(self):
        byte_str = b"\x54\x45\x53\x54\x46\x49\x7e\x33\x54\x58\x54\x20\x00\x37\x0a\x93" \
                   b"\x43\x51\x43\x51\x00\x00\x0a\x93\x43\x51\x21\x05\x00\x10\x00\x00"

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

        fat_parser = FATStructParsers()

        dir = fat_parser.parse_file(byte_str)

        assert file1 == dir

    def test_parse_long_name(self):
        byte_str = b'\x41\x74\x00\x33\x00\x32\x00\x00\x00\xFF\xFF\x0F\x00\xE0\xFF\xFF' \
                   b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x00\xFF\xFF\xFF\xFF'

        long_name = FATLongName()
        long_name.LDIR_Ord = 65
        long_name.LDIR_Name1 = 't\x003\x002\x00\x00\x00ÿÿ'
        long_name.LDIR_Attr = 15
        long_name.LDIR_Type = 0
        long_name.LDIR_Chksum = 224
        long_name.LDIR_Name2 = 'ÿÿÿÿÿÿÿÿÿÿÿÿ'
        long_name.LDIR_FstClusLO = 0
        long_name.LDIR_Name3 = 'ÿÿÿÿ'

        fat_parser = FATStructParsers()

        long_file_parse = fat_parser.parse_long_name(byte_str)

        assert long_name.__dict__ == long_file_parse.__dict__

        """
       'LDIR_Ord': 65,                  'LDIR_Ord': 65,
       'LDIR_Name1': 'T32 ÿÿ',          'LDIR_Name1': 't\x003\x002\x00\x00\x00ÿ'
       'LDIR_Attr': 15,                 'LDIR_Attr': 15
       'LDIR_Type': 0,                  'LDIR_Type': 0
       'LDIR_Chksum': 224,              'LDIR_Chksum': 224
       'LDIR_Name2': 'ÿÿÿÿÿÿÿÿÿÿÿÿ',    'LDIR_Name2': 'ÿÿÿÿÿÿÿÿÿÿÿÿ'
       'LDIR_FstClusLO': 0,             'LDIR_FstClusLO': b'\xff'
       'LDIR_Name3': 'ÿÿÿÿ'             'LDIR_Name3': 'ÿÿÿ'
        """

    def test_parse_first_part_super_block(self):
        fat32_obj = FATFileSys()

        fat32_obj.BS_jmpBoot = b'\xeb\x58\x90'
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

        block_fat32 = b'\xeb\x58\x90\x6d\x6b\x66\x73\x2e\x66\x61\x74\x00\x02\x08\x20\x00' \
                      b'\x02\x00\x00\x00\x00\xf8\x00\x00\x3f\x00\xff\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x20\x00'

        fat_parser = FATStructParsers()
        file_sys = FATFileSys()
        file_sys = fat_parser.parse_first_part_super_block(file_sys, block_fat32)

        assert file_sys.__dict__ == fat32_obj.__dict__

    def test_parse_second_part_super_block(self):
        fat32_obj = FATFileSys()

        fat32_obj.BPB_FATSz32 = 2048
        fat32_obj.BPB_ExtFlags = 0
        fat32_obj.BPB_FSVer = 0
        fat32_obj.BPB_RootClus = 2
        fat32_obj.BPB_FSInfo = 1
        fat32_obj.BPB_BkBootSec = 6
        fat32_obj.BPB_Reserved = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        block_fat32 = b'\x00\x08\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x06\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        fat_parser = FATStructParsers()
        file_sys = FATFileSys()
        file_sys = fat_parser.parse_second_part_super_block(file_sys, block_fat32)

        assert file_sys.__dict__ == fat32_obj.__dict__

    def test_parse_third_part_super_block(self):
        fat32_obj = FATFileSys()

        fat32_obj.BS_DrvNum = 128
        fat32_obj.BS_Reserved1 = 0
        fat32_obj.BS_BootSig = 41
        fat32_obj.BS_VolID = 3379013315
        fat32_obj.BS_VolLab = 'NO NAME    '
        fat32_obj.BS_FilSysType = 'FAT32   '

        block_fat32 = b'\x80\x00\x29\xc3\xa6\x67\xc9\x4e\x4f\x20\x4e\x41\x4d\x45\x20\x20' \
                      b'\x20\x20\x46\x41\x54\x33\x32\x20\x20\x20'

        fat_parser = FATStructParsers()
        file_sys = FATFileSys()
        file_sys = fat_parser.parse_third_part_super_block(file_sys, block_fat32)

        assert file_sys.__dict__ == fat32_obj.__dict__

    def test_parse_fs_info_block(self):
        fs_info = FSInfo()
        fs_info.FSI_LeadSig = 0x41615252
        fs_info.FSI_Reserved1 = '\x00' * 480
        fs_info.FSI_StrucSig = 0x61417272
        fs_info.FSI_Free_Count = 0x000189A2
        fs_info.FSI_Nxt_Free = 0x00000017
        fs_info.FSI_Reserved2 = '\x00' * 12
        fs_info.FSI_TrailSig = 0xAA550000

        fs_info_block = b'\x52\x52\x61\x41\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
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
                        b'\x00\x00\x00\x00\x72\x72\x41\x61\xA2\x89\x01\x00\x17\x00\x00\x00' \
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\xAA'

        fat_parser = FATStructParsers()
        fs_info_test = FSInfo()
        fs_info_test = fat_parser.parse_fs_info(fs_info_block, fs_info_test)

        assert fs_info.__dict__ == fs_info_test.__dict__

"""

        # fat32_obj.fat_size = 2048
        # fat32_obj.all_fat_size = 4096
        # 0x41615252

        # block_fat32 = b'\xeb\x58\x90\x6d\x6b\x66\x73\x2e\x66\x61\x74\x00\x02\x08\x20\x00' \
        #               b'\x02\x00\x00\x00\x00\xf8\x00\x00\x3f\x00\xff\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x20\x00\x00\x08\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00' \
        #               b'\x01\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x80\x00\x29\xc3\xa6\x67\xc9\x4e\x4f\x20\x4e\x41\x4d\x45\x20\x20' \
        #               b'\x20\x20\x46\x41\x54\x33\x32\x20\x20\x20\x0e\x1f\xbe\x77\x7c\xac' \
        #               b'\x22\xc0\x74\x0b\x56\xb4\x0e\xbb\x07\x00\xcd\x10\x5e\xeb\xf0\x32' \
        #               b'\xe4\xcd\x16\xcd\x19\xeb\xfe\x54\x68\x69\x73\x20\x69\x73\x20\x6e' \
        #               b'\x6f\x74\x20\x61\x20\x62\x6f\x6f\x74\x61\x62\x6c\x65\x20\x64\x69' \
        #               b'\x73\x6b\x2e\x20\x20\x50\x6c\x65\x61\x73\x65\x20\x69\x6e\x73\x65' \
        #               b'\x72\x74\x20\x61\x20\x62\x6f\x6f\x74\x61\x62\x6c\x65\x20\x66\x6c' \
        #               b'\x6f\x70\x70\x79\x20\x61\x6e\x64\x0d\x0a\x70\x72\x65\x73\x73\x20' \
        #               b'\x61\x6e\x79\x20\x6b\x65\x79\x20\x74\x6f\x20\x74\x72\x79\x20\x61' \
        #               b'\x67\x61\x69\x6e\x20\x2e\x2e\x2e\x20\x0d\x0a\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        #               b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x55\xaa'
"""
