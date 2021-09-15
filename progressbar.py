from tqdm import tqdm
import time

class QueryProgressBar:
    """
    QueryProgressBar displays information about the status of the queries done by
    youtubesearchpython/VideosSearch.
    """

    def __init__(self, query_size):
        """
        Initializes the bar
            Parameters:
                query_size (int): number of queries
        """
        self.bar = tqdm(total=query_size)

    def callback(self):
        """Increases the bar by one"""
        self.bar.update(1)

class DownloadProgressBar:
    """
    ProgressBar manages information from pytube's streams and videos to show
    and update a progress bar.
    """
    
    def __init__(self, stream_list):
        """
        Creates a StreamTracker for every stream provided, and starts a tqdm progress bar
            Parameters:
                stream_list (list): List containing the (pytube) streams to be tracked.
        """
        self.stream_trackers = {stream: StreamTracker(stream) for stream in stream_list}

        stream_sizes = [stream.STREAM_BYTES for stream in self.stream_trackers.values()]
        self.bar = tqdm(total=sum(stream_sizes))

        self.downloaded_bytes = 0
    
    def callback(self, stream, chunk, remaining_bytes):
        """
        Callback method for the pytube stream.download() method.
        Recieves information from a particular stream, transmits the information to the relevant
        StreamTracker and updates the status of ProgressBar.
            Parameters:
                stream (pytube stream): the stream whose download sent the callback
                chunk (bytes): the chunk of bytes that has just been downloaded
                remaining_bytes (int): the amount of bytes that haven't been downloaded
                    yet, in the stream from the argument
        """
        tracker = self.stream_trackers.get(stream)
        tracker.update_downloaded_bytes(remaining_bytes)

        self.bar.update(tracker.last_chunk_size)


class StreamTracker:
    """Tracks individual streams, providing information about their status"""
    def __init__(self, stream):
        """
        Saves the size of the stream and sets the downloaded bytes to 0
            Parameters:
                stream (pytube's stream): Stream to be tracked.
        """
        self.STREAM_BYTES = stream.filesize
        self.downloaded_bytes = 0
        self.last_chunk_size = 0

    def downloaded_percentage(self):
        """Percentage of the stream that has been downloaded"""
        return 100 * self.downloaded_bytes / self.STREAM_BYTES

    def update_downloaded_bytes(self, remaining_bytes):
        """Updates self.downloaded_bytes in StreamTracker"""
        updated_bytes = self.STREAM_BYTES - remaining_bytes
        self.last_chunk_size = updated_bytes - self.downloaded_bytes
        self.downloaded_bytes = updated_bytes