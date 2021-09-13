import DialogGameEdit
from PyQt5.QtWidgets import QDialog, QMessageBox, QLabel, QSizePolicy, QSlider, QInputDialog
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import QDate, Qt

# TODO wywalić z całego okienka fragment "GameEdit"

class DGameEdit(QDialog):
    def __init__(self, conn, data, game_id):
        super().__init__()
        self.ui = DialogGameEdit.Ui_Dialog()
        self.ui.setupUi(self)

        self.conn = conn
        self.game_id = game_id
        self.label = "labelGameEdit"
        self.slider = "horizontalSliderGameEdit"
        self.button = "pushButtonGameEdit"
        self.game = data.Game(self.conn, game_id)

        self.buttons = {
            # "Save": "game_edit_save",
            "Cancel": "close",
            # "CoverAdd": "game_edit_add_cover",
            # "CoverDelete": "game_edit_delete_cover",
            # "DifficultyAdd": "",
            # "DifficultyDelete":"",
            "DifficultyCompleted": "game_edit_difficulty_completed",
            "DifficultyNotCompleted": "game_edit_difficulty_not_completed",
            # "CollectionAdd": "",
            # "CollectionDelete": "",
            "SeriesAdd": "game_edit_add_dict_value",
            # "TypeAdd": "game_edit_add_dict_value",
            # "GenreAdd": "game_edit_add_dict_value",
            # "StorageAdd": "",
            # "StorageDelete": "",


        }

        for k, v in self.buttons.items():
            self.ui.__dict__[self.button + k].clicked.connect(getattr(self, v))

        self.ui.progressBarGameEditAvgNote.setFormat(str(self.ui.progressBarGameEditAvgNote.value()).format(".2f"))

        self.game_edit_dictionaries()

        if self.game_id:
            self.game_edit_notes()
            self.game_edit_basic_info()
            self.game_edit_collection()
            self.game_edit_difficulties()

    def game_edit_basic_info(self):
        self.ui.lineEditGameEditId.setText(str(self.game_id))
        self.ui.lineEditGameEditTitle.setText(self.game.game["Data"].record(0).value("GameTitle"))
        self.ui.dateEditGameEditRelease.setDate(
            QDate.fromString(self.game.game["Data"].record(0).value("ReleaseDate"), "yyyy-MM-dd")
        )

    def game_edit_dictionaries(self):
        cb = ["Series", "Type", "Genre"]

        for i in cb:
            j = -1
            for k in range(self.game.game[i].rowCount()):
                self.ui.__dict__["comboBoxGameEdit" + i].addItem(self.game.game[i].record(k).value("DictValueName"))
                if self.game_id:
                    if self.game.game[i].record(k).value("Id") == self.game.game["Data"].record(0).value(i+"Id"):
                        j = k

            self.ui.__dict__["comboBoxGameEdit" + i].setCurrentIndex(j)

    def game_edit_notes(self):
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
            self.ui.__dict__[self.slider + note_category].valueChanged.connect(self.game_edit_avg_note)
            self.ui.__dict__[self.slider + note_category].setValue(int(note))

            # TODO jak rozwiązać kwestię tłumaczenia w powyższym?
            # TODO jak zrobić, żeby to było ładnie równomiernie rozłożone w pionie, a nie zbite w kupę?
            # TODO jak zrobić, żeby oceny w label nie wpływały na rozmiar sliderów?
            # TODO jak podpiąć suwak?

    def game_edit_difficulties(self):
        for i in range(self.game.game["Difficulties"].rowCount()):
            if self.game.game["Difficulties"].record(i).value("Completed"):
                self.ui.listWidgetGameEditDifficultyComplete.addItem(
                    self.game.game["Difficulties"].record(i).value("DictValueName")
                )
            else:
                self.ui.listWidgetGameEditDifficulty.addItem(
                    self.game.game["Difficulties"].record(i).value("DictValueName")
                )

    def game_edit_collection(self):
        for i in range(self.game.game["Collection"].rowCount()):
            self.ui.listWidgetGameEditCollection.addItem(
                self.game.game["Collection"].record(i).value("DictValueName"))

        # TODO dolozyc Storage

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
            notes_avg = notes_sum / notes_count
        except ZeroDivisionError:
            notes_avg = 0

        self.ui.progressBarGameEditAvgNote.setValue(int(notes_avg * 1000))
        self.ui.progressBarGameEditAvgNote.setFormat(str(round(notes_avg, 2)).format(".2f"))

    def game_edit_difficulty_completed(self):
        if bool(self.ui.listWidgetGameEditDifficulty.selectedItems()):
            rows = self.ui.listWidgetGameEditDifficulty.currentRow() + 1
            for i in range(rows):
                self.ui.listWidgetGameEditDifficultyComplete.addItem(
                    self.ui.listWidgetGameEditDifficulty.item(0).text()
                )

                self.ui.listWidgetGameEditDifficulty.takeItem(0)

    def game_edit_difficulty_not_completed(self):
        if bool(self.ui.listWidgetGameEditDifficultyComplete.selectedItems()):
            rows = self.ui.listWidgetGameEditDifficultyComplete.currentRow()
            for i in range(self.ui.listWidgetGameEditDifficultyComplete.count() - 1, rows - 1, -1):
                self.ui.listWidgetGameEditDifficulty.insertItem(
                    0, self.ui.listWidgetGameEditDifficultyComplete.item(i).text()
                )
                self.ui.listWidgetGameEditDifficultyComplete.takeItem(i)

    def game_edit_storage_filter(self):
        pass

    def game_edit_add_cover(self):
        # otwieramy okienko do wyboru obrazu
        # wczytujemy obraz
        # przerabiamy format obrazu
        # podczas zapisu:
            # zapisujemy obraz w bazie
            # ustawiamy obraz w odpowiednim polu
            # zamykamy okienko
        pass

    def game_edit_delete_cover(self):
        # wyświetlamy komunikat, czy na pewno
        # podczas zapisu
            # usuwamy obraz z bazy
            # usuwamy obraz z odpowiedniego pola
        pass

    def game_edit_add_dict_value(self):
        # okienko, które wie jaki słownik ma edytować
        # wpisujemy wartość, zapisujemy lub wychodzimy
        # podczas zapisu:
            # dodajemy odpowiednią wartość do bazy
            # ponownie pobieramy model z bazy
            # usuwamy wszystkie itemy odpowiedniego comboboxa
            # ponownie dodajemy itemy do comboboxa
            # zamykamy okienko
        pass

    def game_edit_add_collection(self):
        pass

    def game_edit_add_storage(self):
        # sprawdzamy na czym jest focus i wybieramy odpowiednią listę
        pass

    def game_edit_add_difficulty(self):
        pass

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
    #         ### przy zapisie porównujemy czy wszystko jest takie samo z aktualnymi wartościami, ale po stronie bazy
