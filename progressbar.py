from tqdm import tqdm
import time

class ProgressBar:
    """
    TODO, not implemented yet
    ProgressBar manages information from pytube's streams and videos to show
    and update a progress bar.
    """
    
    def __init__(self):
        """Inits the stream, TODO"""
    
    def callback(self, stream, chunk, remaining_bytes):
        """
        TODO, not implemented yet
        Recieves information from a particular stream and updates it.
            Parameters:
                stream (pytube stream): the stream whose download sent the callback
                chunk (bytes): the chunk of bytes that has just been downloaded
                remaining_bytes (int): the amount of bytes that haven't been downloaded
                    yet, in the stream from the argument
        """
        print("I received a callback")


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