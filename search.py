"""Container for classes and methods related to searching in youtube"""
from pytube import Search, YouTube

class YTVideo:
    """
    Minimal representation of a youtube video, provides essential information.
        Parameters:
            searchstring (str): string to use on yt search engine
            callback (function): callback to handle the stream download. See documentation on
                progressbar.DownloadProgressBar.callback
    """

    def __init__(self, searchstring, callback = None):
        search = Search(searchstring)
        url = search.results[0].watch_url
        self.vid = YouTube(url, on_progress_callback=callback)

    def get_url(self):
        """Gets the (not embeded) url of the video"""
        return self.vid.watch_url

    def get_stream(self):
        """Returns an audio stream. Assumes the one with most quality."""
        audio_streams = self.vid.streams.filter(only_audio=True)
        return audio_streams.order_by("abr").first()

if __name__ == "__main__":
    vid = YTVideo("Alfonsina y el Mar")
    