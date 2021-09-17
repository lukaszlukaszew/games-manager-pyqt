-- DATABASE

CREATE DATABASE GAMESTEMP
GO

USE GAMESTEMP

GO

-- TABLES

CREATE TABLE GamesDictionarySeries (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL	);

CREATE TABLE GamesDictionaryCategory (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL
	);

CREATE TABLE GamesDictionaryGenre (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL
	);

CREATE TABLE GamesDictionaryNotes (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL
	);

CREATE TABLE GamesDictionaryCollection (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL
	);

CREATE TABLE GamesDictionaryTags (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL
	);

CREATE TABLE GamesDictionaryDifficulties (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL
	);

CREATE TABLE GamesDictionaryStorage (
	Id int IDENTITY (1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL,
	);

CREATE TABLE Games (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Name varchar(max) NOT NULL,
	Series_id int FOREIGN KEY REFERENCES GamesDictionarySeries(Id) NULL,
	Release_date date,
	Category_id int FOREIGN KEY REFERENCES GamesDictionaryCategory(Id) NOT NULL,
	Added smalldatetime DEFAULT GETDATE() NOT NULL,
	Genre_id int FOREIGN KEY REFERENCES GamesDictionaryGenre(Id) NOT NULL
	);

CREATE TABLE GamesAttributesDifficulties (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Dificulty_id int FOREIGN KEY REFERENCES GamesDictionaryDifficulties(Id) NOT NULL,
	Game_id int FOREIGN KEY REFERENCES Games(Id) NOT NULL,
	InGameNumber int NOT NULL,
	Completed bit NOT NULL DEFAULT 0
	);

CREATE TABLE GamesAttributesNotes (
	Id int IDENTITY (1,1) PRIMARY KEY NOT NULL,
	Game_id int FOREIGN KEY REFERENCES Games(Id) NOT NULL,
	Note_id int FOREIGN KEY REFERENCES GamesDictionaryNotes(Id) NOT NULL,
	Note int CHECK(Note BETWEEN 0 AND 10)
	);

CREATE TABLE GamesAttributesCollection (
	Id int IDENTITY (1,1) PRIMARY KEY NOT NULL,
	Game_id int FOREIGN KEY REFERENCES Games(Id) NOT NULL,
	Collection_id int FOREIGN KEY REFERENCES GamesDictionaryCollection(Id) NOT NULL,
	Storage_id int FOREIGN KEY REFERENCES GamesDictionaryStorage(Id) NULL
	);
GO

--- WSTÊPNE WYPE£NIENIE WIERSZY, KTÓRE S¥ POTRZEBNE




-- VIEWS

CREATE VIEW GamesMainView
AS
SELECT
	g.Id
	, g.Name AS Title
	, ISNULL(gds.Name, '') AS Series
	, gdc.Name AS Category
	, gdg.Name AS Genre
	, Release_date as [Release date]
	, ISNULL(CAST(gan.Note AS varchar(max)), '') AS Note
	, ISNULL(gac.Copies, 0) AS Copies
	, CAST(gad.CompletedDiffs * 100 / gad.AllDiffs AS varchar(3)) + ' %' AS Completion
FROM Games g
	LEFT JOIN GamesDictionarySeries gds ON gds.Id = g.Series_id
	LEFT JOIN GamesDictionaryCategory gdc ON gdc.Id = g.Category_id
	LEFT JOIN GamesDictionaryGenre gdg ON gdg.Id = g.Genre_id
	LEFT JOIN (
		SELECT Game_id
			, COUNT(*) AS Copies
		FROM GamesAttributesCollection
		GROUP BY Game_id
		) gac on gac.Game_id = g.Id
	LEFT JOIN (
		SELECT Game_id
			, ROUND(CAST(SUM(Note)AS float(2))/COUNT(Note) , 2) AS Note
		FROM GamesAttributesNotes 
		GROUP BY Game_id
		) gan on gan.Game_id = g.Id
	LEFT JOIN (
		SELECT Game_id
			, SUM(CASE WHEN Completed = 1 THEN 1 ELSE 0 END) AS CompletedDiffs
			, COUNT(*) AS AllDiffs
		FROM GamesAttributesDifficulties
		GROUP BY Game_id
		) gad on gad.Game_id = g.Id

GO

CREATE VIEW GamesNotesView
AS
SELECT gan.Game_id, gdn.Id, gdn.Name, gan.Note
FROM dbo.GamesAttributesNotes gan
	INNER JOIN dbo.GamesDictionaryNotes gdn on gan.Note_id = gdn.Id

GO

CREATE VIEW GamesCollectionView
AS
SELECT gac.Game_id, gdc.Name as Collection_name, gds.Name as Storage_name
FROM dbo.GamesAttributesCollection gac
	INNER JOIN dbo.GamesDictionaryCollection gdc ON gac.Collection_id = gdc.Id
	LEFT JOIN dbo.GamesDictionaryStorage gds ON gac.Storage_id = gds.Id

GO

CREATE VIEW GamesDifficultiesView
AS
SELECT gad.Game_id, gad.InGameNumber, gad.Completed, gdd.Name
FROM dbo.GamesAttributesDifficulties gad
	INNER JOIN dbo.GamesDictionaryDifficulties gdd on gdd.Id = gad.Dificulty_id

GO

ALTER TABLE GamesAttributesDifficulties add [Current] bit