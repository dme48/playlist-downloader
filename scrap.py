"""Container for the Scrapper class"""
from urllib import request
import re

def scrap_songs(url):
    """
    Shows the songs in a spotify's url.
        Parameters:
            url (str): spotify's playlist url.
    """
    html = request.urlopen(url).read().decode("utf-8")
    pattern = r'(?<="is_playable":true,"name":")[^"]+(?=")'
    return re.findall(pattern, html)
