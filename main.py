import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel
from PyQt5.QtCore import QSortFilterProxyModel

import MainWindow, DialogGameEdit
import config


class AppGamesManager(QMainWindow):
    def __init__(self, connector):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.showMaximized()

        self.ui.actionGames.triggered.connect(self.subwindow_games)
        self.ui.pushButtonGamesEdit.clicked.connect(self.dialog_game_edit)

        self.sql_games_list = 'select * from dbo.Games_View order by ReleaseDate'
        self.query_games_list = QSqlQueryModel()

        self.connector = connector

    def subwindow_games(self):
        self.query_games_list = self.connector.sql_query_model_fetch(self.query_games_list, self.sql_games_list)

        self.ui.mdiArea.addSubWindow(self.ui.subwindowGames)
        self.ui.tableViewGamesList.setModel(self.query_games_list)
        self.ui.subwindowGames.showMaximized()

    def dialog_game_edit(self):
        index = self.ui.tableViewGamesList.currentIndex()
        index = self.ui.tableViewGamesList.model().index(index.row(), 0)
        dialog = DGameEdit(self.connector, self.ui.tableViewGamesList.model().data(index))
        dialog.exec_()


class DatabaseConnector:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase('QODBC')
        self.db.setDatabaseName(config.conn_string)
        self.db.open()

    def __del__(self):
        self.db.close()

    def sql_query_model_fetch(self, query_model, sql):
        if self.db.isOpen():

            qry = QSqlQuery(self.db)
            qry.prepare(sql)
            qry.exec()

            query_model.setQuery(qry)

            while query_model.canFetchMore():
                query_model.fetchMore()
        else:
            print("Database not connected")

        return query_model


