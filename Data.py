class Data:
    class GameList:
        sql = "SELECT * FROM dbo.GamesMainView where id >= 95 order by Id"

        def __init__(self, conn):
            self.model = conn.sql_refresh(self.sql, None)

    class Game:
        sql_d = {
            "Data": 'SELECT Id, Name, Category_id, Genre_id, Series_id, Release_date FROM dbo.Games WHERE Id = :id',
            "Series": 'SELECT Id, Name FROM dbo.GamesDictionarySeries ORDER BY Name',
            "Category": 'SELECT Id, Name FROM dbo.GamesDictionaryCategory ORDER BY Name',
            "Genre": 'SELECT Id, Name FROM dbo.GamesDictionaryGenre ORDER BY Name',
            "Notes": 'SELECT gan.Game_id, gan.Note, gdc.Id, gdc.Name FROM dbo.GamesDictionaryNotes gdc LEFT JOIN '
                     '( SELECT Game_id, Note_Id, Note FROM dbo.GamesAttributesNotes WHERE Game_id = :id ) gan ON '
                     'gan.Note_id = gdc.Id ORDER BY gan.Note_id',
            "Collection": 'SELECT gdc.Id, gac.Game_id, gdc.Name FROM dbo.GamesDictionaryCollection gdc LEFT JOIN '
                          '( SELECT Id, Game_id, Collection_id FROM dbo.GamesAttributesCollection WHERE '
                          'Game_id = :id) gac ON gac.Collection_id = gdc.Id ORDER BY gdc.Name',
            "Storage": 'SELECT gds.Id, gas.Game_id, gds.Name FROM dbo.GamesDictionaryStorage gds LEFT JOIN '
                       '( SELECT Id, Game_id, Storage_id FROM dbo.GamesAttributesStorage WHERE Game_id = :id) gas '
                       'ON gas.Storage_id = gds.Id',
            "Difficulties": 'SELECT gad.Game_id, gad.InGameNumber, gad.Completed, gdd.Name, gdd.Id FROM '
                            'dbo.GamesDictionaryDifficulties gdd LEFT JOIN (SELECT Game_id, InGameNumber, Completed, '
                            'Dificulty_id FROM dbo.GamesAttributesDifficulties WHERE game_id = :id) gad ON '
                            'gdd.Id = gad.Dificulty_id ORDER BY gad.InGameNumber',
            "Review": "SELECT Review FROM dbo.GamesReviews WHERE Game_id = :id",
        }

        sql_u = {
            "Data": "EXEC dbo.GamesDataManipulate @id = :id, @name = :name, @category = :category, @date = :date, "
                    "@genre = :genre, @series = :series, @type = 'ADDGAME'",
            "Notes": "EXEC dbo.GamesDataManipulate @note_id = :note_id, @id = :id, @note = :note, @type = 'ADDNOTES'",
            "Collection1": "EXEC dbo.GamesDataManipulate @id = :id, @type = 'FINDCOLL'",
            "Collection2": "EXEC dbo.GamesDataManipulate @id = :id, @collection = :collection, @type = 'ADDCOLL'",
            "Collection3": "EXEC dbo.GamesDataManipulate @id = :id, @type = 'CLEANCOLL'",
            "Storage1": "EXEC dbo.GamesDataManipulate @id = :id, @type = 'FINDSTOR'",
            "Storage2": "EXEC dbo.GamesDataManipulate @id = :id, @storage = :storage, @type = 'ADDSTOR'",
            "Storage3": "EXEC dbo.GamesDataManipulate @id = :id, @type = 'CLEANSTOR'",
            "Difficulties1": "EXEC dbo.GamesDataManipulate @id = :id, @type = 'FINDDIFF'",
            "Difficulties2": "EXEC dbo.GamesDataManipulate @id = :id, @diff = :diff, @complete = :complete, "
                             "@ign = :ign, @type = 'ADDDIFF'",
            "Difficulties3": "EXEC dbo.GamesDataManipulate @id = :id, @type = 'CLEANDIFF'",
            "Review": "EXEC dbo.GamesDataManipulate @id = :id, @text = :text, @type = 'REVIEW'",
            "Dict": "EXEC dbo.GamesDataManipulate @type = :dictionary, @value = :value",
        }

        params = {
            "Data": (":id", ":name", ":series", ":date", ":category", ":genre",),
            "Notes": (":id", ":note", ":note_id",),
            "Collection1": (":id",),
            "Collection2": (":id", ":collection",),
            "Collection3": (":id",),
            "Storage1": (":id",),
            "Storage2": (":id", ":storage",),
            "Storage3": (":id",),
            "Difficulties1": (":id",),
            "Difficulties2": (":id", ":diff", ":ign", ":complete",),
            "Difficulties3": (":id",),
            "Review": (":id", ":text",),
            "Dict": (":dictionary", ":value",),
        }

        def __init__(self, conn, game_id):
            self.models = dict()

            for i in self.sql_d.keys():
                self.models[i] = conn.sql_refresh(self.sql_d[i], game_id)

        def data_refresh(self, conn, game_id, key):
            self.models[key] = conn.sql_refresh(self.sql_d[key], game_id)
