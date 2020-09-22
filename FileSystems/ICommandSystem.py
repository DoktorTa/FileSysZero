from abc import ABCMeta, abstractmethod


class IFSWork(metaclass=ABCMeta):
    """
        Интерфейс который определяет методы работы с файловыми системами

        Metods:
        ~~~~~~~~~~~~~~~~~~
            **read**
            **cd**
            **get_root**
            **get_pwd**
    """

    @abstractmethod
    def read(self, dir_now: str, num_in_dir: int, count: int, pointer: int) \
            -> (bytes, int, int):
        """
            Прочесть данный блок||кластер файловой системы.
            Первый аргумент: лист элементов.
            Второй: номер в листе.
            Третий: количество блоков на котороенеобходимо провести чтение с
             нулем в текушей точке указателя.
            Четвертый: текущая позиция указателя на последний прочинанный блок
             для этого номера именно в этом листе элементов.

            Первый аргумент ответа: прочитаные блоки.
            Второй: текушая позиция указателя.
            Третий: номер ощибки, без ощибки == 0.
        """
        print("read abc metod: read block file")

    @abstractmethod
    def cd(self, dir_now: str, num_in_dir: int) -> (list, int):
        """
            Реализует перемешение по директориям в файловой системе в лучших
             традициях командной строки.
            Первый аргумент: лист элементов.
            Второй: номер в листе.

            Первый аргумент ответа: новый лист элементов для номера в старом
             листе в случае если он директория.
            Второй: номер ощибки, без ощибки == 0.
        """
        print("cd abc metod: move on directory")

    @property
    @abstractmethod
    def get_root(self) -> list:
        """
            Возврашает содержимое корневого котолога файловой системы.
        """
        print("get root directory")
        return []

    @property
    @abstractmethod
    def get_pwd(self) -> str:
        """
            Возврашает имя текушего каталога.
        """
        print("get pwd directory")
        return ""
