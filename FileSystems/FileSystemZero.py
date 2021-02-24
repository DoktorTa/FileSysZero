import importlib


class FileSystemZero:
    __package_fs_name: dict = {
        "FAT": "FAT321612"
    }

    def __init__(self):


    def __enter__(self, file_path: str, mode: str, file_system_name: str):

        if not self.__check_file_type(file_path):
            raise ValueError("This file is not fs file.")

        self.__import_package(file_system_name)


        pass

    def __import_package(self, name_fs: str) -> None:
        if package_name := self.__package_fs_name.get(name_fs) is not None:
            importlib.import_module(package_name)
        else:
            raise ValueError("File system not recognized.")

    @staticmethod
    def __check_file_type(file_path: str) -> bool:
        """
            Проверка на то что тип файла действительно может нести на себе образ жесткого
                диска.

            .ima, .img, .iso
            https://en.wikipedia.org/wiki/IMG_(file_format)

        :param file_path: путь к файлу
        :return: может ли файл нести на борту фс
        """
        if file_path.endswith('.img'):
            return True
        else:
            return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
