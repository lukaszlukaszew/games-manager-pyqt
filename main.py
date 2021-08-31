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

        self.connector = connector

    def subwindow_games(self):

        self.querymodel = QSqlQueryModel()

        sql_statement = 'select * from dbo.Games_View order by ReleaseDate'

        if self.connector.db.isOpen():

            qry = QSqlQuery(self.connector.db)
            qry.prepare(sql_statement)
            qry.exec()

            self.querymodel.setQuery(qry)

            while self.querymodel.canFetchMore():
                self.querymodel.fetchMore()


        self.ui.mdiArea.addSubWindow(self.ui.subwindowGames)
        self.ui.tableViewGamesList.setModel(self.querymodel)
        self.ui.subwindowGames.showMaximized()


    def dialog_game_edit(self):
        index = self.ui.tableViewGamesList.currentIndex()
        index = self.ui.tableViewGamesList.model().index(index.row(), 0)
        _dialog = DGameEdit(self.connector, self.ui.tableViewGamesList.model().data(index))
        _dialog.exec_()


class DatabaseConnector:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase('QODBC')
        self.db.setDatabaseName(config.conn_string)
        self.db.open()


    def __del__(self):
        self.db.close()


class DGameEdit(QDialog):
    def __init__(self, connector, game_id):
        super().__init__()
        self.ui = DialogGameEdit.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonGameEditSave.clicked.connect(self.game_edit_save)
        self.ui.pushButtonGameEditCancel.clicked.connect(self.close)

        self.game = self.Game(connector, game_id)

        self.ui.lineEditGameEditId.setText(str(self.game.game_data.record(0).value("Id")))
        self.ui.lineEditGameEditTitle.setText(self.game.game_data.record(0).value("GameTitle"))
        #self.ui.dateEditGameEditRelease.setDate(self.game.game_data.record(0).value("ReleaseDate"))

        current_index = -1

        for i in range(self.game.game_series.rowCount()):
            self.ui.comboBoxGameEditSeries.addItem(self.game.game_series.record(i).value("DictValueName"))
            if self.game.game_data.record(0).value("SeriesId") == self.game.game_series.record(i).value("Id"):
                current_index = i

        self.ui.comboBoxGameEditSeries.setCurrentIndex(current_index)

        current_index_2 = -1

        for i in range(self.game.game_type.rowCount()):
            self.ui.comboBoxGameEditType.addItem(self.game.game_type.record(i).value("DictValueName"))
            if self.game.game_data.record(0).value("GameAtr") == self.game.game_type.record(i).value("Id"):
                current_index_2 = i

        self.ui.comboBoxGameEditType.setCurrentIndex(current_index_2)

        current_index_3 = -1

        for i in range(self.game.game_genre.rowCount()):
            self.ui.comboBoxGameEditGenre.addItem(self.game.game_genre.record(i).value("DictValueName"))
            if self.game.game_data.record(0).value("Genre") == self.game.game_genre.record(i).value("Id"):
                current_index_3 = i

        self.ui.comboBoxGameEditGenre.setCurrentIndex(current_index_3)


        self.data = self.AdditionalData(connector, game_id)


    class Game:
        def __init__(self, connector, game_id):
            self.game_data = QSqlQueryModel()
            self.game_difficulties = QSqlQueryModel()
            self.game_collection = QSqlQueryModel()
            self.game_storage = QSqlQueryModel()
            self.game_notes = QSqlQueryModel()
            self.game_series = QSqlQueryModel()
            self.game_type = QSqlQueryModel()
            self.game_genre = QSqlQueryModel()



            #self.game = dict()
            self.game_data_sql_statement = 'select * from dbo.Games where id = ' + str(game_id)

            self.game_series_sql_statement = 'select Id, InTypeId, DictValueName ' \
                                             'from dbo.Dictionaries where DictType = 6'

            self.game_type_sql_statement = 'select Id, InTypeId, DictValueName ' \
                                             'from dbo.Dictionaries where DictType = 1'

            self.game_genre_sql_statement = 'select Id, InTypeId, DictValueName ' \
                                             'from dbo.Dictionaries where DictType = 2'

            #if connector.db.open():
            if connector.db.isOpen():
                self.qry = QSqlQuery(connector.db)
                self.qry.prepare(self.game_data_sql_statement)
                self.qry.exec()
                self.game_data.setQuery(self.qry)

                while self.game_data.canFetchMore():
                    self.game_data.fetchMore()

            if connector.db.isOpen():
                self.qry = QSqlQuery(connector.db)
                self.qry.prepare(self.game_series_sql_statement)
                self.qry.exec()
                self.game_series.setQuery(self.qry)

                while self.game_series.canFetchMore():
                    self.game_series.fetchMore()

            if connector.db.isOpen():
                self.qry = QSqlQuery(connector.db)
                self.qry.prepare(self.game_type_sql_statement)
                self.qry.exec()
                self.game_type.setQuery(self.qry)

                while self.game_type.canFetchMore():
                    self.game_type.fetchMore()

            if connector.db.isOpen():
                self.qry = QSqlQuery(connector.db)
                self.qry.prepare(self.game_genre_sql_statement)
                self.qry.exec()
                self.game_genre.setQuery(self.qry)

                while self.game_genre.canFetchMore():
                    self.game_genre.fetchMore()

            # for i in

            ### tutaj stworzymy klasę danej gry pobranej z bazy

            ### przy zapisie porównujemy czy wszystko jest takie samo z aktualnymi wartościami






    class AdditionalData:
        def __init__(self, connector, game_id):
            self.querymodel = QSqlQueryModel()
            self.sql_statement = 'select * from dbo.dictionaries'# where GameId = ' + str(game_id)'

            #if connector.db.open():
            if connector.db.isOpen():
                self.qry = QSqlQuery(connector.db)
                self.qry.prepare(self.sql_statement)
                self.qry.exec()

                self.querymodel.setQuery(self.qry)


    def game_edit_save(self):
        self.close()
        self.destroy()
        print(self.ui.comboBoxGameEditSeries.count())
        print(globals())










if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DatabaseConnector()
    win = AppGamesManager(connector=db)
    win.show()
    sys.exit(app.exec_())


