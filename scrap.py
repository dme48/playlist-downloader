"""Container for the Scrapper class"""
from urllib import request
import re

def scrap_songs(url):
    """
    Shows the songs in a spotify's url.
        Parameters:
            url (str): spotify's playlist url.
    """
    title_pattern = r'(?<="is_playable":true,"name":")[^"]+(?=")'
    song_titles = re.findall(title_pattern, html)

    artist_pattern = r'(?<="name":")[^"]+(?=","type":"artist")'
    artist_names = re.findall(artist_pattern, html)
    artist_names = purge_duplicated(artist_names)

    return song_titles

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
    html = request.urlopen(url).read().decode("utf-8")

    title_pattern = r'(?<="is_playable":true,"name":")[^"]+(?=")'
    song_titles = re.findall(title_pattern, html)

    artist_pattern = r'(?<="name":")[^"]+(?=","type":"artist")'
    artist_names = re.findall(artist_pattern, html)
    print(song_titles)
    print(purge_duplicated(artist_names))