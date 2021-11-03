"""Collection of exceptions related to the playlist_downloader module"""

class InvalidStateError(Exception):
    """
    Raised when an object reaches a state that doesn't make sense or tries to call methods in a
    wrong order, e.g. by trying to parse html before having downloaded it.

    In this project, proper initialization avoids most of InvalidStateError candidates, but they
    are still likely to appear when 
        a) using threads/async tasks and
        b) using single-use methods multiple times
    As an example of the second case, Converter instances are associated to an original and a
    converted audio file. A delete_originals method may incur in an InvalidStateError if it is
    called before the audios are converted or after the originals have been deleted.
    """
    def __init__(self, message):
        super().__init__(message)