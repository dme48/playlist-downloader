import os
import threading
from youtubesearchpython import VideosSearch


def str_to_sec(duration):
    count = 0
    units = [int(s) for s in duration.split(":")]
    for unit in units:
        count *= 60
        count += unit
    return count


class Downloader:
    TRIAL_VIDS = 3

    def __init__(self, title, path):
        self.title = title
        self.path = path
        self.vid_query = VideosSearch(title, limit=Downloader.TRIAL_VIDS)
        self.vid_info = self.min_duration_video()
        self.job = threading.Thread(target=self.call_ydl)

    def min_duration_video(self):
        min_duration = float("inf")
        selected_vid = None
        for vid in self.vid_query.result()["result"]:
            duration = str_to_sec(vid["duration"])
            if (duration < min_duration):
                min_duration = duration
                selected_vid = vid
        return selected_vid

    def download(self):
        self.job.start()

    def call_ydl(self):
        url = self.vid_info["link"]
        command = "youtube-dl -x --audio-format mp3 \"" + url + "\" -o \"" + self.path + "/%(title)s.%(ext)s\""
        print("The command is: " + command)
        os.system(command)
