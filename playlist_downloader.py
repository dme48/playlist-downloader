#!/usr/bin/python
"""Searches and downloads a playlist"""
import sys
from scrap import Scrapper
from downloads import DownloadManager


def main(url: str,
         artist: str,
         path: str) -> None:
    """
    Downloads the songs inside a playlist.
    Parameters:
        url (str): url link to a Spotify's playlist. Can be obtained inside spotify's desktop
            app by right-clicking --> Share --> Copy Spotify URL.
        selected_artist (str): if different than None, only the songs with an artist containing
            selected_artist will be downloaded (case insensitive)
        path (str): Folder to download the songs into. If it doesn't exist it will be created.
    """
    if not url:
        raise TypeError("A valid url must be provided.")
    path = path if path else "Songs/"

    playlist_titles = Scrapper(url, artist).get_searchstring()

    down_manager = DownloadManager(playlist_titles, path)
    down_manager.start_all()


if __name__ == "__main__":
    if NUM_ARGS == 0:
        sys.exit("Not enough arguments")

    url = None
    path = None
    artist = None

    for arg in sys.argv[1:]:
        if arg.startswith("https"):
            url = arg
        if arg.startswith("-d="):
            path = arg.split("-d=")[1]
        if arg.startswith("-a="):
            artist = arg.split("-a=")[1]

    main(url, artist, path)
