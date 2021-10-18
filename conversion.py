"""Module for converting playlist_downloader's audio files into different formats."""
import os
from pydub import AudioSegment

class ConversionManager:
    """Manages the audio conversions through Converter instances"""
    def __init__(self,
                 audio_paths: list[str],
                 new_extension: str) -> None:
        """Checks the paths and creates the converters"""
        check_paths(audio_paths)
        self.converters = [Converter(path) for path in audio_paths]
        self.new_extension = new_extension

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
    def __init__(self, path: str) -> None:
        """Parses the original name and extension"""
        self.original_path = path
        absolut_path, extension = os.path.splitext(path)
        self.file_no_extension = absolut_path + "/"
        self.original_extension = extension.split(".")[1]

    def convert_to(self, new_extension: str) -> None:
        """Converts the original file to the new_extension format"""
        out_file = f"{self.file_no_extension}.{new_extension}"
        original_audio = AudioSegment.from_file(self.original_path, format=self.original_extension)
        original_audio.export(out_file, format=new_extension)

    def delete_original(self) -> None:
        """Deletes the original file"""
        os.remove(self.original_path)


def check_paths(paths: list[str]) -> None:
    """Calls check_path on every path in the list"""
    for path in paths:
        check_path(path)

def check_path(path: str) -> None:
    """Checks a file exists at path."""
    if not os.path.exists(path):
        raise ValueError(f"File is not found at {path}.")

if __name__ == "__main__":
    PATH = os.getcwd() + "/RandomFile.mp3"
    conv = Converter(PATH)
