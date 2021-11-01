# Playlist Downloader
Playlist Downloader is a tool to download songs from a Spotify's playlist. The songs are downloaded from youtube with [pytube](https://pytube.io/en/latest/).


## Usage
To use playlist_downloader reach the project's folder through a shell and write:
```
    python playlist_downloader.py [OPTIONS] URL
```
With URL being a link to a Spotify's playlist. Can be obtained inside spotify's desktop app by right-clicking --> Share --> Copy Spotify URL. URL is optional if an --append option is provided, otherwise it is required (see [options](##Options)).

If no options are provided, the program creates a `Songs` folder and downloads all the songs present at the url into it. These files will have the original sound extension, typically a sound file extracted from a mp4 file.

## Options

    -h, --help                           Show help on how to execute the program.

    -p PATH, --path PATH                 Path of the destination folder for the downloaded
                                         songs. Will be created if not present. Defaults
                                         to "Songs/".

    -a ARTIST, --artist ARTIST           Filters the songs at the playlist by artist,
                                         downloading only those whose author matches
                                         <author> (case insensitive).

    -e EXTENSION, --extension EXTENSION  Desired format for the downloaded files.

    --keep-originals                     If a new extension is provided (through -e
                                         EXTENSION), keep the files with the original
                                         format. By default those files are deleted.

    --append [SONG_SEQUENCE]             Appends the songs in SONG_SEQUENCE to the songs
                                         extracted from the playlist. Make sure to quote each
                                         song for proper parsing. Including the artist in the
                                         searchstring (e.g. "Hey Jude, Beatles") is
                                         allowed and recommended.

## About
Playlist Downloader's core structure is quite simple, connecting two main elements:

1. A "Scrapper": The Scrapper job is to access the Spotify's url and obtain all of the songs that appear inside.
2. A "Downloader": There's a `DownloadManager` class that takes a list of titles as the input and coordinates several individual `Downloader`s to download each of the songs.

Other minor components are present, mainly to search for youtube videos (via `pytube`), to show the status of the downloads (via `tqdm`) or to convert the audio files (via `pydub`).
