class FileSystemZero:


    def __init__(self):


    def __enter__(self, file_path: str, mode: str, file_systems_names: tuple, all: bool):

        if not self.__check_file_type(file_path):
            raise ValueError("This file is not fs file")



        pass

    def __check_file_type(self, file_path: str) -> bool:
        """
            Проверка на то что тип файла действительно может нести на себе образ жесткого
                диска.

            .ima, .img, .iso
            https://en.wikipedia.org/wiki/IMG_(file_format)
        :param file_path:
        :return:
        """
        if file_path.endswith('.img'):
            return True
        else:
            return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
