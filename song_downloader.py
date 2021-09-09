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
        self.job = threading.Thread(target=self.call_ydl)

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
        """Wrapper around the thread's job"""
        self.job.start()

    def call_ydl(self):
        """
        'Call youtube-dl'. Creates the adequate shell command to download the
        previously selected video.
        """
        url = self.vid_info["link"]
        command = ("youtube-dl -x --audio-format mp3 \"" +
                   url + "\" -o \"" + self.path + "/%(title)s.%(ext)s\"")
        os.system(command)
