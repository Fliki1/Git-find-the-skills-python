from bs4 import BeautifulSoup
import urllib3

class WebScraper:
    baseurl = None

    def __init__(self, extension: str):
        if extension == "js":
            self.baseurl = "https://www.npmjs.com/package/"
        else:
            self.baseurl = ""   # tmp

    def classifyImport(self, packagename: str):
        try:
            #TEST
            page = urllib3.urlopen('http://www.google.com/')
            soup = BeautifulSoup(page)

            x = soup.body.find('div', attrs={'class': 'container'}).text
            #
        except ValueError:
            print(ValueError)
        return None
