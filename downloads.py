"""Container for the Downloader class"""
import threading
from typing import Callable
from pathlib import Path
from pytube import Stream
from search import YTVideo
from progressbar import DownloadProgressBar, QueryProgressBar

Callback = Callable[[Stream, bytes, int], None]

class DownloadManager:
    """Class that handles all the downloads through Downloader instances"""

    def __init__(self, song_list: list[str], path: Path) -> None:
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
        self.has_started = False
        if not path.exists():
            path.mkdir()
        self.path = path
        self.query_bar = QueryProgressBar(len(song_list))
        self.downloads = [Downloader(song, self) for song in song_list]

        stream_list = [d.stream() for d in self.downloads]
        self.download_bar = DownloadProgressBar(stream_list)

    def start_all(self) -> None:
        """Starts all downloads that haven't started already."""
        for downloader in self.downloads:
            downloader.download()
        self.has_started = True

    def wait_until_finished(self) -> None:
        """Waits until all the Downloader threads have finished"""
        for downloader in self.downloads:
            if not downloader.job:
                raise ValueError(f"Download at {downloader} hasn't been called yet")
            downloader.job.join()

    def get_file_paths(self) -> list[Path]:
        """Returns the audio file paths; can only be called after downloads are finished"""
        return [d.get_absolute_path() for d in self.downloads]

    def is_download_complete(self) -> None:
        """Checks every Downloader has finished downloading its song"""
        for download in self.downloads:
            if not download.finished:
                return False
            return True

    def query_callback(self) -> None:
        """Updates the query progressbar. Should be called when Downloader finishes a query"""
        self.query_bar.callback()

    def download_callback(self, stream: Stream, chunk: bytes, remaining_bytes: int):
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
    def __init__(self, title: str, parent: DownloadManager) -> None:
        """
        Querys and selects a video; sets the download as a thread.
            Parameters:
                title (str): title of the song
                parent (DownloadManager): Manager of the Downloader instance
        """
        self.title = title
        self.path = parent.path
        self.video = YTVideo(title, parent.download_callback)
        parent.query_callback()
        self.job = None

    def stream(self) -> Stream:
        """
        Returns the stream associated to the video. The stream is saved at YTVideo's cache, so after
        the first call, get_stream is unexpensive to call.
        """
        return self.video.get_stream()

    def download(self) -> None:
        """Thread wrapper around _stream_download_call"""
        if self.job:
            raise ValueError(f"Download already at progress\nVid:{self.get_filename}")
        self.job = threading.Thread(target=self._stream_download_call)
        self.job.start()

    def _stream_download_call(self) -> None:
        """Downloads the associated stream in path"""
        stream = self.video.get_stream()
        stream.download(output_path=self.path, filename = self.get_filename())

    def get_filename(self) -> None:
        """Returns the relative path of the downloaded song."""
        filename = self.video.vid.title
        ext = self.video.get_format()
        return f"{filename}.{ext}"

    def get_absolute_path(self) -> Path:
        """Returns the absolute path of the downloaded song."""
        return Path(self.path, self.get_filename())


def check_songlist(song_list: list[str]) -> None:
    """Checks that song_list is not None and that its elements are strings."""
    if not song_list:
        raise TypeError("The song list was None or empty.")
    for song in song_list:
        if not isinstance(song, str):
            raise TypeError(f"Input '{song}' in song_list was not a string")
