import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import QDate

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
        self.ui.pushButtonGamesAdd.clicked.connect(self.dialog_game_add)

        self.sql_games_list = 'select * from dbo.Games_View where id = 4 order by ReleaseDate'
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

    def dialog_game_add(self):
        dialog = DGameEdit(self.connector, None)
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
            qry.exec_()

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

        self.game = self.Game(connector, game_id)

        if game_id is not None:
            self.ui.pushButtonGameEditSave.clicked.connect(self.game_edit_save)
        else:
            self.ui.pushButtonGameEditSave.clicked.connect(lambda: self.game_add(connector))

        self.ui.pushButtonGameEditCancel.clicked.connect(self.close)

        current_index = -1

        for i in range(self.game.query_game_series.rowCount()):
            self.ui.comboBoxGameEditSeries.addItem(self.game.query_game_series.record(i).value("DictValueName"))
            if game_id is not None:
                if self.game.query_game_data.record(0).value("SeriesId") == self.game.query_game_series.record(i).value(
                        "Id"):
                    current_index = i

        self.ui.comboBoxGameEditSeries.setCurrentIndex(current_index)

        current_index_2 = -1

        for i in range(self.game.query_game_type.rowCount()):
            self.ui.comboBoxGameEditType.addItem(self.game.query_game_type.record(i).value("DictValueName"))
            if game_id is not None:
                if self.game.query_game_data.record(0).value("GameAtr") == self.game.query_game_type.record(i).value("Id"):
                    current_index_2 = i

        self.ui.comboBoxGameEditType.setCurrentIndex(current_index_2)

        current_index_3 = -1

        for i in range(self.game.query_game_genre.rowCount()):
            self.ui.comboBoxGameEditGenre.addItem(self.game.query_game_genre.record(i).value("DictValueName"))
            if game_id is not None:
                if self.game.query_game_data.record(0).value("Genre") == self.game.query_game_genre.record(i).value("Id"):
                    current_index_3 = i

        self.ui.comboBoxGameEditGenre.setCurrentIndex(current_index_3)


        if game_id is not None:
            self.ui.progressBarGameEditAvgNote.setFormat("%.02f %%" % self.ui.progressBarGameEditAvgNote.value())
            self.ui.pushButtonGameEditSave.clicked.connect(self.game_edit_save)
            self.ui.horizontalSliderGameEditGraphics.valueChanged.connect(self.game_avg_note)
            self.ui.horizontalSliderGameEditSound.valueChanged.connect(self.game_avg_note)
            self.ui.horizontalSliderGameEditPlayability.valueChanged.connect(self.game_avg_note)
            self.ui.horizontalSliderGameEditStory.valueChanged.connect(self.game_avg_note)
            self.ui.horizontalSliderGameEditAmbience.valueChanged.connect(self.game_avg_note)
            self.ui.horizontalSliderGameEditOptimization.valueChanged.connect(self.game_avg_note)
            self.ui.horizontalSliderGameEditFun.valueChanged.connect(self.game_avg_note)
            self.ui.pushButtonGameEditDifficultyCompleted.clicked.connect(self.game_difficulty_completed)
            self.ui.pushButtonGameEditDifficultyNotCompleted.clicked.connect(self.game_difficulty_not_completed)
            self.ui.listWidgetGameEditCollection.currentRowChanged.connect(self.game_storage_filter)



            self.ui.lineEditGameEditId.setText(str(game_id))
            self.ui.lineEditGameEditTitle.setText(self.game.query_game_data.record(0).value("GameTitle"))

            date = QDate(
                int(self.game.query_game_data.record(0).value("ReleaseDate")[:4]),
                int(self.game.query_game_data.record(0).value("ReleaseDate")[5:7]),
                int(self.game.query_game_data.record(0).value("ReleaseDate")[8:10])
            )
            self.ui.dateEditGameEditRelease.setDate(date)

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

            for i in range(self.game.query_game_collection.rowCount()):
                self.ui.listWidgetGameEditCollection.addItem(
                    self.game.query_game_collection.record(i).value("DictValueName"))

            for i in range(self.game.query_game_difficulties.rowCount()):
                if self.game.query_game_difficulties.record(i).value("Completed"):
                    self.ui.listWidgetGameEditDifficultyComplete.addItem(
                        self.game.query_game_difficulties.record(i).value("DictValueName")
                    )
                else:
                    self.ui.listWidgetGameEditDifficulty.addItem(
                        self.game.query_game_difficulties.record(i).value("DictValueName")
                    )



    def game_avg_note(self):
        self.ui.labelGameEditGraphics.setText(str(self.ui.horizontalSliderGameEditGraphics.value()))
        self.ui.labelGameEditSound.setText(str(self.ui.horizontalSliderGameEditSound.value()))
        self.ui.labelGameEditPlayability.setText(str(self.ui.horizontalSliderGameEditPlayability.value()))
        self.ui.labelGameEditAmbience.setText(str(self.ui.horizontalSliderGameEditAmbience.value()))
        self.ui.labelGameEditOptimization.setText(str(self.ui.horizontalSliderGameEditOptimization.value()))
        self.ui.labelGameEditFun.setText(str(self.ui.horizontalSliderGameEditFun.value()))
        self.ui.labelGameEditStory.setText(str(self.ui.horizontalSliderGameEditStory.value()))

        summary = self.ui.horizontalSliderGameEditGraphics.value() + self.ui.horizontalSliderGameEditSound.value() + \
                  self.ui.horizontalSliderGameEditPlayability.value() + \
                  self.ui.horizontalSliderGameEditAmbience.value() + \
                  self.ui.horizontalSliderGameEditOptimization.value() + self.ui.horizontalSliderGameEditFun.value() + \
                  self.ui.horizontalSliderGameEditStory.value()

        summary = summary * 10 / 7

        self.ui.progressBarGameEditAvgNote.setValue(int(summary * 100))
        self.ui.progressBarGameEditAvgNote.setFormat("%.02f %%" % summary)

    def game_difficulty_completed(self):
        if bool(self.ui.listWidgetGameEditDifficulty.selectedItems()):
            rows = self.ui.listWidgetGameEditDifficulty.currentRow() + 1
            for i in range(rows):
                self.ui.listWidgetGameEditDifficultyComplete.addItem(
                    self.ui.listWidgetGameEditDifficulty.item(0).text()
                )

                self.ui.listWidgetGameEditDifficulty.takeItem(0)

    def game_difficulty_not_completed(self):
        if bool(self.ui.listWidgetGameEditDifficultyComplete.selectedItems()):
            rows = self.ui.listWidgetGameEditDifficultyComplete.currentRow()
            for i in range(self.ui.listWidgetGameEditDifficultyComplete.count()-1, rows-1, -1):
                self.ui.listWidgetGameEditDifficulty.insertItem(
                    0, self.ui.listWidgetGameEditDifficultyComplete.item(i).text()
                )
                self.ui.listWidgetGameEditDifficultyComplete.takeItem(i)

    def game_storage_filter(self):
        pass

    def game_edit_save(self):
        pass

    def game_add(self, connector):

        check = [self.ui.lineEditGameEditTitle.text(), self.ui.comboBoxGameEditType.currentText(),
                 self.ui.comboBoxGameEditGenre.currentText()]
        print("A")
        print(all(check))
        print(connector.db.isOpen())

        if all(check) and connector.db.isOpen():
            query = QSqlQuery()
            query.prepare("EXEC DodajGre @title = :title, @gameatrid = :atr, @ReleaseDate = :date, @typ = 2, @genreid = :genre")

            query.bindValue(":title", self.ui.lineEditGameEditTitle.text())
            print(self.ui.lineEditGameEditTitle.text())

            #if self.ui.comboBoxGameEditSeries.currentIndex() != -1:
            #    query.bindValue(":series", "NULL")
            #else:
            #    query.bindValue(":series", self.game.query_game_series.record(self.ui.comboBoxGameEditSeries.currentIndex()).value("Id"))

            query.bindValue(":date", self.ui.dateEditGameEditRelease.text())
            print(self.ui.dateEditGameEditRelease.text())
            query.bindValue(":atr", str(self.game.query_game_type.record(self.ui.comboBoxGameEditType.currentIndex()).value("Id")))
            print(self.game.query_game_type.record(self.ui.comboBoxGameEditType.currentIndex()).value("Id"))
            query.bindValue(":genre", str(self.game.query_game_genre.record(self.ui.comboBoxGameEditGenre.currentIndex()).value("Id")))
            print(self.game.query_game_genre.record(self.ui.comboBoxGameEditGenre.currentIndex()).value("Id"))

            #query.exec_()
            print(query.lastInsertId())

            if query.exec_():
                connector.db.commit()
            else:
                QMessageBox.warning(None, "Database Error",
                                    query.lastError().text())

        """ dobra ściągawka """
        # db = QSqlDatabase.addDatabase("QMYSQL")
        #
        # db.setHostName("localhost")
        # db.setDatabaseName("vista")
        # db.setUserName("root")
        # db.setPassword("secret")
        #
        # if (db.open() == False):
        #     QMessageBox.critical(None, "Database Error",
        #                          db.lastError().text())
        # query = QSqlQuery()
        # query.prepare("INSERT INTO user (fio, sex,polis,document,birtday) "
        #               "VALUES (:fio, :sex,:polis,:document,:birtday)");
        # query.bindValue(":fio", fio);
        # query.bindValue(":sex", sex);
        # query.bindValue(":polis", polis);
        # query.bindValue(":document", document);
        # query.bindValue(":birtday", birtday);
        # query.exec_();


    class Game:
        def __init__(self, connector, game_id):
            if game_id is not None:
                self.query_game_data = QSqlQueryModel()
                self.sql_game_data = 'select * from dbo.Games where id = ' + str(game_id)

                self.query_game_notes = QSqlQueryModel()
                self.sql_game_notes = 'select NoteCategory, Note from dbo.GamesNotes where GameId = ' + str(game_id)

                self.query_game_collection = QSqlQueryModel()
                self.sql_game_collection = 'select * from dbo.Collection_View where Id = ' + str(game_id)

                self.query_game_difficulties = QSqlQueryModel()
                self.sql_game_difficulties = 'select * from dbo.Difficulties_View where Id = ' + str(
                    game_id) + 'order by InGameNumber'

                self.query_game_data = connector.sql_query_model_fetch(self.query_game_data, self.sql_game_data)
                self.query_game_notes = connector.sql_query_model_fetch(self.query_game_notes, self.sql_game_notes)
                self.query_game_collection = connector.sql_query_model_fetch(self.query_game_collection,
                                                                             self.sql_game_collection)
                self.query_game_difficulties = connector.sql_query_model_fetch(self.query_game_difficulties,
                                                                             self.sql_game_difficulties)

            self.query_game_series = QSqlQueryModel()
            self.sql_game_series = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 6'

            self.query_game_type = QSqlQueryModel()
            self.sql_game_type = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 1'

            self.query_game_genre = QSqlQueryModel()
            self.sql_game_genre = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 2'

            #self.game_storage = QSqlQueryModel()


            self.query_game_series = connector.sql_query_model_fetch(self.query_game_series, self.sql_game_series)
            self.query_game_type = connector.sql_query_model_fetch(self.query_game_type, self.sql_game_type)
            self.query_game_genre = connector.sql_query_model_fetch(self.query_game_genre, self.sql_game_genre)


            ### przy zapisie porównujemy czy wszystko jest takie samo z aktualnymi wartościami



