# Playlist Downloader
Playlist Downloader is a tool to download songs from a Spotify's playlist. The songs are downloaded from youtube with [pytube](https://pytube.io/en/latest/).


## Usage
```
    python playlist_downloader.py [OPTIONS] <spotify's url>
```
If no options are provided, the program creates a `Songs` folder and downloads all the songs present at the url into it. These files will have the original sound extension, typically a mp4 sound file.

## Options

    -d=<destination_folder>              Destination folder for the downloaded songs. Will
                                         be created if not present. Defaults to "Songs".
    -a=<author>                          Filters the songs at the playlist by author,
                                         downloading only those whose author matches
                                         <author> (case insensitive).

## About
Playlist Downloader's core structure is quite simple, connecting two elements:

1. A "Scrapper": The Scrapper job is to access the Spotify's url and obtain all of the songs that appear inside. Currently Playlist Downloader does this by using regex on the raw html, but a more solid approach, using a html parser, is being worked on.
2. A "Downloader": There's a `DownloadManager` class that takes a list of titles as the input and coordinates several individual `Downloader`s to download each of the songs.

Other minor components are present, mainly to search for youtube videos (via `pytube`) or to show the status of the downloads (via `tqdm`).
