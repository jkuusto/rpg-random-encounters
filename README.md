# rpg-random-encounters

With this web tool for tabletop role-playing games a game master can create 
"games" in which random encounters can be generated for players to interact 
with (narrated to them verbally by the game master). The generated encounters 
can be influenced by the campaign parameters selected by the user. 
Each user is a basic user (a game master).


## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Legal](#legal)


## Features

These are the the web app's main features:

- Users can log in, log out, and create a new user account.
- Users can create games, edit existing games and delete games.
- Users can browse all games they've created and access them.
- Users can select parameters for the game (just biome for now).
- Selected game parameters are persistent between sessions.
- Main encounter table points to different sub-tables by encounter type.
- Users can "roll dice", i.e. randomly determine an encounter on the main 
  table and subsequently another "dice roll" is made automatically on a 
  relevant sub-table.
- Users can make game-specific edits to the probability ranges in the main 
  encounter table.
- Users can add, edit, and remove encounter entries in each sub-table, 
  creating game-specific customizations.
- Preset content uses 5E compatible game rules (see legal section).


Progress update May 5, 2024
- All core features have been implemented.
- CSRF vulnerabilities have been patched.
- An HTML template has been added for a uniform look across pages.
- Visual appearance has been worked on. A monochrome look was chosen.
- Character limit for user input has been enforced where applicable.
- User feedback upon invalid input has been implemented.
- User account deletion feature has been added.


Planned features for future development:
- Verification dialogue when deleting games and encounters
- Ability to roll directly on a chosen encounter table
- More game parameters and accompanying encounter tables to games
- Customizible game parameters
- Further improvements on visual appearance
- Support for images for encounter entries


## Setup

The app is not available online, so please follow these instructions to 
run it locally on your computer.
- $ indicates Bash commands
- PS> indicates Windows PowerShell commands

Python 3.10.12 and PostgreSQL 14.11 have been used in development but the app 
will likely run on older versions, too, but compatibility is not guaranteed.

Clone this repository to your computer and access its root directory.
```
$ git clone https://github.com/jkuusto/rpg-random-encounters
$ cd <repository-directory>
```

Before proceeding, ensure that the database service is running:
```
$ sudo service postgresql status
PS> Get-Service -Name postgresql-x64-<version>
```
If the database service isn't running, start it with:
```
$ sudo service postgresql start
PS> Start-Service -Name postgresql-x64-<version>
```

If you want to create a new database for this app, go to psql and type:
```
user=# CREATE DATABASE newdbname;
```
You can create a new secret key with:
```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```

Create an .env file in the app's directory with the following content:
```
DATABASE_URL=<database-local-address>
SECRET_KEY=<secret-key>
```

Activate the virtual environment and install dependencies:
```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r ./requirements.txt
```
```
PS> python -m venv venv
PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
PS> .\venv\Scripts\Activate.ps1
(venv) PS> pip install -r .\requirements.txt
```

Create and populate the database by pointing the schema to psql:
```
(venv) $ psql < schema.sql
(venv) $ psql -d databasename < data.pgdump
```
Or by assigning a specific database for this app:
```
(venv) $ psql -d newdbname -f schema.sql
(venv) $ psql -d newdbname -f data.pgdump
---
(venv) PS> Get-Content schema.sql | psql -U username -d databasename
(venv) PS> Get-Content data.pgdump | psql -U username -d databasename
```
Note: It is important to populate the database with data.pgdump. 
Without it, the app will not have any preset data.

You can now start the app with the following command:
```
$ (venv) flask run
```
To access the app locally, open a web browser and navigate to:
`http://localhost:5000/` or `http_//127.0.0.1:5000/`


## Usage

1.  On front page, click Login/Register
2.  Use the Register section to create a new user
3.  Login using the Login section, you will be redirected to the dashboard
4.  Create new games by clicking the button and giving it a name in the text 
    editor. Created games will be listed under Your Games
5.  Rename or delete games, by clicking the appropriate button next to a game
6.  Access a game by clicking its name
7.  On the game page you can change game biome from the dropdown menu
8.  You can roll for encounters by clicking Roll on the main table
9.  You can show/hide encounter tables by clicking corresponding buttons
10. Change the roll range of any entry on a table by clicking Range, typing 
    an integer and pressing enter. The table entries are reordered according 
    to range value in descending order
11. Rewrite or delete encounters by clicking the appropriate button next to 
    the entry
12. Add new encounters by clicking Add new encounter on the bottom of a table
13. You may delete your account on the dashboard by clicking Delete Account


## Legal

This work includes material taken from the System Reference Document 5.1 
(“SRD 5.1”) by Wizards of the Coast LLC and available at 
https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is 
licensed under the Creative Commons Attribution 4.0 International License 
available at https://creativecommons.org/licenses/by/4.0/legalcode.
