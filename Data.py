from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery


class Data:
    class Game:
        sql = {
                  "Data": 'select Id, GameTitle, SeriesId, ReleaseDate, GameAtr as TypeId, Genre as GenreId from dbo.games where id = :id'
                , "Series": 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 6 order by DictValueName'
                , "Type": 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 1'
                , "Genre": 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 2'
                , "Notes": 'select d.Id, d.DictValueName, gn.Note from dbo.GamesNotes gn inner join dbo.Dictionaries d on d.Id = gn.NoteCategory where d.DictType = 4 and gn.GameId = :id order by d.InTypeId'
                #, "GameNotes": 'select NoteCategory, Note from dbo.GamesNotes where GameId = :id'
                , "Collection": 'select * from dbo.Collection_View where Id = :id'
                #, "Storage":
                , "Difficulties": 'select * from dbo.Difficulties_View where Id = :id order by InGameNumber'
                #, "Review":
                #, "Cover":
        }

        def __init__(self, conn, game_id):
            self.game = dict()

            for i in self.sql.keys():
                qry = QSqlQuery(conn.db)
                qry.prepare(self.sql[i])

                if ":id" in self.sql[i]:
                    if game_id:
                        qry.bindValue(':id', game_id)
                    else:
                        continue

                self.game[i] = QSqlQueryModel()
                self.game[i] = conn.sql_query_model_fetch(self.game[i], qry)
