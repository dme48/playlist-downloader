"""Container for the Scrapper class"""
from urllib import request
from bs4 import BeautifulSoup

class Scrapper:
    """Class that extracts titles and artists from songs in a Spotify's url"""
    ARTIST_ALBUM_DIVIDER = "     •"
    def __init__(self, url):
        """
        Fetches the url's html and wraps it inside a BeautifulSoup instance.
            Parameters:
                url (str): url of the Spotify's playlist
        """
        html = request.urlopen(url).read().decode("utf-8")
        self.html_soup = BeautifulSoup(html, "html.parser")

    def get_titles(self):
        """Parses the html to find all the song titles"""
        raw_songs = self.html_soup.find_all("span", "track-name")
        return [tag.get_text() for tag in raw_songs]

    def get_artists(self):
        """
        Parses the html to find all the artist names. Slightly more complicated than the title
        counterpart, since artist and albums share a string."""
        tag_artist_albums = self.html_soup.find_all("span", "artists-albums")
        raw_artist_albums = [tag.get_text() for tag in tag_artist_albums]
        sep = self.ARTIST_ALBUM_DIVIDER
        return [raw.split(sep)[0] for raw in raw_artist_albums]

    def get_searchstring(self):
        """Gets the artist and title list and combines them in a single list 'title, artist'"""
        titles = self.get_titles()
        artists = self.get_artists()

        return ["{}, {}".format(t, a) for t, a in zip(titles, artists)]


if __name__ == "__main__":
    SPOTIFY_URL = "https://open.spotify.com/playlist/4oJvONQDLoXaZ7TxkRUz3Q?si=d6eb4d34d95a40f6"
    scrap = Scrapper(SPOTIFY_URL)
    print(scrap.get_searchstring())
