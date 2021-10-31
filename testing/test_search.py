"""Tests for the search module"""
import sys
import pathlib
import unittest

sys.path.append(str(pathlib.Path(".").absolute()))
from search import YTVideo

class TestYTVideo(unittest.TestCase):
    """YTVideo class tests"""

    def test_no_yt_search_matches(self) -> None:
        """Tries to create a YTVid with a searchstring with no associated results."""
        unusual_searchstring = "1281uy 9128u e19n wde1 2e91n82e912e8u12e"
        with self.assertRaises(ValueError):
            YTVideo(unusual_searchstring)


if __name__ == "__main__":
    unittest.main()
