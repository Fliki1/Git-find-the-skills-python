import configparser
import sys
import csv
import time
from datetime import datetime
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
        replace = urlNoProtocol.replace(".", "/")   # per splittare anche github.com/... --> github/com/...
        splitted = replace.split("/")
        if len(splitted) > 0:
            return splitted[0].strip()
    else:
        url = os.path.expanduser(urlOrPath+"/.git/config")
        try:
            f = open(url, "r")
            for text in f.readlines():
                if text.strip().startswith("url = "):
                    urlNoProtocol = text.replace("url", "").replace("=", "").replace("git@", "").replace("www", "").replace("https://", "").replace("http://", "")
                    replace = urlNoProtocol.replace(".", "/")  # per splittare anche github.com/... --> github/com/...
                    splitted = replace.split("/")
                    if len(splitted) > 0:
                        return splitted[0].strip()
        except ValueError:
            print(ValueError)
        finally:
            try:
                f.close()
            except ValueError:
                print(ValueError)

def getRepoName(url: str):
    splitted = url.split("/")
    return splitted[ len(splitted)-1 ]



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
    print("socialname", socialname)
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
        #time.sleep(60)  # GitHub Error: Authenticated requests get a higher rate limit. Check out the documentation for more details...

    now = datetime.now() #  2021-03-24 16:48:05.591
    timestamp = now.strftime("%m-%d-%Y_%H:%M:%S")
    filename = getRepoName(urlOrPath) +"_"+ timestamp

    if CONFIG["OutputSection"]["export_as"] == "csv":
        try:
            csv_headers = ["Name", "Email", "SocialID", "SocialUsername", "AvatarURL", "WebSite", "Location", "Bio", "CreatedAt", "Commits"]
            heading = "Name;Email;SocialID;SocialUsername;AvatarURL;WebSite;Location;Bio;CreatedAt;Commits;"
            ciao = list(developers.keys())
            firstDev = developers.get(ciao[0])
            for cat in firstDev.getKeyPoints(): # ogni categoria extra?
                heading += cat + "%;"

            with open(filename + ".csv", 'w') as f:
                # Header del csv
                writer = csv.DictWriter(f, fieldnames=heading, delimiter=';')

                writer.writeheader()
                for i in developers.values():
                    # riga del csv
                    total = 0
                    for cat in i.getKeyPoints():
                        total += i.getPoints( cat )

                    singleline = i.name + ";" + i.email + ";" + (
                        " " if (i.getId() == None) else i.getId() ) + ";" + (
                        " " if (i.getUsername() == None) else i.getUsername() ) + ";" + (
                        " " if (i.getAvatar_url() == None) else i.getAvatar_url()) + ";" + (
                        " " if (i.getWebsite() == None) else i.getWebsite() ) + ";" + (
                        " " if (i.getLocation() == None) else i.getLocation()) +  ";" + (
                        " " if (i.getBio() == None) else i.getBio()) + ";" + (
                        " " if (i.getCreated_at() == None) else i.getCreated_at()) + ";" + str(i.commit) + ";"

                    for cat in i.getKeyPoints():
                        singleline += str( round(float(i.getPoints( cat )*100/total)) ) + ";"

                    writer.writerow(singleline)
            print('csv')
        except ValueError:
            print(ValueError)
    elif CONFIG["OutputSection"]["export_as"] == "html":
        pass
    else: print("Not valid output provided. Output supported: csv or html")

    #p1.myfunc()
    #p1.checkIfFileHasExtension("testaciao", ["tavolo","sedia","comodinociao", "ciao"])

    print("this is the end")
    del analyzer





"""
        try:
            csv_headers = ["Name", "Email", "SocialID", "SocialUsername", "AvatarURL", "WebSite", "Location", "Bio", "CreatedAt", "Commits"]
            heading = "Name;Email;SocialID;SocialUsername;AvatarURL;WebSite;Location;Bio;CreatedAt;Commits;"
            ciao = list(developers.keys())
            firstDev = developers.get(ciao[0])
            for cat in firstDev.getKeyPoints(): # ogni categoria extra?
                heading += cat + "%;"

            with open(filename + ".csv", 'w') as f:
                # Header del csv
                writer = csv.DictWriter(f, fieldnames=heading, delimiter=';')

                writer.writeheader()
                for i in developers.values():
                    # riga del csv
                    total = 0
                    for cat in i.getKeyPoints():
                        total += i.getPoints( cat )

                    singleline = i.name + ";" + i.email + ";" + (
                        " " if (i.getId() == None) else i.getId() ) + ";" + (
                        " " if (i.getUsername() == None) else i.getUsername() ) + ";" + (
                        " " if (i.getAvatar_url() == None) else i.getAvatar_url()) + ";" + (
                        " " if (i.getWebsite() == None) else i.getWebsite() ) + ";" + (
                        " " if (i.getLocation() == None) else i.getLocation()) +  ";" + (
                        " " if (i.getBio() == None) else i.getBio()) + ";" + (
                        " " if (i.getCreated_at() == None) else i.getCreated_at()) + ";" + str(i.commit) + ";"

                    for cat in i.getKeyPoints():
                        singleline += str( round(float(i.getPoints( cat )*100/total)) ) + ";"

                    writer.writerow(singleline)
            print('csv')
        except ValueError:
            print(ValueError)
"""