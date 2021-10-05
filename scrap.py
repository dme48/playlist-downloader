"""Container for the Scrapper class"""
from urllib import request
from bs4 import BeautifulSoup

class Scrapper:
    """Class that extracts titles and artists from songs in a Spotify's url"""
    ARTIST_ALBUM_DIVIDER = "     •"
    def __init__(self, url, artist):
        """
        Fetches the url's html and wraps it inside a BeautifulSoup instance.
            Parameters:
                url (str): url of the Spotify's playlist
        """
        self.artist = artist
        is_url_valid(url)
        html = request.urlopen(url).read().decode("utf-8")
        self.html_soup = BeautifulSoup(html, "html.parser")

    def get_titles(self, playlist_artists=None):
        """Parses the html to find all the song titles."""
        raw_songs = self.html_soup.find_all("span", "track-name")
        clean_songs = [tag.get_text() for tag in raw_songs]
        if self.artist and playlist_artists:
            is_included = [is_substring_included(a, self.artist) for a in playlist_artists]
            clean_songs = [song for song, included in zip(clean_songs, included) if included]
        return clean_songs

    def get_artists(self):
        """
        Parses the html to find all the artist names. Slightly more complicated than the title
        counterpart, since artist and albums share a string.
        """
        tag_artist_albums = self.html_soup.find_all("span", "artists-albums")
        raw_artist_albums = [tag.get_text() for tag in tag_artist_albums]
        sep = self.ARTIST_ALBUM_DIVIDER
        clean_artists = [raw.split(sep)[0] for raw in raw_artist_albums]
        if self.artist:
            clean_artists = [a for a in clean_artists if is_substring_included(a, self.artist)]
        return clean_artists

    def get_searchstring(self):
        """Gets the artist and title list and combines them in a single list 'title, artist'"""
        titles = self.get_titles()
        artists = self.get_artists()

        return ["{}, {}".format(t, a) for t, a in zip(titles, artists)]

def is_url_valid(url):
    """Checks that the url belongs to a spotify's playlist"""
    prefixes = ["https://open.spotify.com/playlist",
                "open.spotify.com/playlist"]

    prefixes_at_start = [url.startswith(p) for p in prefixes]

    if sum(prefixes_at_start) == 0:
        raise ValueError("Url doesn't belong to a standard spotify's playlist.")

def is_substring_included(mainstring, substring):
    """Checks if substring is included in mainstring"""
    return mainstring.find(substring) >= 0


if __name__ == "__main__":
    SPOTIFY_URL = "https://open.spotify.com/playlist/4oJvONQDLoXaZ7TxkRUz3Q?si=d6eb4d34d95a40f6"
    scrap = Scrapper(SPOTIFY_URL)
    print(scrap.get_searchstring())
