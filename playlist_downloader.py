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
from scrap import scrap_songs
from downloads import DownloadManager


NUM_ARGS = len(sys.argv) - 1

if NUM_ARGS >= 3:
    sys.exit("Too many arguments")
if NUM_ARGS == 0:
    sys.exit("Not enough arguments")

playlist_url = sys.argv[1]

if NUM_ARGS == 1:
    path = os.getcwd() + "/Songs"
elif NUM_ARGS == 2:
    path = os.getcwd() + "/" + sys.argv[2]

if not os.path.exists(path):
    os.mkdir(path)

playlist_titles = scrap_songs(playlist_url)
playlist_titles.append("blue eyes elton john")

down_manager = DownloadManager(playlist_titles, path)
down_manager.start_all()
