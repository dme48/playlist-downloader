"""Container for the Downloader class"""
import os
import threading
from youtubesearchpython import VideosSearch


def str_to_sec(duration):
    """
    Converts a measure of time into its corresponding seconds
        Parameters:
            duration (str): The time interval. Must be specified int the format
                (h)h:mm:ss, (m)m:ss or (s)s.
        Returns:
            coutn (int): Number of seconds in the interval.
    """
    count = 0
    units = [int(s) for s in duration.split(":")]
    for unit in units:
        count *= 60
        count += unit
    return count


class DownloadManager:
    """Class that handles all the downloads through Downloader instances"""

    def __init__(self, song_list, path):
        """
        Creates a Downloader instance for each song in song_list. Also initializes
        the has_started list, which keeps track of which downloads have been started.
            Parameters:
                song_list (string list): list with the titles of the songs to be downloaded.
                path (string): path of the directory where the songs will be saved.
        """
        self.song_list = song_list
        self.path = path
        self.downloads = [Downloader(song, path) for song in song_list]
        self.has_started = [False] * len(song_list)

    def print_song_id(self):
        """Prints the song names and their indexes"""
        for i, song in enumerate(self.song_list):
            print("id: {},\ttitle: {}".format(i, song))

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

class Downloader:
    """Class that handles the download of a single video"""
    TRIAL_VIDS = 3

    def __init__(self, title, path):
        """
        Querys and selects a video; sets the download as a thread.
            Parameters:
                title (str): title of the song
                path (str): path of the directory where the song is to ve saved
        """
        self.title = title
        self.path = path
        self.vid_query = VideosSearch(title, limit=Downloader.TRIAL_VIDS)
        self.vid_info = self.min_duration_video()

    def min_duration_video(self):
        """
        Once the query is done, selects the shortest video found.
            Returns:
                selected_vid (dict): Info on the shortest vid.
        """
        min_duration = float("inf")
        selected_vid = None
        for vid in self.vid_query.result()["result"]:
            duration = str_to_sec(vid["duration"])
            if duration < min_duration:
                min_duration = duration
                selected_vid = vid
        return selected_vid

    def download(self):
        """Wraps call_ydl in a thread and starts it."""
        job = threading.Thread(target=self.call_ydl)
        job.start()

    def call_ydl(self):
        """
        'Call youtube-dl'. Creates the adequate shell command to download the
        previously selected video.
        """
        url = self.vid_info["link"]
        command = ("youtube-dl -x --audio-format mp3 \"" +
                   url + "\" -o \"" + self.path + "/%(title)s.%(ext)s\"")
        os.system(command)
