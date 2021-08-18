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

|| Nota: utilizzare il carattere **;** per differenziare le varie librerie/estensioni.
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
Try Catch per verificare se è presente ConfigFile.properties nella
directory.

**validatePropertiesSkills()** verifica se i campi principali: "RepositorySection", "SkillsSection", "OutputSection"
sono presenti all'interno del file properties.
Se qualunque di questi campi è vuoto l'applicazione si ferma.

Successivamenta a questo controllo si eseguono...

