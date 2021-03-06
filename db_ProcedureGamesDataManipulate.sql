USE [GAMESTEMP]
GO
/****** Object:  StoredProcedure [dbo].[GamesDataManipulate]    Script Date: 2021-09-21 19:52:57 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[GamesDataManipulate]
	@type varchar(max),
	@value varchar(max) = null,
	@name varchar(max) = null,
	@date date = null,
	@series int = null,
	@genre int = null,
	@category int = null,
	@id int = null,
	@note_id int = null,
	@note int = null,
	@diff int = null,
	@complete bit = null,
	@ign int = null,
	@collection int = null,
	@storage int = null,
	@text text = null

	AS
-- to elegancko mozna przerobic na dynamic SQL
IF @type = 'Storage'
	BEGIN 
	IF NOT EXISTS (SELECT NULL FROM dbo.GamesDictionaryStorage WHERE Name = @value)
		BEGIN
			insert into dbo.GamesDictionaryStorage (Name)
			values (@value)
		END
	END

IF @type = 'Category'
	BEGIN
	IF NOT EXISTS (SELECT NULL FROM dbo.GamesDictionaryCategory WHERE Name = @value)
		BEGIN
			insert into dbo.GamesDictionaryCategory (Name)
			values (@value)
		END
	END

IF @type = 'Genre'
	BEGIN
	IF NOT EXISTS (SELECT NULL FROM dbo.GamesDictionaryGenre WHERE Name = @value)
		BEGIN
			insert into dbo.GamesDictionaryGenre (Name)
			values (@value)
		END
	END

IF @type = 'Collection'
	BEGIN
	IF NOT EXISTS (SELECT NULL FROM dbo.GamesDictionaryCollection WHERE Name = @value)
		BEGIN
			insert into dbo.GamesDictionaryCollection (Name)
			values (@value)
		END
	END

IF @type = 'Series'
	BEGIN
	IF NOT EXISTS (SELECT NULL FROM dbo.GamesDictionarySeries WHERE Name = @value)
		BEGIN
			insert into dbo.GamesDictionarySeries (Name)
			values (@value)
		END
	END
IF @type = 'Difficulties'
	BEGIN
	IF NOT EXISTS (SELECT NULL FROM dbo.GamesDictionaryDifficulties WHERE Name = @value)
		BEGIN
			insert into dbo.GamesDictionaryDifficulties (Name)
			values (@value)
		END
	END
IF @type = 'Notes'
	BEGIN
	IF NOT EXISTS (SELECT NULL FROM dbo.GamesDictionaryNotes WHERE Name = @value)
		BEGIN
			insert into dbo.GamesDictionaryNotes(Name)
			values (@value)
		END
	END

IF @type = 'ADDGAME'
	IF @id is NULL
		BEGIN
			IF NOT EXISTS (SELECT NULL FROM dbo.Games WHERE Name = @name)
				BEGIN
				-- tutj na pewno trzeba zabezpieczyc przed brakami
					insert into dbo.Games (Name, Series_id, Category_id, Genre_id, Release_date)
					values (@name, @series, @category, @genre, @date)
				END
		END
	ELSE
		BEGIN
				-- tutj na pewno trzeba zabezpieczyc przed brakami
			update dbo.games
			set Name = @name, Series_id = @series, Category_id = @category, Release_date = @date, Genre_id = @genre
			where Id = @id
		END

IF @type = 'ADDNOTES'
	BEGIN
		IF EXISTS (SELECT NULL FROM dbo.GamesAttributesNotes WHERE Note_id = @note_id and Game_id = @id)
			BEGIN
				UPDATE dbo.GamesAttributesNotes
				SET Note = @note
				where Game_id = @id and Note_id = @note_id
			END
		ELSE
			BEGIN
				INSERT INTO dbo.GamesAttributesNotes (Game_id, Note_id, Note)
				VALUES (@id, @note_id, @note)
			END
	END

IF @type = 'FINDDIFF'
	BEGIN
		update dbo.GamesAttributesDifficulties
		set [current] = 1
		where game_id = @id

	END

IF @type = 'ADDDIFF'
	BEGIN
		IF EXISTS (SELECT NULL FROM dbo.GamesAttributesDifficulties WHERE Dificulty_id = @diff and Game_id = @id)
			BEGIN
				UPDATE dbo.GamesAttributesDifficulties
				SET InGameNumber = @ign, Completed = @complete, [Current] = 0
				WHERE Game_id = @id and Dificulty_id = @diff
			END
		ELSE
			BEGIN
				INSERT INTO dbo.GamesAttributesDifficulties (Dificulty_id, Game_id, InGameNumber, Completed, [Current])
				VALUES (@diff, @id, @ign, @complete, 0)
			END
	END

IF @type = 'CLEANDIFF'
	BEGIN
		DELETE FROM dbo.GamesAttributesDifficulties
		WHERE ( Game_id = @id and [Current] is null) or (Game_id = @id and [Current] = 1)
	END

IF @type = 'FINDCOLL'
	BEGIN
		update dbo.GamesAttributesCollection
		set [current] = 1
		where game_id = @id

	END

IF @type = 'ADDCOLL'
	BEGIN
		IF EXISTS (SELECT NULL FROM dbo.GamesAttributesCollection WHERE Game_id = @id and Collection_id = @collection)
			BEGIN
				UPDATE dbo.GamesAttributesCollection
				SET [Current] = 0
				WHERE Game_id = @id and Collection_id = @collection

			END
		ELSE
			BEGIN
				INSERT INTO dbo.GamesAttributesCollection (Game_id, Collection_id, [Current])
				VALUES (@id, @collection,0)
			END
	END

IF @type = 'CLEANCOLL'
	BEGIN
		DELETE FROM dbo.GamesAttributesCollection
		WHERE ( Game_id = @id and [Current] is null) or (Game_id = @id and [Current] = 1)
	END

IF @type = 'FINDSTOR'
	BEGIN
		update dbo.GamesAttributesStorage
		set [current] = 1
		where game_id = @id

	END

IF @type = 'ADDSTOR'
	BEGIN
		IF NOT EXISTS (SELECT NULL FROM dbo.GamesAttributesStorage WHERE Game_id = @id and Storage_id = @storage)
			BEGIN
				INSERT INTO dbo.GamesAttributesStorage (Game_id, Storage_id, [Current])
				VALUES (@id, @storage,0)
			END
		ELSE
			BEGIN
				UPDATE dbo.GamesAttributesStorage
				SET [Current] = 0
				WHERE Game_id = @id and Storage_id = @storage
			END
	END

IF @type = 'CLEANSTOR'
	BEGIN
		DELETE FROM dbo.GamesAttributesStorage
		WHERE ( Game_id = @id and [Current] is null) or (Game_id = @id and [Current] = 1)
	END

IF @type = 'REVIEW'
	BEGIN
		IF EXISTS (SELECT NULL FROM dbo.GamesReviews WHERE Game_id = @id)
			BEGIN
				UPDATE dbo.GamesReviews
				SET Review = @text
				WHERE Game_id = @id
			END
		ELSE
			BEGIN
				INSERT INTO dbo.GamesReviews (Game_id, Review)
				VALUES (@id, @text)
			END

	END