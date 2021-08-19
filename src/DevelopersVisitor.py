import configparser

class DevelopersVisitor:

    def __init__(self, CONFIG: configparser):
        self.CONFIG = CONFIG
        self.developers = {}        # str, Developer
        self.fileExstensions = {}   # str, str[]
        self.java_fe = list(CONFIG.get("SkillsSection", "java_fe").lower().split(";"))

        for type in ["backend", "frontend", "writer", "undefined"]:
            exstensions = list(CONFIG.get("SkillsSection", type).lower().split(";"))
            self.fileExstensions[type] = exstensions


    def getDevelopers(self):
        return self.developers


    def checkIfFileHasExtension(self, s: str, extn: list):
        """ return boolean value if str s endwith any of extn entry """
        return any([s.endswith(entry) for entry in extn])


    def myfunc(self):
        print(self.CONFIG)
        print(self.developers)
        print(self.fileExstensions)
        print(self.java_fe)
