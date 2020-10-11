import unittest
import logging
import argparse

from Test.Tests.FAT321612 import TestFATReader


class TestConfiguration:
    """Запускает тестовые группы а так же настраивает при этом логгирование"""
    __fs_tests_fat = [TestFATReader.TestFATReader('test_choice_fs'),
                      TestFATReader.TestFATReader('test_calculation_fat_size'),
                      TestFATReader.TestFATReader('test_calculation_total_sector'),
                      TestFATReader.TestFATReader('test_calculation_all_fat_size'),
                      TestFATReader.TestFATReader('test_calculation_number_sectors_root'),
                      TestFATReader.TestFATReader('test_calculation_data_sector'),
                      TestFATReader.TestFATReader('test_calculation_count_of_clusters'),
                      TestFATReader.TestFATReader('test_calculation_num_fat_and_root_dir_sector'),
                      TestFATReader.TestFATReader('test_parse_super_block'),
                      TestFATReader.TestFATReader('test_parse_fat32_super_block')]
    __all_tests = __fs_tests_fat
    __chosen_fs = {"FAT": __fs_tests_fat}

    def __init__(self, log_lvl):
        self.__logging_configuration(log_lvl)

    def configuration_all_tests(self):
        all_tests_group = unittest.TestSuite()
        all_tests_group.addTests(self.__all_tests)
        # all_tests_group.addTests(self.__all_tests)
        self.__run_test(all_tests_group)

    def configuration_test_chosen_fs(self, fs_chosen: str):
        tests_group = unittest.TestSuite()
        tests_group.addTests(self.__chosen_fs.get(fs_chosen))
        self.__run_test(tests_group)

    def __logging_configuration(self, level_logging=logging.CRITICAL):
        format_msg = '%(asctime)s %(name)s %(levelname)s:%(message)s'
        logging.basicConfig(level=level_logging, format=format_msg)
        logging.StreamHandler.emit = self.add_coloring_to_emit_ansi(
            logging.StreamHandler.emit)

    @staticmethod
    def add_coloring_to_emit_ansi(fn):
        def new(*args):
            levelno = args[1].levelno
            if levelno >= 50:
                color = '\x1b[41m'  # red
            elif levelno >= 40:
                color = '\x1b[31m'  # red
            elif levelno >= 30:
                color = '\x1b[33m'  # yellow
            elif levelno >= 20:
                color = '\x1b[32m'  # green
            elif levelno >= 10:
                color = '\x1b[34m'  # blue
            else:
                color = '\x1b[0m'  # normal
            args[1].msg = color + args[1].msg + '\x1b[0m'  # normal
            return fn(*args)
        return new

    @staticmethod
    def __run_test(test_group: unittest.TestSuite):
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(test_group)


def main():
    fs_type, log_lvl = arguments()
    logging_lvl = [logging.DEBUG, logging.CRITICAL, logging.INFO]
    test_conf = TestConfiguration(logging_lvl[log_lvl])
    if fs_type == "a":
        test_conf.configuration_all_tests()
    else:
        test_conf.configuration_test_chosen_fs(fs_type)


def arguments() -> (str, int):
    parser = argparse.ArgumentParser(description='Test module script')

    parser.add_argument('-f', action="store", dest="fs_type", default="a",
                        type=str, nargs=1,
                        help="a - тестирование всех модулей,\n"
                             "FAT - тестирование FAT321612.")

    parser.add_argument('-l', action="store", dest="log_lvl", default=[1],
                        type=int, nargs=1,
                        help="Logging level:\n"
                             "0 - DEBUG,\n"
                             "1 - CRITICAL,\n"
                             "2 - INFO.")

    args = parser.parse_args()
    fs_type = args.fs_type
    log_lvl = args.log_lvl[0]
    return fs_type, log_lvl


if __name__ == '__main__':
    main()
