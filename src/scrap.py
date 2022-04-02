"""Container for the Scrapper class"""
import re
from urllib import request
from bs4 import BeautifulSoup


class Scrapper:
    """Class that extracts titles and artists from songs in a Spotify's url"""
    def __init__(self, url: str, artist: str) -> None:
        """
        Fetches the url's html and wraps it inside a BeautifulSoup instance.
            Parameters:
                url (str): url of the Spotify's playlist
        """
        self.artist = artist
        check_url_is_valid(url)
        url = clean_url(url)
        html = request.urlopen(url).read().decode("utf-8")
        raw_text = BeautifulSoup(html, "html.parser").get_text()

        self._song_data = process_raw_text(raw_text)
        self._filter_by_artist(artist)

    def get_titles(self) -> list[str]:
        """Returns the titles from the songs"""
        return [song["title"] for song in self._song_data]

    def get_artists(self, filter_artists: bool = False):
        """Returns the artists of the songs"""
        return [song["artist"] for song in self._song_data]

    def get_searchstring(self) -> list[str]:
        """Gets the artist and title list and combines them in a single list 'title, artist'"""
        return [f'{song["title"]}, {song["artist"]}' for song in self._song_data]

    def _filter_by_artist(self, artist) -> None:
        """Removes the elements in string_list with a corresponding False in self.is_included."""
        if not artist:
            return

        selection = []
        for song in self._song_data:
            if is_substring_included(song["artist"], artist):
                selection.append(song)

        if not selection:
            raise ValueError(
                f'Artist {self.artist} had no matches in the playlist.')

        self._song_data = selection


def check_url_is_valid(url: str) -> None:
    """Checks that the url belongs to a spotify's playlist"""
    prefixes = ["https://open.spotify.com/playlist",
                "open.spotify.com/playlist"]

    prefixes_at_start = [url.startswith(p) for p in prefixes]

    if sum(prefixes_at_start) == 0:
        raise ValueError(
            "Url doesn't belong to a standard spotify's playlist.")


def clean_url(url: str) -> str:
    """Deletes HTTPS request elements from the url"""
    return url.split("\\?")[0]

def is_substring_included(main: str, sub: str) -> bool:
    """Checks if substring is included in mainstring"""
    return main.lower().find(sub.lower()) >= 0

"y.Spotify1 like2 hr 2 min 1C"
START = ".*[0-9]+ min ([0-9]+ sec)?1"
END = "You might also like.*"
TRIMMING_REGEX = re.compile(f".*{START}|{END}.*")


def process_raw_text(text: str) -> list[dict]:
    """Process the raw text from a playlist webpage and returns the artist and song names"""
    trimmed_text = re.sub(TRIMMING_REGEX, "", text)
    raw_songs = re.split("[0-9]+", trimmed_text)
    extracted_data = []

    for song in raw_songs:
        title, artist = re.split("(?<=\S)(?=[A-Z])", song)[0:2]
        extracted_data.append({"title": title, "artist": artist})

    return extracted_data


if __name__ == "__main__":
    SPOTIFY_URL = "https://open.spotify.com/playlist/4oJvONQDLoXaZ7TxkRUz3Q?si=d6eb4d34d95a40f6"
    scrap = Scrapper(SPOTIFY_URL, "Enric")
    print(scrap._song_data)
