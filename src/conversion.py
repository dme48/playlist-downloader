"""Module for converting playlist_downloader's audio files into different formats."""
import os
from pathlib import Path
from pydub import AudioSegment
from pydub.exceptions import CouldntEncodeError


class ConversionManager:
    """Manages the audio conversions through Converter instances"""

    def __init__(self, audio_paths: list[Path]) -> None:
        """Creates the converters"""
        check_paths_are_valid(audio_paths)
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

    VALID_FORMATS = ["mp3", "mp4", "ogg"]

    def __init__(self, path: Path) -> None:
        """Parses the original name and extension"""
        check_file_exists(path)
        self.original_path = path
        self.filename, extension = os.path.splitext(path)
        self.original_extension = extension.split(".")[1]

    def convert_to(self, new_extension: str) -> None:
        """Converts the original file to the new_extension format"""
        if new_extension not in Converter.VALID_FORMATS:
            raise ValueError(f"Conversion to format '{new_extension}' is not supported.")
        new_file = Path(f"{self.filename}.{new_extension}")
        original_audio = AudioSegment.from_file(
            self.original_path,
            format=self.original_extension)
        original_audio.export(new_file, format=new_extension)

    def delete_original(self) -> None:
        """Deletes the original file"""
        # We check in case path has been already deleted
        check_file_exists(self.original_path)
        self.original_path.unlink()

def check_paths_are_valid(paths: list[Path]) -> None:
    """Checks that the list of paths is not empty or None and that they're instances of Path"""
    if paths == None:
        raise TypeError("Variable 'audio_paths' can't be None")
    if not paths:
        raise ValueError("The list of audio files to be converted was empty")
    for path in paths:
        if not isinstance(path, Path):
            raise TypeError("Provided paths must be of type pathlib.Path")

def check_file_exists(path: Path) -> None:
    """Checks a file exists at path."""
    if not path.exists():
        raise ValueError(f"File is not found at {path}.")


if __name__ == "__main__":
    PATH = os.getcwd() + "/RandomFile.mp3"
    conv = Converter(PATH)
