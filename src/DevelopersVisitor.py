import configparser
import re

class DevelopersVisitor:

    def __init__(self, CONFIG: configparser):
        self.CONFIG = CONFIG
        self.developers = {}        # str, Developer
        self.fileExstensions = {}   # str, str[]
        self.java_fe = list(CONFIG.get("SkillsSection", "java_fe").lower().split(";"))

        for type in ["backend", "frontend", "writer", "undefined"]:
            exstensions = list(CONFIG.get("SkillsSection", type).lower().split(";"))
            self.fileExstensions[type] = exstensions

        self.HTML_PATTERN = "<(\"[^\"]*\"|'[^']*'|[^'\">])*>"
        # TODO: controllare se [ di apertura sono leciti: leggo che
        #  In Python you don't need to escape any nested [ but you do need to do that in Java.


    def getDevelopers(self):
        return self.developers


    def checkIfFileHasExtension(self, s: str, extn: list):
        """ return boolean value if str s endwith any of extn entry """
        return any([s.endswith(entry) for entry in extn])


    def hasHTMLTags(self, text: str):
        """ This method matches the regex pattern in the string with the optional flag.
        It returns true if a match is found in the string otherwise it returns false."""
        return re.match(self.HTML_PATTERN, text)
        """ This method returns the match object if there is a match found in the string. """
        #re.search(regex, text)


    def convertToLowerCase(self, strings: []):
        """ ritorna la lista di stringhe senza spazi agli estremi: strim->strip e in lowercase"""
        return [string.strip().lower() for string in strings]


    def getOnlyAdditions(self):
        """ lista string di soli ADD dalla mod corrente """

    def myfunc(self):
        print(self.CONFIG)
        print(self.developers)
        print(self.fileExstensions)
        print(self.java_fe)
