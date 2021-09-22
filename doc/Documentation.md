# Code documentation Git-find-the-skills-python

Il progetto ha come obiettivo quello di convertire il codice già
realizzato dal Alessandro Maggio da Java ☕ in Python 🐍

Di seguito ne riporto tutte le scelte implementative e struttura
del codice.

### 1 Config.properties
Come fase iniziale del progetto viene preso in considerazione
un file di supporto per gestire l'analisi del repository. Il file
[Config.properties](ConfigFile.properties) permette di personalizzare
l'analisi in base al linguaggio di programmazione e delle librerie
utilizzate nel progetto. Alcuni campi sono obligatori e necessari
per l'esecuzione dello script, altri invece permettono appunto di avere 
un'analisi più accurata.

Il file è suddivisio in sezioni: _RepositorySection_, _SkillsSection_,
_OutputSection_ corrispondenti ai distinti campi.

#### RepositorySection
- **repository**: indirizzo HTTP del repository da analizzare oppure il path globale della repo clonata
#### SkillsSection
- **backend**: lista di estensioni da categorizzare come backend
- **frontend**: lista di estensioni da categorizzare come frontend
- **writer**: lista di estensioni da categorizzare come writer
- **undefined**: lista di tutte le estensioni con categoria dubbia. All’interno dello
script le estensioni come .js, .java e .php vengono trattate in maniera adeguata e
categorizzate correttamente pur essendo undefined
- **java_fe**: lista di packages Java dedicate al frontend
- **...**: ulteriori categorie possono essere inserite per il linguaggio Java semplicemente
scrivendo nomecat=pkg1;pkg2;pkg3
#### OutputSection
- **export_as**: indica la tipologia di output desiderata: csv o _html_
<!---
Se si sceglie HTML verrà creato un archivio .zip contente il 
file index.html e i relativi .js, .css in modo tale da
avere una rappresentazione "grafica" dell’analisi effettuata.
Se si sceglie .csv verrà realizzato un file con la medesima estensione.
-->
 
>Nota: utilizzare il carattere **;** per differenziare le varie librerie/estensioni.
##### Esempio di file Config.properties
```
[RepositorySection]
repository=https://github.com/Tkd-Alex/GIT-Find-The-Skills.git

[SkillsSection]
backend=sh;py;c;cpp;go
frontend=css;scss;html;ts;ui;kt
writer=pdf;md;txt;tex
undefined=php;java;js
java_fe:javax.swing;java.awt;com.lowagie;org.xml;android.view
android:android.app;android.content;android.net;androidx.annotation;android.database;android.support;android.os;android.test;android.util
facebook:com.facebook

[OutputSection]
export_as:csv
```

### 2. main

La prima cosa da validare è il contenuto di Config.properties.
Un Try Catch è usato per verificare se è presente [ConfigFile.properties](../ConfigFile.properties) nella
directory. Un errore verrà stampato altrimenti.

**_validatePropertiesSkills()_**: verifica se i campi principali della 
lettura di [ConfigFile.properties](../ConfigFile.properties) in CONFIG:
- "RepositorySection", 
- "SkillsSection", 
- "OutputSection"

sono presenti all'interno del file .properties.
Il metodo controlla se il contenuto delle key di riferimento alle sezioni
non siano vuote: `""` o `None` e altresì controlla se i campi: "backend", "frontend", "writer", "undefined"
contengano almeno un valore.
In base all'esito del metodo (True/False) l'applicazione si ferma: `sys.exit(0)`

Successivamenta a questo controllo si istanzia [DeveloperVisitor](../src/DevelopersVisitor.py)
Mentre in Java si controllava se l'urlOrPath corrispondente al repository fosse
un url remoto o un path locale, in Python questo controllo non si necessita e si
esegue direttamente il metodo **_process_**

L'analisi del repository viene effettuata escludendo i Merge commit.

