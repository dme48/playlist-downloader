#!/usr/bin/python
"""
Searches and downloads a playlist

    Parameters:
        playlist_url (argv[1]): url of the spotify playlist.
        [directory_name] (argv[2]): songs' directory name. Will be created if
            it doesn't exist.
"""
from playlist_scrapper import Scrapper
from song_downloader import Downloader
import sys
import os
import json


num_args = len(sys.argv) - 1

if num_args >= 3:
    sys.exit("Too many arguments")
if num_args == 0:
    sys.exit("Not enough arguments")

playlist_url = sys.argv[1]

if num_args == 1:
    path = os.getcwd() + "/Songs"
elif num_args == 2:
    path = os.getcwd() + "/" + sys.argv[2]

if not os.path.exists(path):
    os.mkdir(path)

playlist_titles = Scrapper(playlist_url).songs()
playlist_titles.append("blue eyes elton john")

all_downloaders = []

for song in playlist_titles:
    downloader = Downloader(song, path)
    downloader.download()
    all_downloaders.append(downloader)
