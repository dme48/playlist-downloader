"""
Suite of tests for the Playlist Downloader program. Roughly, each class in the program has
one representing class here (f.x. Scrapper has TestScrapper) and each function a function
(Scrapper.get_titles has test_titles).
"""
import unittest
from scrap import Scrapper
from search import YTVideo
from downloads import DownloadManager, Downloader

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
        searchstring = ["{}, {}".format(s, a) for s, a in zip(self.TITLES, self.ARTISTS)]
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

class TestYTVideo(unittest.TestCase):
    """YTVideo class tests"""

    def test_no_yt_search_matches(self) -> None:
        """Tries to create a YTVid with a searchstring with no associated results."""
        unusual_searchstring = "1281uy 9128u e19n wde1 2e91n82e912e8u12e"
        with self.assertRaises(ValueError):
            YTVideo(unusual_searchstring)

class TestDownloader(unittest.TestCase):
    """Downloader class tests"""

    TITLE = "Hey Jude"
    PATH = "Testing"
    CALLBACK = lambda self, x, y, z: None

    def test_multiple_calls_to_donwload(self) -> None:
        """Should raise an error when star_all is called multiple times"""
        downloader = Downloader(self.TITLE, self.PATH, self.CALLBACK)
        with self.assertRaises(ValueError):
            downloader.download()
            downloader.download()

    def class_bad_callback(self, only_one_argument):
        """Callback as a method with the wrong amount of arguments. Does nothing."""
        if not self:
            del only_one_argument

    @staticmethod
    def static_bad_callback(only_one_argument) -> None:
        """Callback as a function with the wrong amount of arguments. Does nothing."""
        del only_one_argument

    def test_bad_callbacks(self) -> None:
        """Tries to create a YTVideo with inappropiate callback functions"""
        with self.assertRaises(ValueError):
            Downloader("Hey Jude", self.PATH, self.class_bad_callback)
            Downloader("Hey Jude", self.PATH, self.static_bad_callback)

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
