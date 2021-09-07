from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel

class Data:

    class Game:
        info = ["Data", "Series", "Type", "Genre", "Notes", "Collection", "Storage", "Difficulties", "Review", "Cover"]
        sql = {
                  "Data": 'select * from dbo.Games where id = :id'
                , "Series": 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 6 order by DictValueName'
                , "Type": 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 1'
                , "Genre": 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 2'
                , "Notes": 'select NoteCategory, Note from dbo.GamesNotes where GameId = :id'
                , "Collection": 'select * from dbo.Collection_View where Id = :id'
                #, "Storage":
                , "Difficulties": 'select * from dbo.Difficulties_View where Id = :id order by InGameNumber'
                #, "Review":
                #, "Cover":
        }

        def __init__(self, conn, game_id):
            self.game = dict()

            for i in self.info:
                self.game[i] = QSqlQueryModel()
                if ":id" in self.sql[i] & game_id is not None:
                    self.game[i].bindValue(":id", str(game_id))

                    """ dobry trop, ale jeszcze chwilę trzeba pomyśleć to u góry mi się nie podoba..."""

                self.game[i] = conn.sql_query_model_fetch(self.game[i], self.sql["data"] + str(game_id))