class DGameEdit(QDialog):
    def __init__(self, connector, game_id):
        super().__init__()
        self.ui = DialogGameEdit.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.progressBarGameEditAvgNote.setFormat("%.02f %%" % self.ui.progressBarGameEditAvgNote.value())

        self.ui.pushButtonGameEditSave.clicked.connect(self.game_edit_save)
        self.ui.pushButtonGameEditCancel.clicked.connect(self.close)
        self.ui.horizontalSliderGameEditGraphics.valueChanged.connect(self.game_avg_note)
        self.ui.horizontalSliderGameEditSound.valueChanged.connect(self.game_avg_note)
        self.ui.horizontalSliderGameEditPlayability.valueChanged.connect(self.game_avg_note)
        self.ui.horizontalSliderGameEditStory.valueChanged.connect(self.game_avg_note)
        self.ui.horizontalSliderGameEditAmbience.valueChanged.connect(self.game_avg_note)
        self.ui.horizontalSliderGameEditOptimization.valueChanged.connect(self.game_avg_note)
        self.ui.horizontalSliderGameEditFun.valueChanged.connect(self.game_avg_note)


        self.game = self.Game(connector, game_id)

        self.ui.lineEditGameEditId.setText(str(game_id))
        self.ui.lineEditGameEditTitle.setText(self.game.query_game_data.record(0).value("GameTitle"))
        #self.ui.dateEditGameEditRelease.setDate(self.game.game_data.record(0).value("ReleaseDate"))

        current_index = -1

        for i in range(self.game.query_game_series.rowCount()):
            self.ui.comboBoxGameEditSeries.addItem(self.game.query_game_series.record(i).value("DictValueName"))
            if self.game.query_game_data.record(0).value("SeriesId") == self.game.query_game_series.record(i).value("Id"):
                current_index = i

        self.ui.comboBoxGameEditSeries.setCurrentIndex(current_index)

        current_index_2 = -1

        for i in range(self.game.query_game_type.rowCount()):
            self.ui.comboBoxGameEditType.addItem(self.game.query_game_type.record(i).value("DictValueName"))
            if self.game.query_game_data.record(0).value("GameAtr") == self.game.query_game_type.record(i).value("Id"):
                current_index_2 = i

        self.ui.comboBoxGameEditType.setCurrentIndex(current_index_2)

        current_index_3 = -1

        for i in range(self.game.query_game_genre.rowCount()):
            self.ui.comboBoxGameEditGenre.addItem(self.game.query_game_genre.record(i).value("DictValueName"))
            if self.game.query_game_data.record(0).value("Genre") == self.game.query_game_genre.record(i).value("Id"):
                current_index_3 = i

        self.ui.comboBoxGameEditGenre.setCurrentIndex(current_index_3)

        for i in range(self.game.query_game_notes.rowCount()):
            if self.game.query_game_notes.record(i).value("NoteCategory") == 34:
                self.ui.horizontalSliderGameEditGraphics.setValue(
                    self.game.query_game_notes.record(i).value("Note")
                )
                self.ui.labelGameEditGraphics.setText(str(self.game.query_game_notes.record(i).value("Note")))

            if self.game.query_game_notes.record(i).value("NoteCategory") == 35:
                self.ui.horizontalSliderGameEditSound.setValue(
                    self.game.query_game_notes.record(i).value("Note")
                )
                self.ui.labelGameEditSound.setText(str(self.game.query_game_notes.record(i).value("Note")))

            if self.game.query_game_notes.record(i).value("NoteCategory") == 36:
                self.ui.horizontalSliderGameEditPlayability.setValue(
                    self.game.query_game_notes.record(i).value("Note")
                )
                self.ui.labelGameEditPlayability.setText(str(self.game.query_game_notes.record(i).value("Note")))

            if self.game.query_game_notes.record(i).value("NoteCategory") == 37:
                self.ui.horizontalSliderGameEditStory.setValue(
                    self.game.query_game_notes.record(i).value("Note")
                )
                self.ui.labelGameEditStory.setText(str(self.game.query_game_notes.record(i).value("Note")))

            if self.game.query_game_notes.record(i).value("NoteCategory") == 38:
                self.ui.horizontalSliderGameEditAmbience.setValue(
                    self.game.query_game_notes.record(i).value("Note")
                )
                self.ui.labelGameEditAmbience.setText(str(self.game.query_game_notes.record(i).value("Note")))

            if self.game.query_game_notes.record(i).value("NoteCategory") == 39:
                self.ui.horizontalSliderGameEditOptimization.setValue(
                    self.game.query_game_notes.record(i).value("Note")
                )
                self.ui.labelGameEditOptimization.setText(str(self.game.query_game_notes.record(i).value("Note")))

            if self.game.query_game_notes.record(i).value("NoteCategory") == 40:
                self.ui.horizontalSliderGameEditFun.setValue(
                    self.game.query_game_notes.record(i).value("Note")
                )
                self.ui.labelGameEditFun.setText(str(self.game.query_game_notes.record(i).value("Note")))

    def game_avg_note(self):
        summary = self.ui.horizontalSliderGameEditGraphics.value() + self.ui.horizontalSliderGameEditSound.value() + \
                   self.ui.horizontalSliderGameEditPlayability.value() +\
                   self.ui.horizontalSliderGameEditAmbience.value() +\
                   self.ui.horizontalSliderGameEditOptimization.value() + self.ui.horizontalSliderGameEditFun.value() +\
                   self.ui.horizontalSliderGameEditStory.value()

        summary = summary * 10 / 7

        self.ui.progressBarGameEditAvgNote.setValue(int(summary*100))
        self.ui.progressBarGameEditAvgNote.setFormat("%.02f %%" % summary)


    class Game:
        def __init__(self, connector, game_id):
            self.query_game_data = QSqlQueryModel()
            self.sql_game_data = 'select * from dbo.Games where id = ' + str(game_id)

            self.query_game_series = QSqlQueryModel()
            self.sql_game_series = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 6'

            self.query_game_type = QSqlQueryModel()
            self.sql_game_type = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 1'

            self.query_game_genre = QSqlQueryModel()
            self.sql_game_genre = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 2'

            self.query_game_notes = QSqlQueryModel()
            self.sql_game_notes = 'select NoteCategory, Note from dbo.GamesNotes where GameId = ' + str(game_id)


            self.game_difficulties = QSqlQueryModel()
            self.game_collection = QSqlQueryModel()
            self.game_storage = QSqlQueryModel()



            self.query_game_data = connector.sql_query_model_fetch(self.query_game_data, self.sql_game_data)
            self.query_game_series = connector.sql_query_model_fetch(self.query_game_series, self.sql_game_series)
            self.query_game_type = connector.sql_query_model_fetch(self.query_game_type, self.sql_game_type)
            self.query_game_genre = connector.sql_query_model_fetch(self.query_game_genre, self.sql_game_genre)
            self.query_game_notes = connector.sql_query_model_fetch(self.query_game_notes, self.sql_game_notes)

            ### przy zapisie porównujemy czy wszystko jest takie samo z aktualnymi wartościami

    def game_edit_save(self):
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DatabaseConnector()
    win = AppGamesManager(connector=db)
    win.show()
    sys.exit(app.exec_())
