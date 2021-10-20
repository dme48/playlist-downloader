#!/usr/bin/python
"""Searches and downloads a playlist"""
import sys
import argparse
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
        artist (str): if different than None, only the songs with an artist containing
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
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-p', '--path')
    parser.add_argument('-a', '--artist')

    parsed_args = parser.parse_args(sys.argv[1:])

    main(parsed_args.url,
         parsed_args.artist,
         parsed_args.path)
