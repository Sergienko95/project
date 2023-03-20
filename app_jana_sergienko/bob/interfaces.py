from typing import Protocol
from typing import TypeVar

T_STORAGE_DATA = TypeVar("T_STORAGE_DATA")
T_USECASE_RESULT = TypeVar("T_USECASE_RESULT", covariant=True)


class Storage(Protocol[T_STORAGE_DATA]):
    def load(self) -> T_STORAGE_DATA:
        ...

    def store(self, data: T_STORAGE_DATA) -> None:
        ...

    def reset(self) -> None:
        ...


class UseCase(Protocol[T_USECASE_RESULT]):
    def __call__(self) -> T_USECASE_RESULT:
        ...
