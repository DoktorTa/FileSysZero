from abc import ABCMeta, abstractmethod


class IComSysRead(metaclass=ABCMeta):
    """
        Интерфейс, который определяет методы работы с файловыми системами в режиме чтения
    """
    __pointer_in_file: int = 0
    __pwd: list
    __root: list

    @abstractmethod
    def read(self, dir_now: str, num_in_dir: int, count: int, pointer: int) \
            -> (bytes, int, int):
        """
            Прочесть данный файл.


        :param dir_now:
        :param num_in_dir: Номер элемента в директории.
        :param pointer:
        :return:
        """
        """         
            Первый аргумент: лист элементов.
            Второй: номер в листе.
            Третий: количество блоков на которое необходимо провести чтение с
             нулем в текущей точке указателя.
            Четвертый: текущая позиция указателя на последний прочитанный блок
             для этого номера именно в этом листе элементов.

            Первый аргумент ответа: прочитанные блоки.
            Второй: текущая позиция указателя.
            Третий: номер ошибки, без ошибки == 0.
            
            
        """
        print("read abc method: read block file")

    @abstractmethod
    def cd(self, dir_now: str, num_in_dir: int) -> (list, int):
        """
            Реализует перемещение по директориям в файловой системе в лучших
             традициях командной строки.
            Первый аргумент: лист элементов.
            Второй: номер в листе.

            Первый аргумент ответа: новый лист элементов для номера в старом
             листе в случае если он директория.
            Второй: номер ошибки, без ошибки == 0.
        """
        print("cd abc method: move on directory")

    @property
    @abstractmethod
    def get_root(self) -> list:
        """
            Возвращает содержимое корневого каталога файловой системы.
        """
        print("get root directory")
        return []

    @property
    @abstractmethod
    def get_pwd(self) -> str:
        """
            Возвращает имя текущего каталога.
        """
        print("get pwd directory")
        return ""
