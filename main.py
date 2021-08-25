import configparser
import sys
import os
from src import DevelopersVisitor

CONFIG = configparser.RawConfigParser()
#CONFIG.read('ConfigFile.properties')


def validatePropertiesSkills():
    """ Valida i campi primari di ConfigFile.properties (non vuoti) [✓]"""
    isValid = True
    for section in ["RepositorySection", "SkillsSection", "OutputSection"]:
        for key in CONFIG[section]:
            if CONFIG.get(section, key) is None or CONFIG.get(section, key) == "":  # non ci sono campi
                isValid = False
                print("Please insert a valid value for " + key + " in Config.properties file.")
            elif len(CONFIG.get(section, key).split(';')) == 0:                     # non ci sono campi
                isValid = False
                print("Please insert a valid value for " + key + " in Config.properties file.")
    return isValid

def isRemote(url:str):
    if url.startswith("www") or url.startswith("http"):
        return True
    return False

def getSocialName(urlOrPath: str):
    if isRemote(urlOrPath):
        urlNoProtocol = urlOrPath.replace("www", "").replace("https://", "").replace("http://","")
        splitted = urlNoProtocol.split("\\.")
        if len(splitted) > 0:
            return splitted[0].strip()
    else:
        url = os.path.expanduser(urlOrPath+"/.git/config")
        try:
            f = open(url, "r")
            for text in f.readlines():
                if text.strip().startswith("url = "):
                    urlNoProtocol = text.replace("url", "").replace("=", "").replace("git@", "").replace("www", "").replace("https://", "").replace("http://", "")
                    splitted = urlNoProtocol.split("\\.")
                    if len(splitted) > 0:
                        return splitted[0].strip()
        except ValueError:
            print(ValueError)
        finally:
            try:
                f.close()
            except ValueError:
                print(ValueError)




if __name__ == '__main__':
    try:
        CONFIG.read('ConfigFile.properties')
    except ValueError:
        print(ValueError)

    if validatePropertiesSkills() == False:     # ConfigFile.properties: wrong or empty fields
        sys.exit(0)

    #TODO: start the metric
    analyzer = DevelopersVisitor.DevelopersVisitor(CONFIG)
    urlOrPath = CONFIG["RepositorySection"]["repository"]
    analyzer.process(urlOrPath)
    #analyzer.process('https://github.com/devopstrainingblr/Maven-Java-Project.git')

    socialname = getSocialName(urlOrPath)

    orginalDev = analyzer.getDevelopers()

    # Removing duplicate users. Primary key = email
    developers = {}
    for i in orginalDev.values():
        dev = None
        for j in developers.values():
            if j.email == i.email:
                dev = j
        if dev == None:
            developers[i.name] = i
        else:
            print("Merge points/commit for: " + i.name + " , " + dev.name )
            for cat in dev.getKeyPoints():
                dev.editPoints(cat, i.getPoints(cat))
            dev.commit += i.commit

    print("Start scraping social info for: " + str(len(developers)) + " developers.")
    max_commit = 0
    for i in developers.values():
        if i.commit > max_commit:
            max_commit = i.commit
        i.initSocialInfo(socialname)

    #p1.myfunc()
    #p1.checkIfFileHasExtension("testaciao", ["tavolo","sedia","comodinociao", "ciao"])

    print("this is the end")
    del analyzer
