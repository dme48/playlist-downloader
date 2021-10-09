#!/usr/bin/python
"""
Searches and downloads a playlist

    Parameters:
        playlist_url (argv[1]): url of the spotify playlist.
        [directory_name] (argv[2]): songs' directory name. Will be created if
            it doesn't exist.
"""
import os
import sys
from scrap import Scrapper
from downloads import DownloadManager


NUM_ARGS = len(sys.argv) - 1

if NUM_ARGS >= 4:
    sys.exit("Too many arguments")
if NUM_ARGS == 0:
    sys.exit("Not enough arguments")

playlist_url = sys.argv[1]
PATH = None
SELECTED_ARTIST = None

for i in range(2, NUM_ARGS+1):
    arg = sys.argv[i]
    if arg.startswith("-d="):
        folder = arg.split("-d=")[1]
        PATH = f"{os.getcwd()}/{folder}"
    if arg.startswith("-a="):
        SELECTED_ARTIST = arg.split("-a=")[1]

playlist_titles = Scrapper(playlist_url, SELECTED_ARTIST).get_searchstring()

down_manager = DownloadManager(playlist_titles, PATH)
down_manager.start_all()
