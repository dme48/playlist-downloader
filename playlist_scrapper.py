from urllib import request
import re

class Scrapper:
    def __init__(self, url):
        self.raw_html = request.urlopen(url).read().decode("utf-8")
        self.songs()
    
    def songs(self):
        pattern = r'(?<="is_playable":true,"name":")[^"]+(?=")'
        titles = re.findall(pattern, self.raw_html)
        return titles