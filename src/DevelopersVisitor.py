import configparser
import re
from src import Developer
from pydriller import Repository


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
        # Oppure: This method returns the match object if there is a match found in the string.
        #re.search(regex, text)


    def convertToLowerCase(self, strings: []):
        """ ritorna la lista di stringhe senza spazi agli estremi: strim->strip e in lowercase"""
        return [string.strip().lower() for string in strings]


    def getOnlyAdditions(self, mod):
        """ lista string di soli ADD dalla mod corrente """
        lines = mod.diff.split("\n")
        ret = []
        for addition in lines:
            if not addition.startswith("++") and addition.startswith("+"):
                ret.append( addition.replace("+", "").replace("\n"," ").strip() )
        return ret


    def getImportsJava(self, lines: []):
        """ gestione degli import Java type """
        imports = []
        for line in lines:
            if line.startwith("import") and len(line.split(".")) > 1:    # import java.awt.BorderLayout;
                imports.append((line.split(".")[0].replace("import", "") + "." + line.split(".")[1]).replace(";+$", "").strip())
        return imports  # NON è ordinato come in java credo

    """ https://developer.mozilla.org/it/docs/Web/JavaScript/Reference/Statements/import
        import defaultExport from "module-name";
        import * as name from "module-name";
        import { export1 } from "module-name";
        import { export1 as alias1 } from "module-name";
        import { export1 , export2 } from "module-name";
        import { export1 , export2 as alias2 , [...] } from "module-name";
        import defaultExport, { export1 [ , [...] ] } from "module-name";
        import defaultExport, * as name from "module-name";
        import "module-name";
        var promise = import("module-name");
    """

    def updatePoint(self, dev: Developer, mod):
        for i in self.fileExstensions.keys():
            if i != "undefined":
                if self.checkIfFileHasExtension(mod.filename, self.fileExstensions.get(i)):
                    dev.editPoints(i, (1 if mod.added_lines == 0 else mod.added_lines))
            else:
                for ext in self.fileExstensions.get(i):
                    if mod.filename.endswith(ext):
                        if ext == "php":
                            if self.hasHTMLTags(mod.source_code):
                                dev.editPoints("frontend", (1 if mod.added_lines == 0 else mod.added_lines))
                            else:
                                dev.editPoints("backend", (1 if mod.added_lines == 0 else mod.added_lines))
                        elif ext == "java" or ext == "js":
                            imports = []
                            additions = self.getOnlyAdditions(mod)
                            # webscraper





    def process(self, url):
        """ processo di lavoro """
        for commit in Repository(path_to_repo=url, only_no_merge=True).traverse_commits():
            # Check if the dic contains already the developer (by name), else create a new instance of Developer.
            contains = commit.author.name in self.developers.keys()
            if not contains:
                newDev = Developer.Developer(commit.author.name, commit.author.email)
                newDev.initExtraCategory(self.CONFIG)
                self.developers[commit.author.name] = newDev
            dev = self.developers.get(commit.author.name)
            dev.commit +=1

            for mod in commit.modified_files:
                self.updatePoint(dev, mod)
