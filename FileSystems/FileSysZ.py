import abc
import inspect

"""
Мы наследуем метакласс abc (ABCMeta), чтобы избежать конфликтов метаклассов
"""


class CheckFileTypeMeta(abc.ABCMeta):
    """
        Мета класс для проверки переданных типов файлов.
        Проверка на тип '.img'.
    """
    _filenames = set()

    def __new__(cls, name, bases, namespace):
        # сначала выполнить логику abc
        new_cls = super().__new__(cls, name, bases, namespace)

        """
        Нет необходимости запускать проверки для абстрактного класса
        """
        if inspect.isabstract(new_cls):  # 2
            return new_cls

        """
        Проверяем, является _filename строкой
        """
        if not isinstance(namespace['_filename'], str):
            raise TypeError(
                f'_filename attribute of {name} class has to be string!')

        """
        Проверяем, имеет ли _filename расширение .json
        """
        if not namespace['_filename'].endswith('.img'):
            raise ValueError(
                f'_filename attribute of {name} class has to end with ".json"!')

        """
         Проверяем уникальность _filename среди других подклассов.
        """
        if namespace['_filename'] in cls._filenames:
            raise ValueError(
                f'_filename attribute of {name} class is not unique!')

        cls._filenames.add(namespace['_filename'])

        return new_cls