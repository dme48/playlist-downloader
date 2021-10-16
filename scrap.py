"""Container for the Scrapper class"""
from urllib import request
from bs4 import BeautifulSoup

class Scrapper:
    """Class that extracts titles and artists from songs in a Spotify's url"""
    ARTIST_ALBUM_DIVIDER = "     •"
    def __init__(self, url: str, artist: str) -> None:
        """
        Fetches the url's html and wraps it inside a BeautifulSoup instance.
            Parameters:
                url (str): url of the Spotify's playlist
        """
        self.artist = artist
        check_url_is_valid(url)
        html = request.urlopen(url).read().decode("utf-8")
        self.html_soup = BeautifulSoup(html, "html.parser")

        if artist:
            self.is_included = [is_substring_included(a, artist) for a in self.get_artists()]
            self.check_match_is_found()
        else:
            self.is_included = None

    def get_titles(self) -> list[str]:
        """Parses the html to find all the song titles."""
        raw_songs = self.html_soup.find_all("span", "track-name")
        clean_songs = [tag.get_text() for tag in raw_songs]
        if self.artist:
            clean_songs = self.filter_by_artist(clean_songs)
        return clean_songs

    def get_artists(self, filter_artists: bool=False):
        """
        Parses the html to find all the artist names. Slightly more complicated than the title
        counterpart, since artist and albums share a string.
        """
        tag_artist_albums = self.html_soup.find_all("span", "artists-albums")
        raw_artist_albums = [tag.get_text() for tag in tag_artist_albums]
        sep = self.ARTIST_ALBUM_DIVIDER
        clean_artists = [raw.split(sep)[0] for raw in raw_artist_albums]
        if filter_artists:
            clean_artists = self.filter_by_artist(clean_artists)
        return clean_artists

    def get_searchstring(self) -> list[str]:
        """Gets the artist and title list and combines them in a single list 'title, artist'"""
        titles = self.get_titles()
        artists = self.get_artists()

        return ["{}, {}".format(t, a) for t, a in zip(titles, artists)]

    def filter_by_artist(self, string_list: list[str]) -> list[str]:
        """Removes the elements in string_list with a corresponding False in self.is_included."""
        return [item for item, included in zip(string_list, self.is_included) if included]

    def check_match_is_found(self) -> None:
        """Checks at least one artist match has been found"""
        if self.is_included is None:
            f_name = self.check_match_is_found.__name__
            raise ValueError(f"{f_name} shouldn't be called if is_included hasn't been created.")
        for included in self.is_included:
            if included:
                return

        raise ValueError(f'Artist {self.artist} had no matches in the playlist.')


def check_url_is_valid(url: str) -> None:
    """Checks that the url belongs to a spotify's playlist"""
    prefixes = ["https://open.spotify.com/playlist",
                "open.spotify.com/playlist"]

    prefixes_at_start = [url.startswith(p) for p in prefixes]

    if sum(prefixes_at_start) == 0:
        raise ValueError("Url doesn't belong to a standard spotify's playlist.")

def is_substring_included(main: str, sub: str) -> bool:
    """Checks if substring is included in mainstring"""
    return main.lower().find(sub.lower) >= 0


if __name__ == "__main__":
    SPOTIFY_URL = "https://open.spotify.com/playlist/4oJvONQDLoXaZ7TxkRUz3Q?si=d6eb4d34d95a40f6"
    scrap = Scrapper(SPOTIFY_URL, None)
    print(scrap.get_searchstring())
