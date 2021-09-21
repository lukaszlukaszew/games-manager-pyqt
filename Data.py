from PyQt5.QtSql import QSqlQueryModel, QSqlQuery


class Data:
    class Game:
        sql_d = {
            "Data": 'SELECT Id, Name, Category_id, Genre_id, Series_id, Release_date FROM dbo.Games WHERE Id = :id'
            , "Series": 'SELECT Id, Name FROM dbo.GamesDictionarySeries ORDER BY Name'
            , "Category": 'SELECT Id, Name FROM dbo.GamesDictionaryCategory ORDER BY Name'
            , "Genre": 'SELECT Id, Name FROM dbo.GamesDictionaryGenre ORDER BY Name'
            , "Notes": 'SELECT gan.Game_id, gan.Note, gdc.Id, gdc.Name FROM dbo.GamesDictionaryNotes gdc LEFT JOIN ( SELECT Game_id, Note_Id, Note FROM dbo.GamesAttributesNotes WHERE Game_id = :id ) gan ON gan.Note_id = gdc.Id ORDER BY gan.Note_id'
            , "Collection": 'SELECT gdc.Id, gac.Game_id, gdc.Name FROM dbo.GamesDictionaryCollection gdc LEFT JOIN ( SELECT Id, Game_id, Collection_id FROM dbo.GamesAttributesCollection WHERE Game_id = :id) gac ON gac.Collection_id = gdc.Id ORDER BY gdc.Name'
            , "Storage": 'SELECT gds.Id, gas.Game_id, gds.Name FROM dbo.GamesDictionaryStorage gds LEFT JOIN ( SELECT Id, Game_id, Storage_id FROM dbo.GamesAttributesStorage WHERE Game_id = :id) gas ON gas.Storage_id = gds.Id'
            , "Difficulties": 'SELECT gad.Game_id, gad.InGameNumber, gad.Completed, gdd.Name, gdd.Id FROM dbo.GamesDictionaryDifficulties gdd LEFT JOIN (SELECT Game_id, InGameNumber, Completed, Dificulty_id FROM dbo.GamesAttributesDifficulties WHERE game_id = :id) gad ON gdd.Id = gad.Dificulty_id ORDER BY gad.InGameNumber'
            , "Review": "SELECT Review FROM dbo.GamesReviews WHERE Game_id = :id"
        }

        def __init__(self, conn, game_id):
            self.models = dict()

            for i in self.sql_d.keys():
                self.data_refresh(i, conn, game_id)

        def data_refresh(self, i, conn, game_id):
            qry = QSqlQuery(conn.db)
            qry.prepare(self.sql_d[i])

            if ":id" in self.sql_d[i]:
                if game_id:
                    qry.bindValue(':id', game_id)
                else:
                    qry.bindValue(':id', 0)

            self.models[i] = QSqlQueryModel()
            self.models[i] = conn.sql_query_model_fetch(self.models[i], qry)

    #class Dictionary

    # TODO how to store all sql queries in here?

    #class Params
