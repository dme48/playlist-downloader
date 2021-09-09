"""Container for the Scrapper class"""
from urllib import request
import re

class Scrapper:
    """Class that extracts songs from a spotify url"""
    def __init__(self, url):
        """
        Accesses and saves the raw html of the spotify url.
            Parameters:
                url (string): Spotify's playlist url.
        """
        self.raw_html = request.urlopen(url).read().decode("utf-8")
        self.songs()

    def songs(self):
        """Extracts song titles from the raw html"""
        pattern = r'(?<="is_playable":true,"name":")[^"]+(?=")'
        titles = re.findall(pattern, self.raw_html)
        return titles
