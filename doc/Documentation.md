# Code documentation Git-find-the-skills-python

Il progetto ha come obiettivo quello di convertire il codice già
realizzato dal Alessandro Maggio in Java ☕ in Python 🐍

Di seguito ne riporto tutte le scelte implementative e struttura
del codice implementato.

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
#### OutputSection
- **export_as**: indica la tipologia di output desiderata: csv o _html_
<!---
Se si sceglie HTML verrà creato un archivio .zip contente il 
file index.html e i relativi .js, .css in modo tale da
avere una rappresentazione "grafica" dell’analisi effettuata.
Se si sceglie .csv verrà realizzato un file con la medesima estensione.
-->
#### Extra??
- **...**: ulteriori categorie possono essere inserite per il linguaggio Java semplicemente
scrivendo nomecat=pkg1;pkg2;pkg3
 
>Nota: utilizzare il carattere **;** per differenziare le varie librerie/estensioni.
##### Esempio del file Config.properties
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
Try Catch per verificare se è presente [ConfigFile.properties](../ConfigFile.properties) nella
directory. Un errore verrà stampato altrimenti.

**_validatePropertiesSkills()_**: verifica se i campi principali della 
lettura di [ConfigFile.properties](../ConfigFile.properties) in CONFIG:
- "RepositorySection", 
- "SkillsSection", 
- "OutputSection"

sono presenti all'interno del file .properties.
Il metodo controlla se il contenuto delle key di riferimento alle sezioni
non siano vuote: `""` o `None`

e altresì controlla se i campi: "backend", "frontend", "writer", "undefined"
contengano almeno un valore.
In base all'esito del metodo (True/False) l'applicazione si ferma: `sys.exit(0)`

Successivamenta a questo controllo si istanzia [DeveloperVisitor](../src/DevelopersVisitor.py)
Mentre in Java si controllava se l'urlOrPath corrispondente al repository fosse
un url remoto o un path locale, in Python questo controllo non si necessita e si
esegue direttamente il metodo **_process_**

L'analisi del repository viene effettuata escludendo i Merge commit.

Nota ❗ <span style="color:OrangeRed">Una differenza notata con Java nella fase di testing: Java non considera certi commit.
Non sono riuscito a capire per quale ragione. Caso d'uso 
`https://github.com/Tkd-Alex/GIT-Find-The-Skills.git` con attualmente 22 commit
ne vengono valutati 21 in Python e 20 in Java escludendo un autore.
Evita un: Bump jsoup from 1.11.3 to 1.14.2 in /gittocv effettuato proprio 
da: Signed-off-by: dependabot[bot] <support@github.com> che ne aggiorna le dipendenze.</span>.

**_getSocialName(urlorPath)_**: in base al tipo di repository stabilito da 
urlorPath(se remoto o locare) determina e ritorna il dominio del repository
di lavoro: github, gitlab..

Una volta ottenuto la lista dei developers, si procede a verificare ed eliminare
i possibili account duplicati. In quanto potrebbero esserci commit effettuati 
dallo stesso user(user.email) con nick diversi(user.name). Si rimuovo i duplicati
facendo un merge dei valori delle loro categorie associate e del numero di commit
effettuati.

_max_commit_ rappresenta il numero di commit massimo raggiunto tra tutti i developers
servirà a calcolare un rate in stelle per determinare un andamamento ed effort
tra gli sviluppatori.
Contemporaneamente **_initSocialInfo(socialname)_**: determina e salva le informazioni
social reperibili dall'developer di turno: 'id', 'username', 'avatar_url', 'website', 
'location', 'bio', 'created_at'.

Se è stato specificato di esportare i dati nel formato csv.
Si determinano le categorie effettivamente trovate nel repository,
prendendo le info di un developer (il primo). 
Es: android, facebook, backend, writer, frontend
(rispetto al totale delle categorie specificate: java_fe, undefined, )

perché non tutte?


### 3. DevelopersVisitor
DevelopersVisitor classe che gestisce la metrica, prende come input
un riferimento a ConfigFile.properties dal quale ne ricava i parametri settati.

Salva in:
- **CONFIG**: un riferimento al ConfigFile
- **developers**: un dizionario chiave valore (str, Developer)
- **fileExstensions**: un dizionario chiave valore (str, str[])
dei campi backend-frontend-writer-undefined separati da `;` in lowercase
> {'backend': ['sh', 'py', 'c', 'cpp', 'go'], 'frontend': ['css', 'scss', 'html', 'ts', 'ui', 'kt'], 'writer': ['pdf', 'md', 'txt', 'tex'], 'undefined': ['php', 'java', 'js']}
- **java_fe**: list string delle librerie specificate nel ConfigFile separate da `;`
in lowercase
> ['javax.swing', 'java.awt', 'com.lowagie', 'org.xml', 'android.view']

### X. WebScraper
Per la gestione dei package di Java e JavaScript, ci si affida al sito https://www.npmjs.com/package/
il quale specificando il nome del package ne darà tutte le informazioni utili.

Per leggere il sito: ci si affida a un HTML Parser `BeautifulSoup`.

Viene letto il campo "readme" del sito, se ne contiene la parola: _node.js_, il
package in questione viene trattato come **backend** altrimenti **frontend**