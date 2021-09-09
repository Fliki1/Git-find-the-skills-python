import configparser
import re
from src import Developer, WebScraper
from pydriller import Repository


class DevelopersVisitor:

    def __init__(self, CONFIG: configparser): # ok
        self.CONFIG = CONFIG
        self.developers = {}        # str, Developer
        self.fileExstensions = {}   # str, str[]
        self.java_fe = list(CONFIG.get("SkillsSection", "java_fe").lower().split(";"))

        for type in ["backend", "frontend", "writer", "undefined"]:
            exstensions = list(CONFIG.get("SkillsSection", type).lower().split(";"))
            self.fileExstensions[type] = exstensions

        self.HTML_PATTERN = r"<(\"[^\"]*\"|'[^']*'|[^'\">])*>" # changed
        self.pattern = re.compile(self.HTML_PATTERN)
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
        return self.pattern.match(text)
        # re.match(self.HTML_PATTERN, text)

        # Oppure: This method returns the match object if there is a match found in the string.
        # re.search(regex, text)


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
            if line.startswith("import") and len(line.split(".")) > 1:    # import java.awt.BorderLayout;
                #print("in: getImportsJava")
                #print("line: ", line)
                #print("line.startswith('import')", line.startswith("import"))
                #print("len(line.split('.') > 1", len(line.split("."))>1)
                # TODO: ho trovato casi del tipo import static com.google.common.collect.Multimaps.*;
                imports.append((line.split(".")[0].replace("import", "").replace("static", "") + "." + line.split(".")[1]).replace(";+$", "").strip())
                #print("=========================================")
        #print("ritorna: ", imports)
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

    def getImportsJAVASCRIPT(self, lines: []):
        imports = []
        for line in lines:
            if (line.strip().startswith("import") or line.strip().startswith("require")) and not "/" in line:
                #print("in: getImportsJAVASCRIPT")
                #print("line: ", line)
                #print("(line.strip().startswith('import')", (line.strip().startswith("import")))
                #print("line.strip().startswith('require')", line.strip().startswith("require"))
                #print("not / in line")
                p = re.compile(r"\"([^\"]*)\"")
                #print(p)
                m = p.match(line.replace("'", "\""))
                #print("m", m)
                if m:   # In actual programs, the most common style is to store the match object in a variable, and then check if it was None
                    for i in m: # for i, c in enumerate(m): ----> group(i)? oppure finditer() e for su di esso
                        imports.append(m.group(1))
                #print("=========================================")
        return imports

    def updatePoint(self, dev: Developer, mod):
        for i in self.fileExstensions.keys():
            if i != "undefined":
                if self.checkIfFileHasExtension(mod.filename, self.fileExstensions.get(i)):
                    dev.editPoints(i, (1 if mod.added_lines == 0 else mod.added_lines))
            else:
                for ext in self.fileExstensions.get(i):
                    if mod.filename.endswith(ext):  # Modifica effettuata su un tag di studio
                        if ext == "php":
                            if self.hasHTMLTags(mod.source_code):
                                dev.editPoints("frontend", (1 if mod.added_lines == 0 else mod.added_lines))
                            else:
                                dev.editPoints("backend", (1 if mod.added_lines == 0 else mod.added_lines))
                        elif ext == "java" or ext == "js":
                            imports = []
                            additions = self.getOnlyAdditions(mod)
                            webscraper = WebScraper.WebScraper("js")
                            #print(webscraper.classifyImport("request"))

                            if ext == "java":
                                imports = self.getImportsJava(additions)
                            else:
                                imports = self.getImportsJAVASCRIPT(additions)

                            hasBackendLib = False
                            categoryFile = {}
                            packageIdentified = []

                            categoryFile["backend"] = 0
                            #print("imports ",imports)

                            for imp in imports:
                                if ext == "java":
                                    # The properties file have extraCategory?
                                    if len(dev.extraCategory) == 0: # No extraCategory, default category
                                        type = "frontend" if imp.lower() in self.java_fe else "backend"
                                        if type != None and type == "backend":
                                            hasBackendLib = True
                                            break # Other points are linked by file extension. 1File => 1Point, break the loop (limit request)
                                    else:
                                        for cat in dev.getKeyPoints():
                                            currentPackages = []
                                            if cat == "frontend":
                                                currentPackages = self.java_fe
                                            elif cat != "frontend":
                                                lista = self.CONFIG["SkillsSection"][cat].split(";")    # packages list
                                                currentPackages = (map (lambda x: x.lower(), lista))        # even lower list

                                            if cat != "backend":
                                                if imp.lower() in currentPackages:
                                                    if categoryFile.get(cat) == None:   # vedere se mod in categoryFile[cat] == 0
                                                        categoryFile[cat] = 0
                                                    categoryFile[cat] = categoryFile.get(cat) + 1
                                                    packageIdentified.append(imp)

                                        if imp not in packageIdentified:
                                            categoryFile["backend"] = categoryFile.get("backend") + 1

                                else:   # ext != java
                                    type = webscraper.classifyImport(imp)
                                    if type != None and type == "backend":
                                        hasBackendLib = True
                                        break 	# Other points are linked by file extension. 1File => 1Point, break the loop (limit request)



                            if ext == "js" or len(dev.extraCategory) == 0: # Standard method for js file or java with default category
                                if hasBackendLib == False:
                                    dev.editPoints("frontend", (1 if mod.added_lines == 0 else mod.added_lines))
                                else:
                                    dev.editPoints("backend", (1 if mod.added_lines == 0 else mod.added_lines))
                            else:
                                """
                                     Just do it!
                                     If we have extraCategory get the max value of categoryFile, for example
                                     { android: 5, database: 2, other: 1 } , max = 5
                                     Assign 1 point * modification (example: 1000) at category android 
                                     Case: category with same point
                                     { android: 5, database: 5, other: 1 } , max = 5
                                     Assign 1 point * modification/same_category (example: 1000/2) at category android 
                                     and database 
                                """
                                #print(categoryFile)
                                massimo = max(categoryFile.values())
                                #print(massimo)
                                maxKeys = []
                                for entry in categoryFile:
                                    if categoryFile[entry] == massimo:
                                        maxKeys.append(entry)
                                #print(maxKeys)
                                if len(maxKeys) == 1:
                                    dev.editPoints(maxKeys[0], (1 if mod.added_lines == 0 else mod.added_lines))
                                else:
                                    for cat in maxKeys:
                                        dev.editPoints(cat, (1 if mod.added_lines == 0 else round(mod.added_lines/len(maxKeys))))





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
            dev.commit += 1

            for mod in commit.modified_files:
                # print(commit.hash)
                # print(commit.msg)
                self.updatePoint(dev, mod)
