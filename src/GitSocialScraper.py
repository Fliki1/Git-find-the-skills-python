import requests

class GitSocialScraper:
    socialname = None

    def __init__(self, socialname: str):
        self.socialname = socialname

    def makeRequest(self, url_string):
        """ Get of url_string, return a JSON response or None """
        myResponse = {}
        try:
            con = requests.get(url_string, timeout=15)  # timer di risposta di 10 secondi else None
        except requests.exceptions.ConnectionError:
            print("TIMEOUT request")
        if con.ok:
            myResponse = con.json()
            return myResponse
        return None

    def getInfo(self, email:str):
        if self.socialname == "github":
            user_result = {}
            try:
                #1 - Search user by email
                user_result = self.makeRequest(f"https://api.github.com/search/users?q={email}+in:email")

                """ Modello JSON Vuota
                    {
                      "total_count": 0,
                      "incomplete_results": false,
                      "items": [ ]
                    }
                """
                # se non funziona provare la condizione user_result['items'] != 0
                if user_result != None and user_result['total_count'] > 0:  # Se la GET ha avuto esito e la JSON non è vuota
                    info ={}
                    user = user_result['items'][0]
                    socialid = user['id']

                    info["id"] = user["id"]
                    info["username"] = user["login"]
                    info["avatar_url"] = user["avatar_url"]

                    # 2 - Get full info by id
                    fullinfo = self.makeRequest( f"https://api.github.com/user/{socialid}" )
                    if fullinfo != None:
                        info["website"] = fullinfo["blog"]
                        info["location"] = None if ("location" not in fullinfo) else fullinfo["location"] # controllare meglio Java: fullinfo.isNull("location")
                        info["bio"] = None if (fullinfo['bio'] == 'null') else fullinfo["bio"]
                        info["created_at"] = fullinfo["created_at"]
                        return info
                    return None
            except ValueError:
                print(ValueError)
        elif self.socialname == "bitbucket":
            """ Anche qui richiede una autorizzazione, possibile gestione della chiamata come sotto
            fullinfo = {}
            try:
                # 1 - Search user by email
                fullinfo = self.makeRequest(f"https://api.bitbucket.org/2.0/user/emails/{email}")
                                            # anche il formato https://api.bitbucket.org/2.0/user/ + email
                if fullinfo != None:
                    info = {}
                    info["id"] = fullinfo["account_id"]
                    info["username"] = fullinfo["nickname"]
                    print(info)
                    links = fullinfo['links']
                    avatarl_url = links['avatar']['href']
                    info["avatar_url"] = avatarl_url

                    info["website"] = None
                    info["location"] = None
                    info["bio"] = None
                    info["created_at"] = fullinfo["created_on"]
                    print(info)
                    return info
                return None
            except ValueError:
                print(ValueError)
            """
            return None
        elif self.socialname == "gitlab":
            """ Anche qui richiede una autorizzazione, possibile gestione della chiamata come sotto """
            fullinfo = {}
            try:
                #1 - Search user by email
                fullinfo = self.makeRequest(f"https://gitlab.com/api/v4/users?email={email}")
                                            # https://gitlab.com/api/v4/users?search=name      /users?username=:username
                #print(fullinfo)-> None
                if fullinfo != None:    # auth required for GitLab :(
                    info = {}
                    info["id"] = fullinfo["account_id"]
                    info["username"] = fullinfo["nickname"]
                    print(info)
                    links = fullinfo['links']
                    avatarl_url = links['avatar']['href']
                    info["avatar_url"] = avatarl_url

                    info["website"] = None
                    info["location"] = None
                    info["bio"] = None
                    info["created_at"] = fullinfo["created_on"]
                    print(info)
                    return info
                return None
            except ValueError:
                print(ValueError)
        return None

    """ Qualcosa del tipo: 
        r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
        r.status_code    
        >>200
        r.headers['content-type']
        >>'application/json; charset= utf8
        r.encoding
        >>'utf-8'
        r.text
        >> u'{"type":"User"...'
        r.json()
        >>{u'private_gists': 419, u'total_private_repos': 77, ...}
    """

