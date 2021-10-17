"""Module for converting playlist_downloader's audio files into different formats."""
import os
from pydub import AudioSegment

class ConversionManager:
    """Manages the audio conversions through Converter instances"""
    def __init__(self,
                 audio_paths: list[str],
                 new_extension: str,
                 delete_originals: bool=False) -> None:
        """Checks the paths and creates the converters"""
        check_paths(audio_paths)
        self.converters = [Converter(path) for path in audio_paths]
        # TODO start conversors
        # TODO delete originals if specified

    def convert_all(self, new_extension) -> None:
        """Starts the conversion on all files."""
        # TODO implement

    def delete_originals(self) -> None:
        """Deletes all the original files"""
        for converter in self.converters:
            converter.delete_original()

def check_paths(paths: list[str]) -> None:
    """Checks the files that appear in paths exist"""
    # TODO implement

class Converter:
    """Interface to convert the format of an audio file"""
    def __init__(self, path: str) -> None:
        """Parses the original name and extension"""
        self.original_path = path
        (absolut_path, extension) = os.path.splitext(path)
        self.original_extension = extension.split(".")[1]
        split_path = absolut_path.split("/")
        self.filename = split_path[-1]
        self.containing_folder = "/".join(split_path[:-1])

    def convert_to(self, new_extension: str) -> None:
        """Converts the original file to the new_extension format"""
        # TODO implement

    def delete_original(self) -> None:
        """Deletes the original file"""
        # TODO implement

if __name__ == "__main__":
    PATH = os.getcwd() + "/RandomFile.mp3"
    conv = Converter(PATH)
