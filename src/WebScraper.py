from bs4 import BeautifulSoup
import urllib.request

class WebScraper:
    baseurl = None

    def __init__(self, extension: str):
        if extension == "js":
            self.baseurl = "https://www.npmjs.com/package/"
        else:
            self.baseurl = ""   # tmp

    def classifyImport(self, packagename: str):
        try:
            page = urllib.request.urlopen(self.baseurl + packagename)
            soup = BeautifulSoup(page, features="html.parser")
            readme = soup.find(id="readme").text
            readme = readme.lower()
            if ("node.js" in readme):
                return "backend"
            return "frontend"
        except ValueError:
            print(ValueError)
        return None
