#!/usr/bin/python
"""Searches and downloads a playlist"""
import sys
import argparse
from scrap import Scrapper
from downloads import DownloadManager
from conversion import ConversionManager


def main(url: str,
         artist: str,
         path: str,
         extension: str,
         appended_songs: list[str]) -> None:
    """
    Downloads the songs inside a playlist.
    Parameters:
        url (str): url link to a Spotify's playlist. Can be obtained inside spotify's desktop
            app by right-clicking --> Share --> Copy Spotify URL.
        artist (str): if different than None, only the songs with an artist containing
            selected_artist will be downloaded (case insensitive)
        path (str): Folder to download the songs into. If it doesn't exist it will be created.
        extension (str): Desired format of the output audios (mp3, f.x.).
        appended_songs (list[str]): list with searchings to be appended to the playlist songs.
    """
    if not url:
        raise TypeError("A valid url must be provided.")
    path = path if path else "Songs/"

    playlist_titles = Scrapper(url, artist).get_searchstring()
    if appended_songs:
        playlist_titles += appended_songs

    down_manager = DownloadManager(playlist_titles, path)
    down_manager.start_all()
    down_manager.wait_until_finished()
    audio_paths = down_manager.get_file_paths()

    if extension:
        conv_manager = ConversionManager(audio_paths)
        conv_manager.convert_all("mp3")
        conv_manager.delete_originals()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-p', '--path')
    parser.add_argument('-a', '--artist')
    parser.add_argument('-e', '--extension')
    parser.add_argument('--append', type=str, nargs="+", dest="appended_songs")

    parsed_args = parser.parse_args(sys.argv[1:])

    main(parsed_args.url,
         parsed_args.artist,
         parsed_args.path,
         parsed_args.extension,
         parsed_args.appended_songs)
