-- DATABASE


CREATE DATABASE GAMESTEMP
GO

USE GAMESTEMP
GO


-- TABLES


CREATE TABLE DictionaryType (
	Id int IDENTITY(1, 1) PRIMARY KEY NOT NULL,
	DictName varchar(30) NOT NULL
	);

CREATE TABLE Dictionaries (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	DictType int FOREIGN KEY REFERENCES DictionaryType(Id) NOT NULL,
	DictValueName varchar(max) NOT NULL,
	InTypeId int NOT NULL
	);

CREATE TABLE Games (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	GameTitle varchar(max) NOT NULL,
	SeriesId int FOREIGN KEY REFERENCES Dictionaries(Id),
	ReleaseDate date,
	GameAtr int FOREIGN KEY REFERENCES Dictionaries(Id) NOT NULL,
	Added smalldatetime DEFAULT GETDATE() NOT NULL,
	Genre int FOREIGN KEY REFERENCES Dictionaries(Id),
	);

CREATE TABLE GamesDifficultyLevels (
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	DificultyId int FOREIGN KEY REFERENCES Dictionaries(Id) NOT NULL,
	GameId int FOREIGN KEY REFERENCES Games(Id) NOT NULL,
	InGameNumber int NOT NULL,
	Completed bit NOT NULL DEFAULT 0
	);

CREATE TABLE GamesNotes (
	Id int IDENTITY (1,1) PRIMARY KEY NOT NULL,
	GameId int FOREIGN KEY REFERENCES Games(Id) NOT NULL,
	NoteCategory int FOREIGN KEY REFERENCES Dictionaries(Id) NOT NULL,
	Note int CHECK(Note BETWEEN 0 AND 10)
	);

CREATE TABLE GamesCollection (
	Id int IDENTITY (1,1) PRIMARY KEY NOT NULL,
	GameId int FOREIGN KEY REFERENCES Games(Id) NOT NULL,
	CollectionCategory int FOREIGN KEY REFERENCES Dictionaries(Id) NOT NULL
	);

GO


-- VIEWS


CREATE VIEW Games_View
AS
SELECT
	a.Id
	, a.GameTitle
	, ISNULL(b.DictValueName, '') AS Series
	, a.ReleaseDate
	, c.DictValueName AS GameAtr
	, d.DictValueName AS Genre
	, ISNULL(e.Coll, 0) AS Owned
	, ISNULL(cast(f.AvgN as varchar(max)), '') as AverageNote
	, CAST(g.Completed*100/g.AllDiffLevels AS varchar(3)) + ' %' AS Completion
FROM Games a
	LEFT JOIN Dictionaries b on a.SeriesId = b.Id
	LEFT JOIN Dictionaries c on a.GameAtr = c.Id
	LEFT JOIN Dictionaries d on a.Genre = d.Id
	LEFT JOIN (
		SELECT GameId, COUNT(GameId) AS Coll
		FROM dbo.GamesCollection
		GROUP BY GameId
		) e on e.GameId = a.Id
	LEFT JOIN (
		SELECT z.GameId
			, ROUND(CAST(SUM(z.Note) AS float(2))/CAST(COUNT(z.Note) AS float(2)), 2) AS AvgN
		FROM GamesNotes z
		GROUP BY z.GameId
		) f on f.GameId = a.Id
	LEFT JOIN (
		SELECT GameId
			,SUM(CASE WHEN Completed = 1 THEN 1 ELSE 0 END) AS Completed
			,COUNT(GameId) AS AllDiffLevels
		FROM GamesDifficultyLevels
		GROUP BY GameId) g on g.GameId = a.Id

GO

CREATE VIEW Collection_View
AS
SELECT g.Id, d.DictValueName
FROM dbo.Games g
	INNER JOIN dbo.GamesCollection gc on g.Id = gc.GameId
	INNER JOIN dbo.Dictionaries d on gc.CollectionCategory = d.Id

GO

CREATE VIEW Difficulties_View
AS
SELECT g.Id, gdl.InGameNumber, gdl.Completed, d.DictValueName
FROM dbo.Games g
	INNER JOIN dbo.GamesDifficultyLevels gdl on g.Id = gdl.GameId
	INNER JOIN dbo.Dictionaries d on d.Id = gdl.DificultyId

GO
