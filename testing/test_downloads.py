"""Tests for the downloads module"""
import sys
import pathlib
import unittest

sys.path.append(str(pathlib.Path(".").absolute()))
from downloads import DownloadManager, Downloader

class TestDownloader(unittest.TestCase):
    """Downloader class tests"""

    TITLE = "Hey Jude"
    PATH = pathlib.Path("Testing")
    PARENT = DownloadManager([TITLE], PATH)

    def test_multiple_calls_to_donwload(self) -> None:
        """Should raise an error when star_all is called multiple times"""
        downloader = Downloader(self.TITLE, self.PARENT)
        with self.assertRaises(ValueError):
            downloader.download()
            downloader.download()


class TestDownloadManager(unittest.TestCase):
    """DownloadManager class tests"""
    PATH = "Testing"
    SEARCHSTRINGS = ["Hey Jude", "Purple Rain", "Stairway to Heaven"]

    def test_empty_songlist(self) -> None:
        """Should raise an error when the playlist is empty"""
        with self.assertRaises(TypeError):
            DownloadManager([], self.PATH)

    def test_wrong_type_songlist(self) -> None:
        """Should raise an error when some of the elements in the list are not strings"""
        bad_songlist = self.SEARCHSTRINGS.copy()
        bad_songlist[0] = 1.3
        with self.assertRaises(TypeError):
            DownloadManager(bad_songlist, self.PATH)




if __name__ == "__main__":
    unittest.main()
