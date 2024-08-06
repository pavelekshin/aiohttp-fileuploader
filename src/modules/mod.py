from datetime import datetime
from pathlib import Path

from src.data.data_folder import get_data_path
from src.exceptions import FileError


class File:
    def __init__(self, filename) -> None:
        self._filename: str = filename
        try:
            name, *_, suffix = self._filename.split(".")
        except ValueError as ex:
            raise FileError from ex
        self._name: str = name
        self._suffix: str = suffix
        self._saved_filename: str | None = None

    def _generate_new_filename(self):
        return (
            f"{self._name}_{datetime.now().strftime("%Y_%m_%d_%H%M%S")}.{self._suffix}"
        )

    @property
    def suffix(self) -> str:
        return self._suffix

    @property
    def saved_filename(self) -> str:
        if not self._saved_filename:
            self._saved_filename = self._generate_new_filename()
        return self._saved_filename

    @property
    def filepath(self) -> Path:
        if not self._saved_filename:
            self._saved_filename = self._generate_new_filename()
        return get_data_path(self._saved_filename)

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}(filename={self._filename})"

    def __str__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(filename={self._filename}, name={self._name}, suffix={self._suffix},"
            f" filepath={self.filepath}, saved_filename={self._saved_filename})"
        )
