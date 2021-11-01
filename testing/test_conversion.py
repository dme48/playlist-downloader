"""Tests for the conversion module"""
import sys
import shutil
import pathlib
import unittest

sys.path.append(str(pathlib.Path(".").absolute()))
from conversion import ConversionManager, Converter


class TestConversionManager(unittest.TestCase):
    """Tests ConversionManager from conversion module"""
    def test_invalid_filelists(self) -> None:
        """Tries to create a ConversionManager with an empty list"""
        with self.assertRaises(ValueError):
            ConversionManager([])
        with self.assertRaises(TypeError):
            ConversionManager(None)
        with self.assertRaises(TypeError):
            ConversionManager(["path1", "path2"])

class TestConverter(unittest.TestCase):
    """Tests Converter from conversion module"""
    TEST_SONG_PATH = pathlib.Path("Testing/The Beatles - Hey Jude.mp4")
    copy_count = 0

    def copy_testing_song(self) -> pathlib.Path:
        """
        Copies TEST_SONG_PATH so tests can use the second without interfering.
        Returns the path of the copy.
        """
        copy_path = pathlib.Path(f"Testing/testing_copy_{self.copy_count}.mp3")
        self.copy_count += 1
        shutil.copy(self.TEST_SONG_PATH, copy_path)
        return copy_path

    def test_nonexistent_file(self) -> None:
        """Tries to create an instance with a path not containing a file."""
        nonexistent_file = pathlib.Path(
            "Testing/The Rolling Stones - Hey Jude.mp4")
        with self.assertRaises(ValueError):
            Converter(nonexistent_file)

    def test_delete_original(self) -> None:
        """Tests that original file is deleted by delete_original"""
        copy_path = self.copy_testing_song()
        self.assertTrue(copy_path.exists())
        conv = Converter(copy_path)
        conv.delete_original()
        self.assertFalse(copy_path.exists())

    def test_double_delete(self) -> None:
        """Tries to delete original files twice"""
        copy_path = self.copy_testing_song()
        converter = Converter(copy_path)
        converter.delete_original()
        with self.assertRaises(ValueError):
            converter.delete_original()

    def test_invalid_format(self) -> None:
        """Tries to convert to an invalid format"""
        converter = Converter(self.TEST_SONG_PATH)
        with self.assertRaises(ValueError):
            converter.convert_to("exe")


if __name__ == "__main__":
    unittest.main()
