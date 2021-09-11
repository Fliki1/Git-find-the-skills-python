import configparser
import sys
import csv
import time
from datetime import datetime
import json
import os, zipfile
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
            elif key in ["backend", "frontend", "writer", "undefined"] and len(CONFIG.get(section, key).split(';')) == 0:       # almeno 1 valore presente
                isValid = False
                print("Please insert a valid value for " + key + " in Config.properties file.")
    return isValid

def isRemote(url:str):
    if url.startswith("www") or url.startswith("http"):
        return True
    return False

def getSocialName(urlOrPath: str):
    """ return the domain of repository: github/gitlab/... """
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

def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, mode='w') as zipf:
        len_dir_path = len(folder_path)
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path[len_dir_path:])

if __name__ == '__main__':
    try:
        CONFIG.read('ConfigFile.properties')
    except ValueError:
        print(ValueError)

    if validatePropertiesSkills() == False:     # ConfigFile.properties: empty fields #ok
        sys.exit(0)

    # Java execute()
    analyzer = DevelopersVisitor.DevelopersVisitor(CONFIG)
    urlOrPath = CONFIG["RepositorySection"]["repository"]   # ok
    analyzer.process(urlOrPath)

    socialname = getSocialName(urlOrPath)
    orginalDev = analyzer.getDevelopers()
    for a in orginalDev.keys():
        print(a, orginalDev[a].email)

    # Removing duplicate users. Primary key = email
    developers = {}
    for i in orginalDev.values():   # for all dev in repo
        dev = None
        for j in developers.values():   # check if already in list
            if j.email == i.email:
                dev = j
        if dev == None:                 # new dev in list
            developers[i.name] = i
        else:                           # it's a double: 2 dev with same email and different username
            print("Merge points/commit for: " + i.name + " , " + dev.name )
            for cat in dev.getKeyPoints():  # unione delle categorie di dev.cat + i.cat corrente
                dev.editPoints(cat, i.getPoints(cat))
            dev.commit += i.commit

    print("Start scraping social info for: " + str(len(developers)) + " developers.")
    max_commit = 0      # max commit of the "best" dev
    for i in developers.values():
        if i.commit > max_commit:
            max_commit = i.commit
        i.initSocialInfo(socialname)
        time.sleep(15)
        # To handle GitHub Error: Authenticated requests get a higher rate limit. Check out the documentation for more details...

    now = datetime.now()    #  2021-03-24 16:48:05.591
    timestamp = now.strftime("%m-%d-%Y_%H:%M:%S")
    filename = getRepoName(urlOrPath) + "_" + timestamp

    if CONFIG["OutputSection"]["export_as"] == "csv":
        try:
            csv_headers = ["Name", "Email", "SocialID", "SocialUsername", "AvatarURL", "WebSite", "Location", "Bio", "CreatedAt", "Commits"]
            first = list(developers.keys())  # per prendere il primo dev_key element sotto formato di lista
            firstDev = developers.get(first[0])
            for cat in firstDev.getKeyPoints(): # recupero le cat effettivamente presenti
                #print(cat)
                csv_headers.append(cat + "%")#TODO: perché non ci sono tutte le categorie specificate nel config manca undefined e java_fe

            singleline= {}

            with open(filename + ".csv", 'w') as f:
                # Header del csv
                writer = csv.DictWriter(f, fieldnames=csv_headers)
                writer.writeheader()

                for i in developers.values():
                    # calcolo totale cat lavoro effettuato dal singolo dev: 10% writer, 60% facebook, 30% frontend...
                    total = 0
                    for cat in i.getKeyPoints():
                        total += i.getPoints(cat)


                    # riga del csv
                    singleline[csv_headers[0]] = i.name  # Name
                    singleline[csv_headers[1]] = i.email  # Email
                    singleline[csv_headers[2]] = " " if (i.getId() == None) else i.getId()  # SocialID
                    singleline[csv_headers[3]] = " " if (i.getUsername() == None) else i.getUsername() # SocialUsername
                    singleline[csv_headers[4]] = " " if (i.getAvatar_url() == None) else i.getAvatar_url() # AvatarURL
                    singleline[csv_headers[5]] = " " if (i.getWebsite() == None) else i.getWebsite()  # WebSite
                    singleline[csv_headers[6]] = " " if (i.getLocation() == None) else i.getLocation()  # Location
                    singleline[csv_headers[7]] = " " if (i.getBio() == None) else i.getBio()  # Bio
                    singleline[csv_headers[8]] = " " if (i.getCreated_at() == None) else i.getCreated_at() # CreatedAt
                    singleline[csv_headers[9]] = i.commit  # Commits

                    #print("total: ",total)

                    # Percentuali: frontend%,writer%,backend%,android%,facebook%...
                    for index, cat in enumerate(i.getKeyPoints()):
                        if total !=0:
                            singleline[csv_headers[10 + index]] = round(float(i.getPoints( cat )*100/total))   # cat%
                        else:   # Errore: che dev non ha nulla di specifico per quelle categorie specificate
                            singleline[csv_headers[10 + index]] = 0  # 0%

                    writer.writerow(singleline)

            print('Csv generato')
        except ValueError:
            print(ValueError)
    elif CONFIG["OutputSection"]["export_as"] == "html":
        outputData = [] #JSONArray
        for i in developers.values():
            singleDeveloper = {}    # JSONObject

            total = 0
            for cat in i.getKeyPoints():
                total += i.getPoints(cat)

            singleDeveloper["name"] = i.name
            singleDeveloper["email"] = i.email
            singleDeveloper["id"] = (" " if (i.getId() == None) else i.getId())
            singleDeveloper["username"] = (" " if (i.getUsername() == None) else i.getUsername())
            singleDeveloper["avatar_url"] = (" " if (i.getAvatar_url() == None) else i.getAvatar_url())
            singleDeveloper["website"] = (" " if (i.getWebsite() == None) else i.getWebsite())
            singleDeveloper["location"] = (" " if (i.getLocation() == None) else i.getLocation())
            singleDeveloper["bio"] = (" " if (i.getBio() == None) else i.getBio())
            singleDeveloper["created_at"] = (" " if (i.getCreated_at() == None) else i.getCreated_at())
            singleDeveloper["commit"] = i.commit

            # commit Star
            if (i.commit > 1 and i.commit <= (max_commit / 5)):
                singleDeveloper["commit_star"] = 1
            elif (i.commit > (max_commit / 5) and i.commit <= (max_commit / 5) * 2):
                singleDeveloper["commit_star"] = 2
            elif ( i.commit > ((max_commit / 5) * 2) and i.commit <= (max_commit / 5) * 3 ):
                singleDeveloper["commit_star"] = 3
            elif ( i.commit > ((max_commit / 5) * 3) and i.commit <= (max_commit / 5) * 4 ):
                singleDeveloper["commit_star"] = 4
            elif ( i.commit > ((max_commit / 5) * 4) ):
                singleDeveloper["commit_star"] = 5

            skills = {} #JSONArray
            for cat in i.getKeyPoints():
                skills[cat] = round(float(i.getPoints(cat)*100/total))
            singleDeveloper["skills"] = skills

            # conversione JSON
            jsonSingleDeveloper = json.dumps(singleDeveloper)
            outputData.append(jsonSingleDeveloper)

        print(outputData)
        # Save Data
        try:
            with open("html/js/git_data.js", 'w') as f:
                for data in outputData:
                    f.write(data)
            zip_directory("./html", "./" + filename + ".zip")

        except ValueError:
            print(ValueError)


    else: print("Not valid output provided. Output supported: csv or html")


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