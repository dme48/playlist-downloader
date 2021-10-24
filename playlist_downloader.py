#!/usr/bin/python
"""Searches and downloads a playlist"""
import argparse
from pathlib import Path
from scrap import Scrapper
from downloads import DownloadManager
from conversion import ConversionManager


def main(url: str,
         artist: str = None,
         path: str = None,
         extension: str = None,
         keep_originals: bool = False,
         appended_songs: list[str] = None) -> None:
    """
    Downloads the songs inside a playlist.
    Parameters:
        url (str): url link to a Spotify's playlist. Can be obtained inside spotify's desktop
            app by right-clicking --> Share --> Copy Spotify URL.
        artist (str): if different than None, only the songs with an artist containing
            selected_artist will be downloaded (case insensitive)
        path (Path): Folder to download the songs into. If it doesn't exist it will be created.
        extension (str): Desired format of the output audios (mp3, f.x.).
        appended_songs (list[str]): list with searchings to be appended to the playlist songs.
    """
    path = path if path else Path("Songs/")
    playlist_titles = []
    if url:
        playlist_titles += Scrapper(url, artist).get_searchstring()
    if appended_songs:
        playlist_titles += appended_songs

    down_manager = DownloadManager(playlist_titles, path)
    down_manager.start_all()
    down_manager.wait_until_finished()
    audio_paths = down_manager.get_file_paths()

    if extension:
        conv_manager = ConversionManager(audio_paths)
        conv_manager.convert_all("mp3")
        if not keep_originals:
            conv_manager.delete_originals()


def check_arguments_are_valid(args: argparse.Namespace, parser: argparse.ArgumentParser):
    """
    Checks that the arguments in args are valid, otherwise sends an error through parser.
    Checks for:
        - Either url or appended_songs being present
        - keep_originals can only be present if another extension has been provided
    """
    if not args.url and not args.appended_songs:
        parser.error(
            "Either a url or a list of appended songs (--append) must be provided.")
    if not args.extension and args.keep_originals:
        parser.error(
            "Flag --keep-originals may only be passed if a change of extension (--extension) is provided.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url',
                        type=str,
                        nargs="?",
                        help="Spotify's playlist")
    parser.add_argument('-p', '--path', metavar="DESTINATION_PATH",
                        type=Path,
                        help="Path of the directory songs are downloaded into.")
    parser.add_argument('-a', '--artist',
                        type=str,
                        help="Artist to be filter songs by; if indicated only songs by ARTIST \
                              are downloaded")
    parser.add_argument('-e', '--extension',
                        type=str,
                        help="Desired audio extension for the downloaded files. By default, the \
                              original format of the youtube's video audio; typically mp4.")
    parser.add_argument('--keep-originals',
                        action="store_true",
                        help="Keep original files. Only valid if --extension argument is provided.")

    parser.add_argument('--append',
                        type=str,
                        nargs="+",
                        dest="appended_songs",
                        help="List of songs to append to include in the download.")

    parsed_args = parser.parse_args()
    check_arguments_are_valid(parsed_args, parser)

    main(parsed_args.url,
         artist=parsed_args.artist,
         path=parsed_args.path,
         extension=parsed_args.extension,
         keep_originals=parsed_args.keep_originals,
         appended_songs=parsed_args.appended_songs
         )