❗ <span style="color:OrangeRed">Una differenza notata con Java nella fase di testing: Java non considera certi commit.
Non sono riuscito a capire per quale ragione. Caso d'uso 
`https://github.com/Tkd-Alex/GIT-Find-The-Skills.git` con attualmente 22 commit
ne vengono valutati 21 in Python e 20 in Java escludendo un autore.
Evita un: `Bump jsoup from 1.11.3 to 1.14.2 in /gittocv Signed-off-by: dependabot[bot] <support@github.com>` 
che ne aggiorna le dipendenze.</span>

**_getSocialName(urlorPath)_**: in base al tipo di repository stabilito da 
urlorPath (se remoto o locare) determina e ritorna il dominio del repository
di lavoro: github, gitlab..

Una volta ottenuto la lista dei developers, si procede a verificare ed eliminare
i possibili account duplicati. In quanto potrebbero esserci commit effettuati 
dallo stesso user(user.email) con nick diversi(user.name). Si rimuovo i duplicati
facendo un merge dei valori delle loro categorie associate e del numero di commit
effettuati.

_max_commit_ rappresenta il numero di commit massimo raggiunto tra tutti i developers.
Servirà, se si sceglie il formato html, a calcolare un rate in stelle per determinare 
un andamento ed effort tra tutti gli sviluppatori che hanno collaborato nel progetto.
Contemporaneamente **_initSocialInfo(socialname)_**: determina e salva le informazioni
social reperibili dal developer di turno: 'id', 'username', 'avatar_url', 'website', 
'location', 'bio', 'created_at'.

Se è stato specificato di esportare i dati nel formato **csv**.
Si determinano le categorie effettivamente trovate nel repository,
prendendo le info di un developer (il primo). 
Es: android, facebook, backend, writer, frontend
(vengono trattati diversamente: java_fe, undefined)

❗ <span style="color:OrangeRed"> Analizzando i risultati ottenuti per l'analisi
delle singole categorie ho scoperto che nella versione JAVA i conteggi non sono
del tutto corretti. Nell'esempio https://github.com/Tkd-Alex/GIT-Find-The-Skills.git
in corrispondenza del `commit fca941c046f81e39e30d380983bd421912a9094d` Java riporta un
incremento della categoria "frontend" di 0 che per costruzione diventa pari a 1.
Seguendo il commit segnalato invece si può ben vedere come la modifica effettuata incrementa
il numero di linee aggiunte di 5923. Così come le successive modifiche di 10 e 5905...
</span>
![plot](Schermata%20da%202021-09-12%2000-58-45.png)
Su un file.csv nominato con il nome del repository e un timestamp si salva il tutto.
![plot](Immagine%202021-09-13%20135309.png)

Se è stato specificato di esportare i dati nel formato **html**.
Si genera un JSON contenente le stesse informazioni ottenibili nel formato csv.
A differenza di Java, in Python i campi non sono ordinati.

Per ciascun developer si recuperano le sue bio info, la sua percentuale di effort per 
categoria specificata e uno star rate per indicare sul totale dei commit effettuati
quanto è stato il suo contributo nel repository.

Il tutto viene salvato in uno zip file contenenti anche altri elementi per una 
rappresentazione web degli esiti ottenuti. (solo su windows a quanto pare)

### 3. DevelopersVisitor
[DevelopersVisitor](../src/DevelopersVisitor.py) classe che gestisce la metrica, prende come input
un riferimento a ConfigFile.properties dal quale ne ricava i parametri settati.

Salva in:
- **CONFIG**: un riferimento al ConfigFile
- **developers**: un dizionario chiave valore _(str, Developer)_
- **fileExstensions**: un dizionario chiave valore _(str, str[])_
dei campi backend-frontend-writer-undefined separati da `;` in lowercase
> {'backend': ['sh', 'py', 'c', 'cpp', 'go'], 'frontend': ['css', 'scss', 'html', 'ts', 'ui', 'kt'], 'writer': ['pdf', 'md', 'txt', 'tex'], 'undefined': ['php', 'java', 'js']}
- **java_fe**: list string delle librerie specificate nel ConfigFile separate da `;`
in lowercase
> ['javax.swing', 'java.awt', 'com.lowagie', 'org.xml', 'android.view']

