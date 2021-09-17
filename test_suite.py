"""
Suite of tests for the Playlist Downloader program. Roughly, each class in the program has
one representing class here (f.x. Scrapper has TestScrapper) and each function a function
(Scrapper.get_titles has test_titles).
"""
import unittest
from scrap import Scrapper

class TestScrapper(unittest.TestCase):
    """
    Scrapper class tests.
        Attributes:
            URL (str): contains playlist with unusual formats: covers, unicode characters, etc.
    """

    URL = "https://open.spotify.com/playlist/4oJvONQDLoXaZ7TxkRUz3Q?si=d6eb4d34d95a40f6&nd=1"

    def test_artists(self):
        """Checks fetched artists are the desired artists."""
        expected_artists = ["Enric Montefusco",
                            "Seu Jorge",
                            "Avishai Cohen"]
        fetched_artists = Scrapper(self.URL).get_artists()
        self.assertEqual(expected_artists, fetched_artists)


if __name__ == "__main__":
    unittest.main()
