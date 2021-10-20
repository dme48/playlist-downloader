"""Container for classes and methods related to searching in youtube"""
from typing import Callable
from inspect import signature
from pytube import Search, Stream

Callback = Callable[[Stream, bytes, int], None]

def check_callback(callback: Callback) -> None:
    """Checks that a callback has the right amount of needed arguments or that is None"""
    if callback is None:
        return
    param_number = len(signature(callback).parameters)

    if param_number != 3:
        raise ValueError("The callback passed to YTVideo is supposed to have 3 parameters.")


class YTVideo:
    """
    Minimal representation of a youtube video, provides essential information.
        Parameters:
            searchstring (str): string to use on yt search engine
            callback (function): callback to handle the stream download. See documentation on
                progressbar.DownloadProgressBar.callback
    """

    def __init__(self, searchstring: str, callback: Callback=None) -> None:
        check_callback(callback)

        search = Search(searchstring)
        if len(search.results) == 0:
            raise ValueError(f"The searchstring '{searchstring}' didn't have any matches.")
        self.vid = search.results[0]

        # It takes time to get the stream, will only fetch through get_stream or get_format
        self.stream = None

    def get_url(self) -> str:
        """Gets the (not embeded) url of the video"""
        return self.vid.watch_url

    def get_stream(self) -> Stream:
        """Returns the audio stream with most quality."""
        if not self.stream:
            audio_streams = self.vid.streams.filter(only_audio=True)
            self.stream = audio_streams.order_by("abr").first()
        return self.stream

    def get_format(self) -> str:
        """Returns the format associated with the selected stream"""
        raw_type = self.get_stream().mime_type
        return raw_type.split("/")[1]

if __name__ == "__main__":
    vid = YTVideo("Alfonsina y el Mar")
    url = vid.get_url()
    stream = vid.get_stream()
