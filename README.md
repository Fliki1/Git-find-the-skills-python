# Git-find-the-skills-python
[![en](https://img.shields.io/badge/lang-en-green)](README.en.md)

Il progetto GIT-Find-The-Skills ha come obiettivo principale
la classificazione dei committer presenti all’interno di una 
determinata repository git. Ogni utente può aver collaborato 
in maniera differente all’interno del progetto, in particolare 
può aver occupato un posto principale come: backend, frontend,
oppure writer e dunque si è dedicato principalmente alla 
documentazione del progetto stesso.

## Problemi riscontratri nella conversione:
#### Filter and sort API objects
You can query the 2.0 API for specific objects using a simple language which resembles SQL.
> Note that filtering and querying by username has been deprecated, due to privacy changes. See the announcement for details.

Fonte:
https://developer.atlassian.com/bitbucket/api/2/reference/meta/filtering

Vuole una Token API OAuth

Fonte di repository Bitbucket: https://bitbucket.org/repo/all


Sto trovando difficoltà a testare l'efficacia di quanto implementato:

* getImportsJAVASCRIPT call "come funzionano gli import e require in JavaScript?"

### Requests
beautifulsoup4
pydriller
#### TODO:
* nella gestione degli import in java ho trovato casi del tipo 
`import static com.google.common.collect.Multimaps.*;`
ho gestito rimuovendo anche 'static' nel filtro per la libreria
* gestire repository di Gitlab
  * sembrava fattibile, ma riporta uno status 200 con esito vuoto {[]}
* gestire repository di Bitbucket
  * non riesco a reperire nemmeno l'access token: qualcosa di assurdo