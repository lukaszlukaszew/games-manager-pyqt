import PyQt5

import DialogGameEdit2
from PyQt5.QtWidgets import QDialog, QMessageBox, QLabel, QSizePolicy, QSlider
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import QDate, Qt


class DGameEdit(QDialog):
    def __init__(self, conn, data, game_id):
        super().__init__()
        self.ui = DialogGameEdit2.Ui_Dialog()
        self.ui.setupUi(self)

        self.conn = conn
        self.game_id = game_id
        self.game = data.Game(self.conn, game_id)

        #self.ui.pushButtonGameEditSave.clicked.connect(self.game_edit_save)
        self.ui.pushButtonGameEditCancel.clicked.connect(self.close)
        # TODO jak wywalić % z progress bar?
        self.ui.progressBarGameEditAvgNote.setFormat("%.02f %%" % self.ui.progressBarGameEditAvgNote.value())

        cb = ["Series", "Type", "Genre"]

        for i in cb:
            j = -1
            for k in range(self.game.game[i].rowCount()):
                self.ui.__dict__["comboBoxGameEdit" + i].addItem(self.game.game[i].record(k).value("DictValueName"))
                if self.game_id:
                    if self.game.game[i].record(k).value("Id") == self.game.game["Data"].record(0).value(i+"Id"):
                        j = k

            self.ui.__dict__["comboBoxGameEdit" + i].setCurrentIndex(j)

        self.label = "labelGameEdit"
        self.slider = "horizontalSliderGameEdit"

        for i in range(self.game.game["Notes"].rowCount()):
            note_category = self.game.game["Notes"].record(i).value("DictValueName")
            note = str(self.game.game["Notes"].record(i).value("Note")).replace("NULL", "0")

            self.ui.__dict__[self.label + note_category] = QLabel(self.ui.tabGameEditNotes)
            self.ui.__dict__[self.label + note_category].setText(note_category)
            self.ui.gridLayoutGameEditNotes.addWidget(self.ui.__dict__[self.label + note_category], i, 0, 1, 1)

            self.ui.__dict__[self.label + note_category + "Note"] = QLabel(self.ui.tabGameEditNotes)
            self.ui.gridLayoutGameEditNotes.addWidget(self.ui.__dict__[self.label + note_category + "Note"], i, 1, 1, 1)

            self.ui.__dict__[self.slider + note_category] = QSlider(self.ui.tabGameEditNotes)
            self.ui.__dict__[self.slider + note_category].setMaximum(10)
            self.ui.__dict__[self.slider + note_category].setPageStep(1)
            self.ui.__dict__[self.slider + note_category].setOrientation(Qt.Horizontal)
            self.ui.gridLayoutGameEditNotes.addWidget(self.ui.__dict__[self.slider + note_category], i, 2, 1, 1)

            self.ui.__dict__[self.label + note_category + "Note"].setText(note)
            self.ui.__dict__[self.slider + note_category].setValue(int(note))
            self.ui.__dict__[self.slider + note_category].valueChanged.connect(self.game_edit_avg_note)

            # TODO jak rozwiązać kwestię tłumaczenia w powyższym?
            # TODO jak zrobić, żeby to było ładnie równomiernie rozłożone w pionie, a nie zbite w kupę?
            # TODO jak podpiąć suwak?

        if self.game_id:
            self.ui.lineEditGameEditId.setText(str(game_id))
            self.ui.lineEditGameEditTitle.setText(
                self.game.game["Data"].record(0).value("GameTitle")
            )
            self.ui.dateEditGameEditRelease.setDate(
                QDate.fromString(self.game.game["Data"].record(0).value("ReleaseDate"), "yyyy-MM-dd")
            )

    def game_edit_avg_note(self):
        notes_sum = 0
        notes_count = 0

        for i in self.ui.__dict__.keys():
            if i.startswith(self.label) and i.endswith("Note"):
                type = i.replace(self.label, "").replace("Note", "")
                self.ui.__dict__[i].setText(str(self.ui.__dict__[self.slider + type].value()))
                notes_sum += self.ui.__dict__[self.slider + type].value()
                notes_count += 1

        try:
            notes_avg = notes_sum * 10 / notes_count
        except ZeroDivisionError:
            notes_avg = 0

        self.ui.progressBarGameEditAvgNote.setValue(int(notes_avg * 100))
        self.ui.progressBarGameEditAvgNote.setFormat("%.02f %%" % notes_avg)
    #
    # def game_edit_difficulty_completed(self):
    #     if bool(self.ui.listWidgetGameEditDifficulty.selectedItems()):
    #         rows = self.ui.listWidgetGameEditDifficulty.currentRow() + 1
    #         for i in range(rows):
    #             self.ui.listWidgetGameEditDifficultyComplete.addItem(
    #                 self.ui.listWidgetGameEditDifficulty.item(0).text()
    #             )
    #
    #             self.ui.listWidgetGameEditDifficulty.takeItem(0)
    #
    # def game_difficulty_not_completed(self):
    #     if bool(self.ui.listWidgetGameEditDifficultyComplete.selectedItems()):
    #         rows = self.ui.listWidgetGameEditDifficultyComplete.currentRow()
    #         for i in range(self.ui.listWidgetGameEditDifficultyComplete.count() - 1, rows - 1, -1):
    #             self.ui.listWidgetGameEditDifficulty.insertItem(
    #                 0, self.ui.listWidgetGameEditDifficultyComplete.item(i).text()
    #             )
    #             self.ui.listWidgetGameEditDifficultyComplete.takeItem(i)
    #
    # def game_storage_filter(self):
    #     pass
    #
    #
    # def game_edit_save(self):
    #
    #     check = [self.ui.lineEditGameEditTitle.text(), self.ui.comboBoxGameEditType.currentText(),
    #              self.ui.comboBoxGameEditGenre.currentText()]
    #
    #     """ ok i tutaj ważna rzecz: dodawanie nowej gry i edycja istniejącej będzie oparta o to samo okienko i ta
    #     sama funkcje - rozroznienie, czy to jest edycja, czy nie, bedzie w procedurze w bazie po prostu po tym, czy
    #     @gameid is null
    #     podczas zapisywania beda dzialaly procedury: dodaj gre, dodaj poziomy trudnosci, dodaj ocene, dodaj okladke, dodaj recenzje"""
    #
    #     if all(check) and self.conn.db.isOpen():
    #         query = QSqlQuery()
    #         query.prepare(
    #             "EXEC DodajGre @title = :title, @gameatrid = :atr, @ReleaseDate = :date, @typ = 2, @genreid = :genre, @seriesId = :series")
    #
    #         query.bindValue(":title", self.ui.lineEditGameEditTitle.text())
    #
    #         """ co z serią??"""
    #         print(self.ui.comboBoxGameEditSeries.currentIndex())
    #         if self.ui.comboBoxGameEditSeries.currentIndex() == -1:
    #             query.bindValue(":series", "NULL")
    #         else:
    #             query.bindValue(":series", str(self.game.query_game_series.record(
    #                 self.ui.comboBoxGameEditSeries.currentIndex()).value("Id")))
    #
    #         query.bindValue(":date", self.ui.dateEditGameEditRelease.text())
    #         query.bindValue(":atr",
    #                         str(self.game.query_game_type.record(self.ui.comboBoxGameEditType.currentIndex()).value(
    #                             "Id")))
    #         query.bindValue(":genre",
    #                         str(self.game.query_game_genre.record(self.ui.comboBoxGameEditGenre.currentIndex()).value(
    #                             "Id")))
    #
    #         # query.exec_()
    #         # print(query.lastInsertId())
    #
    #         if query.exec_():
    #             conn.db.commit()
    #             QMessageBox.warning(None, "Confirmation",
    #                                 "Game added")
    #         else:
    #             QMessageBox.warning(None, "Database Error",
    #                                 query.lastError().text())
    #
    #     """ dobra ściągawka """
    #     # db = QSqlDatabase.addDatabase("QMYSQL")
    #     #
    #     # db.setHostName("localhost")
    #     # db.setDatabaseName("vista")
    #     # db.setUserName("root")
    #     # db.setPassword("secret")
    #     #
    #     # if (db.open() == False):
    #     #     QMessageBox.critical(None, "Database Error",
    #     #                          db.lastError().text())
    #     # query = QSqlQuery()
    #     # query.prepare("INSERT INTO user (fio, sex,polis,document,birtday) "
    #     #               "VALUES (:fio, :sex,:polis,:document,:birtday)");
    #     # query.bindValue(":fio", fio);
    #     # query.bindValue(":sex", sex);
    #     # query.bindValue(":polis", polis);
    #     # query.bindValue(":document", document);
    #     # query.bindValue(":birtday", birtday);
    #     # query.exec_();
    #
    # class Game:
    #     def __init__(self, conn, game_id):
    #         if game_id is not None:
    #             self.query_game_data = QSqlQueryModel()
    #             self.sql_game_data = 'select * from dbo.Games where id = ' + str(game_id)
    #
    #             self.query_game_notes = QSqlQueryModel()
    #             self.sql_game_notes = 'select NoteCategory, Note from dbo.GamesNotes where GameId = ' + str(game_id)
    #
    #             self.query_game_collection = QSqlQueryModel()
    #             self.sql_game_collection = 'select * from dbo.Collection_View where Id = ' + str(game_id)
    #
    #             self.query_game_difficulties = QSqlQueryModel()
    #             self.sql_game_difficulties = 'select * from dbo.Difficulties_View where Id = ' + str(
    #                 game_id) + 'order by InGameNumber'
    #
    #             self.query_game_data = conn.sql_query_model_fetch(self.query_game_data, self.sql_game_data)
    #             self.query_game_notes = conn.sql_query_model_fetch(self.query_game_notes, self.sql_game_notes)
    #             self.query_game_collection = conn.sql_query_model_fetch(self.query_game_collection,
    #                                                                          self.sql_game_collection)
    #             self.query_game_difficulties = conn.sql_query_model_fetch(self.query_game_difficulties,
    #                                                                            self.sql_game_difficulties)
    #
    #         self.query_game_series = QSqlQueryModel()
    #         self.sql_game_series = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 6 order by DictValueName'
    #
    #         self.query_game_type = QSqlQueryModel()
    #         self.sql_game_type = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 1'
    #
    #         self.query_game_genre = QSqlQueryModel()
    #         self.sql_game_genre = 'select Id, InTypeId, DictValueName from dbo.Dictionaries where DictType = 2'
    #
    #         # self.game_storage = QSqlQueryModel()
    #
    #         self.query_game_series = conn.sql_query_model_fetch(self.query_game_series, self.sql_game_series)
    #         self.query_game_type = conn.sql_query_model_fetch(self.query_game_type, self.sql_game_type)
    #         self.query_game_genre = conn.sql_query_model_fetch(self.query_game_genre, self.sql_game_genre)
    #
    #         ### przy zapisie porównujemy czy wszystko jest takie samo z aktualnymi wartościami, ale po stronie bazy
    #
    #
