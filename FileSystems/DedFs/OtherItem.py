from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class IntValidator(Validator):
    __max_value: int = 0
    __min_value: int = 0

    def __init__(self, min_value: int, max_value: int):
        self.__max_value = max_value
        self.__min_value = min_value

    def validate(self, value):

        if not isinstance(value, int):
            raise TypeError(f'Type only int, you type is {type(value)}')
        else:
            if value > self.__max_value:
                raise ValueError(f'The transferred value is too large, the value is limited from above {self.__max_value}.')
            elif self.__min_value > value:
                raise ValueError(f'The transmitted value is small, the value is limited from not below {self.__min_value}.')

class StrValidator(Validator):
    def __init__(self, ):

    def validate(self, value):