from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery, QSqlTableModel, QSqlRelationalTableModel


class Data:
    class Game:
        sql = {
            "Data": 'SELECT Id, Name, Category_id, Genre_id, Series_id, Release_date FROM dbo.Games WHERE Id = :id'
            , "Series": 'SELECT Id, Name FROM dbo.GamesDictionarySeries ORDER BY Name'
            , "Category": 'SELECT Id, Name FROM dbo.GamesDictionaryCategory ORDER BY Name'
            , "Genre": 'SELECT Id, Name FROM dbo.GamesDictionaryGenre ORDER BY Name'
            , "Notes": 'SELECT gan.Game_id, gan.Note, gan.Note_id, gdc.Name FROM dbo.GamesDictionaryNotes gdc LEFT JOIN ( SELECT Game_id, Note_Id, Note FROM dbo.GamesAttributesNotes WHERE Game_id = :id ) gan ON gan.Note_id = gdc.Id ORDER BY gan.Note_id'
            , "Collection": 'SELECT gac.Id, gac.Game_id, gdc.Name, gac.Collection_id, gac.Storage_id FROM dbo.GamesDictionaryCollection gdc	LEFT JOIN ( SELECT Id, Game_id, Collection_id, Storage_id FROM dbo.GamesAttributesCollection WHERE Game_id = :id) gac ON gac.Collection_id = gdc.Id ORDER BY gdc.Name'
            , "Storage": 'SELECT gac.Id, gac.Game_id, gds.Name, gac.Collection_id, gac.Storage_id FROM dbo.GamesDictionaryStorage gds LEFT JOIN ( SELECT Id, Game_id, Collection_id, Storage_id FROM dbo.GamesAttributesCollection WHERE Game_id = :id) gac ON gac.Storage_id = gds.Id'
            , "Difficulties": 'SELECT gad.Game_id, gad.InGameNumber, gad.Completed, gdd.Name FROM dbo.GamesDictionaryDifficulties gdd LEFT JOIN (SELECT Game_id, InGameNumber, Completed, Dificulty_id FROM dbo.GamesAttributesDifficulties WHERE game_id = :id) gad ON gdd.Id = gad.Dificulty_id ORDER BY gad.InGameNumber'
            # , "Review":
            # , "Cover":
        }

        def __init__(self, conn, game_id):
            self.game = dict()

            for i in self.sql.keys():
                self.data_refresh(i, conn, game_id)

        def data_refresh(self, i, conn, game_id):
            qry = QSqlQuery(conn.db)
            qry.prepare(self.sql[i])

            if ":id" in self.sql[i]:
                if game_id:
                    qry.bindValue(':id', game_id)
                else:
                    qry.bindValue(':id', 0)

            self.game[i] = QSqlQueryModel()
            self.game[i] = conn.sql_query_model_fetch(self.game[i], qry)
