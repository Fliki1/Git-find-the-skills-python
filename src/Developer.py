import configparser
from src import GitSocialScraper

class Developer:  # Committer: chi fa il commit o Author: autore delle modifiche
    name = None
    email = None
    commit = None

    extraCategory = None

    id = None
    username = None
    avatar_url = None
    website = None
    location = None
    bio = None
    created_at = None

    devPoints = None

    # https://api.github.com/users/fliki1
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.commit = 0
        self.devPoints = {}  # HashMap<String, Integer>

        self.setId()
        self.setUsername()
        self.setAvatar_url()
        self.setWebsite()
        self.setLocation()
        self.setBio()
        self.setCreated_at()

        self.extraCategory = []  # String list

        self.devPoints["frontend"] = 0
        self.devPoints["writer"] = 0
        self.devPoints["backend"] = 0


    def initExtraCategory(self, CONFIG: configparser):
        """ salvo in devPoints e extraCategory le categorie extra """
        arrayProps = ["repository", "backend", "frontend", "writer", "undefined", "java_fe", "export_as"]
        if "repository" not in arrayProps:  # non ha senso di esistere
            self.devPoints["repository"] = 0
            self.extraCategory.append("repository")
        for key in CONFIG["SkillsSection"]:
            if key not in arrayProps:
                self.devPoints[key] = 0
                self.extraCategory.append(key)


    def editPoints(self, key: str, value: int):
        self.devPoints[key] = self.devPoints.get(key) + value
        return self.devPoints.get(key)

    def getKeyPoints(self):
        return self.devPoints.keys()

    def getPoints(self, key:str):
        return self.devPoints.get(key)

    def initSocialInfo(self, socialname:str):
        socialscaper = GitSocialScraper.GitSocialScraper(socialname)
        try:
            socialinfo = socialscaper.getInfo(self.email)
            print("email: ", self.email)
            if socialinfo != None:
                self.setId(socialinfo.get("id"))
                self.setUsername(socialinfo.get("username"))
                self.setAvatar_url(socialinfo.get("avatar_url"))
                self.setWebsite(socialinfo.get("website"))
                self.setLocation(socialinfo.get("location"))
                self.setBio(socialinfo.get("bio"))
                self.setCreated_at(socialinfo.get("created_at"))
            else:
                print("No socialinfo detected for: ", self.email)
        except ValueError:
            print(ValueError)

    def print(self):
        print("Name: " + self.name)
        print("Email: " + self.email)

        total = 0
        for i in self.devPoints.keys():
            print("Category: " + i + " Points: " + str(self.devPoints[i]))
            total += self.devPoints[i]
        if total != 0:
            for i in self.devPoints.keys():
                print("Category: " + i + " Percentage: " + str(round(float(self.devPoints[i]*100/total))) + "%")

    def setId(self, id=None):
        self.id = id

    def getId(self):
        return self.id

    def setUsername(self, username=None):
        self.username = username

    def getUsername(self):
        return self.username

    def setAvatar_url(self, avatar_url=None):
        self.avatar_url = avatar_url

    def getAvatar_url(self):
        return self.avatar_url

    def setWebsite(self, website=None):
        self.website = website

    def getWebsite(self):
        return self.website

    def setLocation(self, location=None):
        self.location = location

    def getLocation(self):
        return self.location

    def setBio(self, bio=None):
        self.bio = bio

    def getBio(self):
        return self.bio

    def setCreated_at(self, created_at=None):
        self.created_at = created_at

    def getCreated_at(self):
        return self.created_at