**_process(url)_**: Per ciascun commit nel repository si recupera il suo autore. Se non è un
developer già trattato, viene creato un nuovo [Developer](../src/Developer.py) di riferimento e
salvato opportunamente incrementando il suo numero di commit effettuati.

**_updatePoint(dev, mod)_**: Parallelamente per ogni modifica presente nello stesso commit si conteggiano 
e aggiornano il numero di punti del developer. Il conteggio viene effettuato
verificando la tipologia di file modificato, in base alla sua estensione (sh, html, pdf...), 
incrementando nella categoria opportuna(backend, frontend, writer, undefined) 
il numero di righe che sono state aggiunte al file, +1 altrimenti se è stato 
creato il file o non sono stati aggiunte righe di modifica.

Lo studio delle categorie "undefined" cerca di comprendere se i file con estensione
php, java e js possiedano elementi per poter stabilire a quale delle due categorie backend o frontend
appartengano. L'analisi viene effettuata approfondendo la tipologia
di librerie importate nei file, in base a quale classificazione e ambiti di librerie ha 
importato chi si può dare un'ipotesi sulle capacità dello sviluppatore.

Sempre nelle ExtraCategorie vengono gestite e soppesate il totale dei punteggi per ciascuna 
di esse, gestendo anche un eventuale pari merito tra più categorie suddividendone il peso su queste ultime.

### 4. Developers
Developers rappresenta una struttura che salva tutte le informazioni di un Autore del commit.

**_initExtraCategory(CONFIG)_**: permette di salvare le categorie extra a quelli basilari (frontend, writer, backend)

**_initSocialInfo(socialname)_**: salva nella struttura dati le informazioni social a partire dall'email

### 5. WebScraper 
Per la gestione dei package di Java e JavaScript, ci si affida al sito https://www.npmjs.com/package/
il quale specificando il nome del package ne darà tutte le informazioni utili.

Per leggere il sito: ci si affida ad un HTML Parser `BeautifulSoup`.

Dalla lettura del paragrafo "readme" del sito, se contiene la parola: _node.js_, il
package in questione viene trattato come **backend** altrimenti **frontend**.


### 6. GitSocialScraper 
E' la classe che gestire le REST API call per ottenere le sole informazioni
social del team di sviluppo dei repository di turno.

REST API are very common for web services. GitHub, GitLab, Bitbucket support it.
A user client construct an HTTP request (GET, POST, PUT, DELETE), that request 
goes to the web server and a response comes back. 
There are different format but JSON is pretty common use.

**_makeRequest(url_string)_**: effettua la chiamata GET. L'url passato come input
sarà già strutturato e parametrizzato opportunamente in base alle API di GitHub,
GitLab o Bitbucket opportune specificandone l'email/id/username dello sviluppatore.
L'esito riporta le informazioni dello sviluppatore in formato JSON, None altrimenti.

**_getInfo(email)_**: recupera le informazioni dei developers:
* id
* username
* avatar_url
* website
* location
* bio
* created_at