if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = DatabaseConnector()
    win = AppGamesManager(connector=db)
    win.show()
    sys.exit(app.exec_())


# TODO - storage po stronie bazy
# TODO - filtrowanie listy storage, gdy jest focus na collection odpowiednim
# TODO - data wydania
# TODO - zapisywanie i edycja bazy
# TODO - wywalenie % z progressBara
# TODO - reformat nr II

# TODO - dodawanie serii
# TODO - dodawanie typu
# TODO - dodawanie gatunku
# TODO - dodawanie kolekcji
# TODO - dodawanie storage
# TODO - dodawanie poziomu trudności (zabezpieczneie, żeby nie dodawać tego samego)
# TODO - dodawanie okładki
# TODO - reformat nr III

# TODO - zakładka recenzji

# TODO - dodawanie nowej gry


# TODO - oprzeć się na procedurach w bazie

# TODO - projekt akcji refresh
# TODO - akcja refresh

# TODO - projekt akcji about
# TODO - akcja about

# TODO - projekt akcji SETTINGS
# TODO - akcja settings (rozdzielczość, motyw,

# TODO - projekt okienka NOTES
# TODO - akcja NOTES

# TODO - projekt okienka DICTS
# TODO - akcja DICTS

# TODO - projekt okienka TAGS
# TODO - akcja TAGS

# TODO - projekt okienka REVIEWS
# TODO - akcja REVIEWS

# TODO - projekt okienka STORAGE
# TODO - akcja STORAGE

# TODO - projekt okienka COLLECTION
# TODO - akcja COLLECTION

# TODO - projekt raportów zdefiniowanych