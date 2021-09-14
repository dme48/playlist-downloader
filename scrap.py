"""Container for the Scrapper class"""
from urllib import request
import re

def scrap_songs(url):
    """
    Returns the songs in a spotify's url.
        Parameters:
            url (str): spotify's playlist url.
        Returns:
            (string list): List containing the songs, title and artist, from the url 
    """
    html = request.urlopen(url).read().decode("utf-8")
    
    titles = scrap_titles(html)
    artists = scrap_artists(html)

    return ["{}, {}".format(t, a) for t, a in zip(titles, artists)]

def scrap_titles(raw_html):
    """Sraps the titles of the songs from the raw html"""
    title_pattern = r'(?<="is_playable":true,"name":")[^"]+(?=")'
    return re.findall(title_pattern, raw_html)

def scrap_artists(raw_html):
    """Sraps the artists of the songs from the raw html"""
    artist_pattern = r'(?<="name":")[^"]+(?=","type":"artist")'
    duplicated_artists = re.findall(artist_pattern, raw_html)
    return purge_duplicated(duplicated_artists)

def purge_duplicated(duplicated_list):
    """
    Removes duplicated elements from a list WHILE MAINTAINING ORDER. Cannot convert from list to
    set and back to list since it would change the order of apparition in the html.
        Parameters:
            duplicated_list (list): List with (possibly) repeated items
    """
    purged_list = []
    found_elements = set()
    for item in duplicated_list:
        if item in found_elements:
            continue
        found_elements.add(item)
        purged_list.append(item)
    
    return purged_list

if __name__ == "__main__":
    url = "https://open.spotify.com/playlist/4oJvONQDLoXaZ7TxkRUz3Q?si=d6eb4d34d95a40f6"
    print(scrap_songs(url))