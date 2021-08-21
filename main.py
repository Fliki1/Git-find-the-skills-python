import configparser
import sys
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


if __name__ == '__main__':
    try:
        CONFIG.read('ConfigFile.properties')
    except ValueError:
        print(ValueError)

    if validatePropertiesSkills() == False:     # ConfigFile.properties: wrong or empty fields
        sys.exit(0)

    #TODO: start the metric
    p1 = DevelopersVisitor.DevelopersVisitor(CONFIG)
    #p1.myfunc()
    #p1.checkIfFileHasExtension("testaciao", ["tavolo","sedia","comodinociao", "ciao"])
    p1.process('https://github.com/devopstrainingblr/Maven-Java-Project.git')
    print("this is the end")
    del p1
