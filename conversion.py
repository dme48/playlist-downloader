"""Module for converting playlist_downloader's audio files into different formats."""
import os
from pydub import AudioSegment
from pathlib import Path


class ConversionManager:
    """Manages the audio conversions through Converter instances"""

    def __init__(self, audio_paths: list[Path]) -> None:
        """Creates the converters"""
        self.converters = [Converter(path) for path in audio_paths]

    def convert_all(self, new_extension) -> None:
        """Starts the conversion on all files."""
        for converter in self.converters:
            converter.convert_to(new_extension)

    def delete_originals(self) -> None:
        """Deletes all the original files"""
        for converter in self.converters:
            converter.delete_original()


class Converter:
    """Interface to convert the format of an audio file"""

    def __init__(self, path: Path) -> None:
        """Parses the original name and extension"""
        check_path(path)
        self.original_path = path
        self.filename, extension = os.path.splitext(path)
        self.original_extension = extension.split(".")[1]

    def convert_to(self, new_extension: str) -> None:
        """Converts the original file to the new_extension format"""
        new_file = Path(f"{self.filename}.{new_extension}")
        if new_file.exists():
            print("Warning: The file with the new extension already exists.")
        original_audio = AudioSegment.from_file(
            self.original_path,
            format=self.original_extension)
        original_audio.export(new_file, format=new_extension)

    def delete_original(self) -> None:
        """Deletes the original file"""
        # We check in case path has been already deleted
        check_path(self.original_path)
        self.original_path.unlink()


def check_path(path: Path) -> None:
    """Checks a file exists at path."""
    if not path.exists():
        raise ValueError(f"File is not found at {path}.")


if __name__ == "__main__":
    PATH = os.getcwd() + "/RandomFile.mp3"
    conv = Converter(PATH)
