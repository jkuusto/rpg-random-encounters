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

- Users can log in, log out, and create a new user account. **COMPLETE**
- Users can create games, edit existing games and delete games. **IN PROGRESS**
- Users can browse all games they've created and access them. **COMPLETE**
- Users can select parameters for the game (just biome for now). **COMPLETE**
- Selected game parameters are persistent between sessions. **COMPLETE**
- Main encounter table points to different sub-tables by encounter type. 
  **COMPLETE**
- Users can "roll dice", i.e. randomly determine an encounter on the main 
  table and subsequently another "dice roll" is made automatically on a 
  relevant sub-table. **IN PROGRESS**
- Users can make game-specific edits to the probability ranges in the main 
  encounter table. **UPCOMING / PLANNED**
- Users can add, edit, and remove encounter entries in each sub-table, 
  creating game-specific customizations. **UPCOMING / PLANNED**
- Preset content uses 5E compatible game rules (see legal section) **COMPLETE**


Progress update April 7, 2024
- User management features have been implemented as planned. Considering add 
  user account deletion feature.
- Game creation and deletion implemented. Game renaming is still in progress.
- For now, users can only roll for encounter type. Auto-roll on subsequent 
  encounter table is still in progress.
- Edits to the probability ranges are still in progress although underlying 
  logic in range representation to support this has already been completed.
- Encounter tables are not yet displayed to the user, so edit features are 
  pertaining those tables are also still in progress. A javascript hide/edit 
  table feature has been implemented to support encounter table user view.
- The database has a few preset entries that are copied to every new game. 
  These entries can be overwritten by the user on a game-by-game basis and 
  users can add their own custom content. Additional preset content may be 
  added later but is not required by the scope of this project.
- The layout and visual appearance are still in planning stage. Once all the 
  features are complete, the user interface will improved.
- Code formatting will be refined to better align with Python best practices.


## Setup

The app is not available online, so please follow these instructions to 
run it locally on your computer. 

Python 3.10.12 and PostgreSQL 14.11 have been used in development but the app 
will likely run on older versions, too, but compatibility is not guaranteed.

Clone this repository to your computer and access its root directory.
```
$ git clone https://github.com/jkuusto/rpg-random-encounters
$ cd <repository-directory>
```

Before proceeding, ensure that the database is running:
```
(venv) $ sudo service postgresql status
```
If the database isn't running, start it with:
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

The app's tables and content are created and inserted into the database 
by pointing the commands in schema.sql to the postgresSQL interpreter:
```
(venv) $ psql < schema.sql
```
Or if you created a new database for this app:
```
(venv) $ psql -d newdbname -f schema.sql
```

You can now start the app with the following command:
```
$ (venv) flask run
```
To access the app locally, open a web browser and navigate to:
`http://localhost:5000/` or `http_//127.0.0.1:5000/`


## Usage

1. On front page, click Login/Register
2. Use the Register section to create a new user
3. Login using the Login section, you will be redirected to the dashboard
4. Create new games by giving it a new in the Create a New Game section, 
   games will be listed under Your Games
5. Delete games, by clicking Delete next to a game
6. Access a game by clicking its name
7. You can change biome from the dropdown menu
8. You can roll for encounter types by clicking Roll
9. You can show/hide encounter tables by clicking corresponding buttons


## Legal

This work includes material taken from the System Reference Document 5.1 
(“SRD 5.1”) by Wizards of the Coast LLC and available at 
https://dnd.wizards.com/resources/systems-reference-document. The SRD 5.1 is 
licensed under the Creative Commons Attribution 4.0 International License 
available at https://creativecommons.org/licenses/by/4.0/legalcode.
