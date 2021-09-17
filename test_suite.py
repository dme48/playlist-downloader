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
    ARTISTS = ["Enric Montefusco",
               "Seu Jorge",
               "Avishai Cohen"]

    TITLES = ["Todo Para Todos",
              "Life On Mars?",
              "Alfonsina y el mar"]

    def test_artists(self):
        """Checks the artists from the playlist are as expected."""
        fetched_artists = Scrapper(self.URL).get_artists()
        self.assertEqual(self.ARTISTS, fetched_artists)

    def test_titles(self):
        """Checks the titles from the playlist are as expected."""
        fetched_titles = Scrapper(self.URL).get_titles()
        self.assertEqual(self.TITLES, fetched_titles)

    def test_searchstring(self):
        """Checks the titles from the playlist are as expected."""
        searchstring = ["{}, {}".format(s, a) for s, a in zip(self.TITLES, self.ARTISTS)]
        fetched_searchstring = Scrapper(self.URL).get_searchstring()
        self.assertEqual(searchstring, fetched_searchstring)


if __name__ == "__main__":
    unittest.main()
