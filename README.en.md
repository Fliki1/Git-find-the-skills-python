# Git-find-the-skills-python
[![it](https://img.shields.io/badge/lang-it-blue)](README.md)

The aim of the metric is the classification of the committers on a given GitHub
repository. The need derives from the disparity on team roles present in a
project.


The developers skills are highlighted by categorizing the work into three macro
categories: _backend_, _frontend_ and _writer_. 

The programming language, the libraries
and the file extension used in the repository are taken as a reference to
analyze the project:
* **Writer**: pdf, txt, md, etc.;
* **Frontend**: css, php, html, etc.; 
* **Backend**: sh, c, py, etc. 

There is an additional **undefined** category which
stand for extensions supposed to be present in the repository but you want to
exclude from the analysis.

In addition to these macro categories, there is the possibility
of include additional **extra** categories by specifying their scope and associable
use libraries that you expect to find: e.g. android, facebook, etc.

The final results can be saved in a csv or html format.

### Setup

Edit the file [config.properties](ConfigFile.properties) as you need:

* **repository** https address of the repository
* **backend** list of extensions to classify as backend
* **frontend** list of extensions to classify as frontend
* **writer** list of extensions to classify as writer
* **java_fe** list of Java packages to classify as frontend
* **export_as** html/csv

### Process
The metric at the first step searches for all repository commit authors.
Developer
list serves to filter possible duplicate accounts. Since there can be
commits made by the same user (user.email) with different aliases (user.name).
Once obtained the different authors whose contributed to the project, the metric
determines a trend effort among all developers.

To define the effort of developers, each committer is assigned scores for each
category. The scores are then converted into a percentage of the total work
done into the repository. The score corresponds to the number of modifications
made in the commit history that satisfy the requests specified in the config file.
Specifically, once the commit author is established, the number of changes made
to the code lines is counted.

### Output
* HTML is a web page that contanis a card for each user and the relative data:
  * Name
  * Email
  * Number of commits (analyzed)
  * Rating star to indicate the amount of contribution related to total commit
  * Percentage for each category
  * Extra 'social' info
  
Use case [CNF cnf-testbed](https://github.com/cncf/cnf-testbed)

![](/home/leo/Scrivania/Python Projects/Git-find-the-skills-python/images/html.png)

* Csv output is a table with the following value:

| Column            |             Description                  |
|-----------------|---------------------------------------|
| Name            | Name and surname of the developer     |
| Email           | Email                                 |
| SocialID        | Unique developer code on the git host |
| SocialUsername  | Developer username on git host        |
| AvatarURL       | URL avatar set on git host            |
| WebSite         | Personal website or blog              |
| Location        | Nationality                           |
| Bio             | Bio info                              |
| CreatedAt       | Account date created on the git host  |
| Commits         | Number of commits processed           |
| Backend%        | Backend category percentage           |
| Writer%         | Writer category percentage            |
| Frontend%       | Frontend category percentage          |
| CatExtra%       | Percentage of extra category          |