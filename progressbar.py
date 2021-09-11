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

if __name__ == "__main__":
    pb = ProgressBar()