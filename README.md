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
- Preset content uses 5E compatible game rules (see legal section)


## Setup

The app has been created using Python 3.10.12 and PostgreSQL 14.11 but will 
likely run on older versions, too, but compatibility is not guaranteed.

Clone this repository to your computer and access its root directory.
```
$ git clone https://github.com/jkuusto/rpg-random-encounters
$ cd <repository-directory>
```

Before proceeding, check that the database is running:
```
(venv) $ sudo service postgresql status
```
If the database is not running, start it with:
```
(venv) $ sudo service postgresql start
```

If you want to create a new database for this app, access psql and type:
```
user=# CREATE DATABASE newdbname;
```
You can create a new secret key with:
```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```

Create an .env file there with the following content:
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

The app's tables and content are created and inserted into the database 
by pointing the commands in schema.sql to the postgresSQL interpreter:
```
(venv) $ psql < schema.sql
```
Or if you created a new database for this app:
```
(venv) $ psql -d newdbname -f schema.sql
```

Now you can start the app with the following command:
```
$ (venv) flask run
```
To access the app locally, open a web browser and navigate to:
`http://localhost:5000/` or `http_//127.0.0.1:5000/`


## Usage

(coming soon)


## Legal

This work includes material taken from the System Reference Document 5.1 
(“SRD 5.1”) by Wizards of the Coast LLC and available at 
https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is 
licensed under the Creative Commons Attribution 4.0 International License 
available at https://creativecommons.org/licenses/by/4.0/legalcode.
