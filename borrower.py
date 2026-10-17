from abc import ABC, abstractmethod

class IBorrower(ABC):
    @property
    @abstractmethod
    def borrower_id(self) -> str:
        pass

    @property
    @abstractmethod
    def borrower_name(self) -> str:
        pass

    @abstractmethod
    def get_maximum_devices(self) -> int:
        pass

class Lecturer:

    def __init__(
        self,
        borrower_id: str,
        borrower_name: str
    ):
        self._borrower_id = borrower_id
        self._borrower_name = borrower_name

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    def borrower_name(self) -> str:
        return self._borrower_name

    def get_maximum_devices(self) -> int:
        return 3

class TeachingAssistant:

    def __init__(
        self,
        borrower_id: str,
        borrower_name: str
    ):
        self._borrower_id = borrower_id
        self._borrower_name = borrower_name

    @property
    def borrower_id(self) -> str:
        return self._borrower_id

    def borrower_name(self) -> str:
        return self._borrower_name

    def get_maximum_devices(self) -> int:
        return 2
