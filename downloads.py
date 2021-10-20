"""Container for the Downloader class"""
import os
import threading
from typing import Callable
from pytube import Stream
from search import YTVideo
from progressbar import DownloadProgressBar, QueryProgressBar

Callback = Callable[[Stream, bytes, int], None]

class DownloadManager:
    """Class that handles all the downloads through Downloader instances"""

    def __init__(self, song_list: list[str], path: str) -> None:
        """
        Creates a Downloader instance for each song in song_list.
        Initializes the has_started list, which keeps track of which downloads have been
        started.
        Creates a QueryProgressBar and a DownloadProgressBar, used to keep track of the state of
        the yt queries and the downloads, respectively.
            Parameters:
                song_list (string list): list with the titles of the songs to be downloaded.
                path (string): path of the directory where the songs will be saved.
        """
        check_songlist(song_list)
        self.song_list = song_list
        self.path = path if path.endswith("/") else path + "/"
        self.has_started = False

        self.query_bar = QueryProgressBar(len(song_list))
        self.downloads = [Downloader(song, self.path, self.callback) for song in song_list]

        stream_list = [d.stream for d in self.downloads]
        self.download_bar = DownloadProgressBar(stream_list)

        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def start_all(self) -> None:
        """Starts all downloads that haven't started already."""
        for downloader in self.downloads:
            downloader.download()
        self.has_started = True

    def get_file_paths(self) -> None:
        """Returns the audio file paths; can only be called after downloads are finished"""
        if not self.is_download_complete():
            raise ValueError("Can't get file paths until audio files have been downloaded.")
        return [d.get_filename for d in self.downloads]

    def is_download_complete(self) -> None:
        """Checks every Downloader has finished downloading its song"""
        for download in self.downloads:
            if not download.finished:
                return False
            return True

    def callback(self, stream: Stream, chunk: bytes, remaining_bytes: int):
        """
        Connector between the callbacks in Downloader instances and the bar.
        See DownloadProgressBar.callback for more info about the callback.
        """
        if "download_bar" not in self.__dict__.keys():
            raise Exception("The DownloadProgressBar in DownloadManager should" \
                            " have been created before callback is called.")

        self.download_bar.callback(stream, chunk, remaining_bytes)

class Downloader:
    """
    Class that handles the download of a single video.
    """
    def __init__(self, title: str, path:str, callback: Callback) -> None:
        """
        Querys and selects a video; sets the download as a thread.
            Parameters:
                title (str): title of the song
                path (str): path of the directory where the song is to be saved
                callback (function): callback for pytube. See DownloadProgressBar.callback
        """
        self.title = title
        self.path = path
        self.video = YTVideo(title, callback)
        self.started = False
        self.finished = False

    def download(self) -> None:
        """Thread wrapper around stream_download_call"""
        if self.started:
            raise ValueError("The download has already started.")
        self.started = True
        job = threading.Thread(target=self._stream_download_call)
        job.start()

    def _stream_download_call(self) -> None:
        """Downloads the associated stream in path"""
        stream = self.video.get_stream()
        stream.download(output_path=self.path)
        self.finished = True

    def get_filename(self) -> None:
        """Returns the path of the downloaded song. Currently adds mp4 as ext. without checking"""
        if not self.finished:
            raise ValueError("Song must be downloaded before the path is returned.")
        filename = self.video.vid.title
        ext = self.video.get_format()
        return f"{self.path}{filename}.{ext}"


def check_songlist(song_list: list[str]) -> None:
    """Checks that song_list is not None and that its elements are strings."""
    if not song_list:
        raise TypeError("The song list was None or empty.")
    for song in song_list:
        if not isinstance(song, str):
            raise TypeError(f"Input '{song}' in song_list was not a string")