Informazioni utilizzati nell'esito degli effort di ciascuno developer.
(Nelle successive ho raccolto una sintesi dei passaggi effettuttati e
dalle documentazioni non ottenendo i risultati sperati: richiedono
l'autorizzazione con token del proprietario stesso)

#### GitHub
Ricerca le informazioni partendo dall'email dell'utente. Solo una volta, se
l'esito è non nullo, approfondisce ulteriormente le ricerche cercando per id.

#### GitLab
> Credenziali: apirepository67@gmail.com Tantoper

[GitLab API DOC](https://docs.gitlab.com/ee/api/)
[YT](https://www.youtube.com/watch?v=0LsMC3ZiXkA&ab_channel=GitLabUnfiltered)

Per interagire con GitLab usando le REST API bisogna fare riferimento a un modello 
di url basilare cui porre le varie requests.
`"https://gitlab.example.com/api/v4/projects"`
In base alle richieste da effettuare si aggiungeranno dei campi all'url opportunamente
al fine di interfacciarsi con la parte di GitLab di interesse.

E' possibile ottenere le public information senza l'ausilio di una Auth token, ma
esiste il "project token owner" per avere più informazioni a riguardo di quel
specifico repository. L'authkey è un personal access token per autenticarsi 
con GitLab associato all'utente del repository di studio.

Le chiamate requests relative alle informazioni vengono riconosciute (200 status)
ma riportano esito nullo perché non si è autorizzati.

#### Bitbucket
> Credenziali: apirepository67@gmail.com Tantoper

A causa di restrizioni: Bitbucket Cloud REST API version 1 is deprecated 
effective 30 June 2018, and were removed from the REST API permanently on 
29 April 2019.

Si necessita di avere delle credenziali di accesso o token OAuth 2.0
per poter invocare certe richieste.

[Bitbucket OAuth Documentation](https://support.atlassian.com/bitbucket-cloud/docs/use-oauth-on-bitbucket-cloud/)

[REST API 1.0 Resources Provided By: Bitbucket Server](https://docs.atlassian.com/bitbucket-server/rest/5.16.0/bitbucket-rest.html)

[Bitbucket API: Authentication methods](https://developer.atlassian.com/bitbucket/api/2/reference/meta/authentication)

##### Come creare un Access Token
Bisogna creare un repository su Bitbucket, entrare nei settings del repository,
sotto la voce "Apps and Features" accedere al campo OAuth consumers.

Nel creare un nuovo Consumer, si richiedono dei campi da riempire:
* Name
* Description
* Callback URL
* Permission: ho messo Email e Read

##### Access tokens
`https://bitbucket.org/site/oauth2/authorize?client_id={client_id}&response_type=code`

Bisogna dare autorizzazione a questo link passandovi il client_id specifico
`aw4faLG4T7pkvMNMzd` rimanda alla urlcall inserita nella creazione del consumers.

L'access tokens è un token il quale permette una volta ottenuto di poter effettuare poi
le successive chiamate di GET e POST opportune con esso. L'access tokens ha un limitato
numero di utilizzi di 7200 per ora, una volta scaduto è di utile norma rinnovarlo.

Per chiedere l'access tokens:

`$ curl -X POST -u "client_id:secret" https://bitbucket.org/site/oauth2/access_token
  -d grant_type=authorization_code -d code={code}`

Nei test effettuati in ipynb non sono riuscito ad ottenere l'access tokens.
Ripotando solo 400(Bad Request), 401(Unauthorized), 403(Forbidden).

L'idea era di utilizzare la chiamata:
`https://api.bitbucket.org/2.0/users/{selected_user}`
>Gets the public information associated with a user account.
If the user's profile is private, location, website and created_on elements are omitted.
Note that the user object returned by this operation is changing significantly, due to privacy changes. See the announcement for details.
[link](https://developer.atlassian.com/bitbucket/api/2/reference/resource/users/%7Bselected_user%7D)

Oppure:
`https://api.bitbucket.org/2.0/2.0/user/emails/{email}}` come da originale progetto Java nonostante
>Returns details about a specific one of the authenticated user's email addresses.
Details describe whether the address has been confirmed by the user and whether it is the user's primary address or not.
[link](https://developer.atlassian.com/bitbucket/api/2/reference/resource/user/emails/%7Bemail%7D)

Note: [stack1](https://stackoverflow.com/questions/44832338/bitbucket-api-returns-bad-request-when-using-python-requests)
[stack2](https://stackoverflow.com/questions/61519360/can-acces-bitbucket-private-repository-with-curl-but-not-with-python)
[stack3](https://stackoverflow.com/questions/66832797/how-to-authenticate-to-bitbucket-cloud-apis-and-then-use-them-post-authenticatio)
[POSTpythondoc](https://docs.python-requests.org/en/master/user/quickstart/#more-complicated-post-requests)
[Youtube](https://www.youtube.com/watch?v=rb_SZE6Sh20&ab_channel=TechJam) (usa Postman per le request call)

Non sono riuscito a generare un auth token dovuto a cattiva 
mia gestione delle chiamate GET, ma questo non risolve il fatto che 
si necessita comunque del token corrispettivo al repository sotto analisi. (anche qui)