"""Container for the Downloader class"""
import threading
from search import YTVideo
from progressbar import DownloadProgressBar, QueryProgressBar


class DownloadManager:
    """Class that handles all the downloads through Downloader instances"""

    def __init__(self, song_list, path):
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
        self.song_list = song_list
        self.path = path
        self.has_started = [False] * len(song_list)

        self.query_bar = QueryProgressBar(len(song_list))
        self.downloads = [Downloader(song, path, self.callback) for song in song_list]

        stream_list = [d.stream for d in self.downloads]
        self.download_bar = DownloadProgressBar(stream_list)

    def start_all(self):
        """Starts all downloads that haven't started already."""
        num_songs = len(self.song_list)
        for i in range(num_songs):
            if self.has_started[i]:
                continue
            self.downloads[i].download()
            self.has_started[i] = True

    def start_by_id(self, index):
        """Starts the download of the song with the indicated id."""
        self.downloads[index].download()
        self.has_started[index] = True

    def start_by_name(self, song_name):
        """Starts the download of the song with the indicated name."""
        index = self.song_list.index(song_name)
        self.start_by_id(index)

    def print_song_id(self):
        """Prints the song names and their indexes"""
        for i, song in enumerate(self.song_list):
            print("id: {},\ttitle: {}".format(i, song))

    def callback(self, stream, chunk, remaining_bytes):
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

    def __init__(self, title, path, callback):
        """
        Querys and selects a video; sets the download as a thread.
            Parameters:
                title (str): title of the song
                path (str): path of the directory where the song is to ve saved
                parent (DownloadManager): Manager of all the Downloader instances.
        """
        self.title = title
        self.path = path
        self.video = YTVideo(title, callback)
        self.stream = self.video.get_stream()

    def download(self):
        """Thread wrapper around stream_download_call"""
        job = threading.Thread(target=self.stream_download_call)
        job.start()

    def stream_download_call(self):
        """Downloads the associated stream in path"""
        self.stream.download(output_path=self.path)
