"""Tests for the scrap module"""
import sys
import pathlib
import unittest

sys.path.append(str(pathlib.Path(".").absolute()))
from scrap import Scrapper

class TestScrapper(unittest.TestCase):
    """
    Scrapper class tests.
        Attributes:
            URL (str): contains playlist with unusual formats: covers, unicode characters, etc.
            ARTISTS (str list): contains the artist names at the playlist at the URL
            TITLES (str list): contains the titles of the songs in the playlist at the URL
    """

    URL = "https://open.spotify.com/playlist/4oJvONQDLoXaZ7TxkRUz3Q?si=d6eb4d34d95a40f6&nd=1"
    ARTISTS = ["Enric Montefusco",
               "Seu Jorge",
               "Avishai Cohen"]

    TITLES = ["Todo Para Todos",
              "Life On Mars?",
              "Alfonsina y el mar"]

    def test_google_url(self) -> None:
        """Tries to create a Scrapper instance with a google url, which should raise an exception"""
        invalid_url = "https://www.google.com/"
        with self.assertRaises(ValueError):
            Scrapper(invalid_url, None)

    def test_artist_spotify_url(self) -> None:
        """
        Tries to create a Scrapper instance with a spotify url belonging to an artist. Should
        raise an exception.
        """
        invalid_url = "https://open.spotify.com/artist/3X3vk6cQHF0ViZeiXFLhR7"
        with self.assertRaises(ValueError):
            Scrapper(invalid_url, None)

    def test_artists(self) -> None:
        """Checks the artists from the playlist are as expected."""
        fetched_artists = Scrapper(self.URL, None).get_artists()
        self.assertEqual(self.ARTISTS, fetched_artists)

    def test_titles(self) -> None:
        """Checks the titles from the playlist are as expected."""
        fetched_titles = Scrapper(self.URL, None).get_titles()
        self.assertEqual(self.TITLES, fetched_titles)

    def test_searchstring(self) -> None:
        """Checks the titles from the playlist are as expected."""
        searchstring = ["{}, {}".format(s, a)
                        for s, a in zip(self.TITLES, self.ARTISTS)]
        fetched_searchstring = Scrapper(self.URL, None).get_searchstring()
        self.assertEqual(searchstring, fetched_searchstring)

    def test_artist_filtering(self) -> None:
        """Checks that a correctly spelled artist works as a filter"""
        artist = self.ARTISTS[0]
        filtered_artists = Scrapper(self.URL, artist).get_artists()
        self.assertEqual(artist, filtered_artists[0])

    def test_artists_lowercase_filtering(self) -> None:
        """Checks that a lowercase version of an artist's name works as a filter"""
        artist = self.ARTISTS[0]
        filtered_artists = Scrapper(self.URL, artist.lower()).get_artists()
        self.assertEqual(artist, filtered_artists[0])

    def test_artist_not_found(self) -> None:
        """Expects an error to be raised when the artist is not found on the list"""
        non_present_artist = "Enrique Montefusco"
        with self.assertRaises(ValueError):
            Scrapper(self.URL, non_present_artist)


if __name__ == "__main__":
    unittest.main()
