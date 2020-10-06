import unittest
import logging
import argparse

from Test.Tests.FAT321612 import TestFATReader


class TestConfiguration:
    """Запускает тестовые группы а так же настраивает при этом логгирование"""
    __fs_tests_fat = [TestFATReader.TestFATReader('test_choice_fs')]
    __all_tests = __fs_tests_fat
    __chosen_fs = {"FAT": __fs_tests_fat}

    def __init__(self, log_lvl):
        self.__logging_configuration(log_lvl)

    def configuration_all_tests(self):
        all_tests_group = unittest.TestSuite()
        all_tests_group.addTests(self.__all_tests)
        self.__run_test(all_tests_group)

    def configuration_test_chosen_fs(self, fs_chosen: str):
        tests_group = unittest.TestSuite()
        tests_group.addTests(self.__chosen_fs.get(fs_chosen))
        self.__run_test(tests_group)

    @staticmethod
    def __logging_configuration(level_logging=logging.CRITICAL):
        logging.basicConfig(level=level_logging)

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

    parser.add_argument('-l', action="store", dest="log_lvl", default=1,
                        type=int, nargs=1,
                        help="Logging level:\n"
                             "0 - DEBUG,\n"
                             "1 - CRITICAL,\n"
                             "2 - INFO.")

    args = parser.parse_args()
    fs_type = args.fs_type
    log_lvl = args.log_lvl
    return fs_type, log_lvl


if __name__ == '__main__':
    main()
