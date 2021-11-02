"""Module for progress bars' interfaces, and smaller classes they depend on."""
from pytube.streams import Stream
from tqdm import tqdm


class QueryProgressBar:
    """
    QueryProgressBar displays information about the status of the queries done by
    youtubesearchpython/VideosSearch.
    """

    def __init__(self, query_size: int) -> None:
        """
        Initializes the bar
            Parameters:
                query_size (int): number of queries
        """
        bar_format = "Searching YT:|{bar}| {n_fmt}/{total_fmt}"
        self.query_bar = tqdm(total=query_size, bar_format=bar_format)

    def callback(self) -> None:
        """Increases the bar by one"""
        self.query_bar.update(1)

    def reset(self) -> None:
        """Resets query_bar"""
        self.query_bar.reset()


class StreamTracker:
    """Tracks individual streams, providing information about their status"""

    def __init__(self, stream: Stream) -> None:
        """
        Saves the size of the stream and sets the downloaded bytes to 0
            Parameters:
                stream (pytube's stream): Stream to be tracked.
        """
        self.filesize = stream.filesize
        self.downloaded_bytes = 0
        self.last_chunk_size = 0

    def downloaded_percentage(self) -> int:
        """Percentage of the stream that has been downloaded"""
        return 100 * self.downloaded_bytes // self.filesize

    def update_downloaded_bytes(self, remaining_bytes: int) -> None:
        """Updates self.downloaded_bytes in StreamTracker"""
        old_downloaded_bytes = self.downloaded_bytes
        self.downloaded_bytes = self.filesize - remaining_bytes
        self.last_chunk_size = self.downloaded_bytes - old_downloaded_bytes

    def is_finished(self) -> None:
        """Checks if the stream has finished downloading"""
        return self.filesize == self.downloaded_bytes


class DownloadProgressBar:
    """
    ProgressBar manages information from pytube's streams and videos to show
    and update a progress bar.
    """

    def __init__(self, stream_list: list[Stream]) -> None:
        """
        Creates a StreamTracker for every stream provided, and starts a tqdm progress bar
            Parameters:
                stream_list (list): List containing the (pytube) streams to be tracked.
        """
        self.stream_trackers = {stream: StreamTracker(
            stream) for stream in stream_list}
        self.is_finished = {stream: False for stream in stream_list}

        stream_sizes = [
            tracker.filesize for tracker in self.stream_trackers.values()]
        bar_format = "Downloading: |{bar}| {desc}: {percentage:3.0f}%"
        self.download_bar = tqdm(
            total=sum(stream_sizes), bar_format=bar_format)

        self.downloaded_bytes = 0

    def callback(self, stream: Stream, chunk: bytes, remaining_bytes: int) -> None:
        """
        Callback method for the pytube stream.download() method.
        Recieves information from a particular stream, transmits the information to the relevant
        StreamTracker and updates the status of ProgressBar.
            Parameters:
                stream (pytube stream): the stream whose download sent the callback
                chunk (bytes): the chunk of bytes that has just been downloaded (unused)
                remaining_bytes (int): the amount of bytes that haven't been downloaded
                    yet, in the stream from the argument
        """
        del chunk
        print("called")
        tracker = self.stream_trackers.get(stream)
        tracker.update_downloaded_bytes(remaining_bytes)
        self.update(stream, tracker)

    def update(self, stream: Stream, tracker: StreamTracker) -> None:
        """Updates the bar by the tracker's last chunk, checking if it has finished"""
        self.download_bar.update(tracker.last_chunk_size)
        self.is_finished[stream] = tracker.is_finished()
        if all(self.is_finished):
            self.download_bar.close()

    def reset(self) -> None:
        """Resets the bar"""
        self.download_bar.reset()
