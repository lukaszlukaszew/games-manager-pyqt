# Welcome to my second project - GAMES MANAGEMENT APP

Few words before I get to the specifics… 

## Why it was made?
Idea for this app came to me from:
- my inner need to making notes and lists about everything what is interesting for me,
- interest in computer games,
- SQL Server database, which was created by me a few years ago thanks to the two points above.
As time went by using only SSMS to keep track of my games collection proved itself far from comfortable, so I decided to make GUI-based app, which will make my life easier. Luckily, I recently finished extensive book about PyQT.

## Details
As soon as the project is finished, I will provide proper readme file with all features.  Until then I will post brief description of added functionalities after every commit on the main branch. I will keep stable version on the main branch and develop rest of the planned features on different ones.

List of features which are usable after most recent commit:
- database structure,
- main app window and sub window with games list called in Edit->Games (for now you could open it once for every start of application, I need to look it up),
- window for adding a new game and editing an existing one with parameters: title, series, genre, category, rating, collection, difficulty levels.
At this moment you can input all needed data to the database using only this app. I believe it is pretty user friendly and obvious in use.

In this paragraph I will put every information about features that may look odd at the first look, and why I made it like that:
- Collection attribute: it is divided into two categories: collection and storage, first one is dedicated to platform on which you have a copy of a game, and second one is to bind that copy to for example external hard drive. I have few of them myself and in case of GOG copies it’s hard to keep track sometimes when you want to have downloaded backup.
- Difficulty attribute: difficulty list needs to be filled from the easiest possible difficulty level in the game to the hardest one. I’ve implemented logic in which this order it’s remembered. Let’s assume that game have three difficulty levels: easy, medium and hard, you’ve inserted this values in proper order and finished the level medium. When you mark it as completed also level easy will be marked as completed, because it’s easier than medium. I’ve made it this way to never replay a game on the easier level than I completed – so even my hobby is challenging 😊

I’m developing this on:
- Python 3.8
- PyQT 5.15.4
- MS SQL SERVER Management Studio 2014

## How can you run it?
To use this app in a desired manner you need:
1.	Download all the files.
2.	Install SQL Server which allows you create database from db_DatabaseStructure.sql file.
3.	Create stored procedure from db_GameDataManipulation.sql file.
4.	Connect app to a database: in order to do that you need to create another .py file called config.py. That file must contain below lines filled with your local server name assigned to a server variable.

```python
server = ''
db = 'GAMESTEMP'

conn_string = f'DRIVER={{SQL Server}};'\
                f'SERVER={server};'\
                f'DATABASE={db}'
```

5.	Run main.py.

There is a lot of work ahead of me, so enough talking! Have a great day!
