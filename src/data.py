import urllib.request
import pathlib
from zipfile import ZipFile
import shutil

class Data():
    url ="https://fritz.freiburg.de/csv_Downloads/VAGFR.zip"
    tmp = "data/tmp/data.zip"

    def __init__(self):
        paths = ["data/raw", "data/processed"]
        for path in paths:
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    def download(self):
        pathlib.Path(self.tmp).parent.mkdir()
        urllib.request.urlretrieve(self.url, self.tmp)

    def process(self):
        archive = ZipFile(self.tmp, "r")
        archive.extract("stop_times.txt", "data/raw")
        archive.close()
        shutil.rmtree(pathlib.Path(self.tmp).parent)

    def make(self):
        self.download()
        self.process()