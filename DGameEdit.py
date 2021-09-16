from PyQt5 import QtCore

import DialogGameEdit
from PyQt5.QtWidgets import QDialog, QMessageBox, QLabel, QSizePolicy, QSlider, QInputDialog
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel, QSqlRelationalTableModel
from PyQt5.QtCore import QDate, Qt


# TODO wywalić z całego okienka fragment "GameEdit"
# TODO zrobic, zeby dzialalo bez game_id


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
            "Save": "game_edit_save",
            "Cancel": "close",
            # "CoverAdd": "game_edit_add_cover",
            # "CoverDelete": "game_edit_delete_cover",
            "DifficultiesAdd": "game_edit_add_dict_value",
            "DifficultiesToList": "game_edit_add_from_dict_value",
            "DifficultiesDelete":"game_edit_remove_from_list",
            "DifficultiesCompleted": "game_edit_difficulty_completed",
            "DifficultiesNotCompleted": "game_edit_difficulty_not_completed",
            "CollectionAdd": "game_edit_add_dict_value",
            "CollectionToList": "game_edit_add_from_dict_value",
            "CollectionDelete": "game_edit_remove_from_list",
            "SeriesAdd": "game_edit_add_dict_value",
            "CategoryAdd": "game_edit_add_dict_value",
            "GenreAdd": "game_edit_add_dict_value",
            "StorageAdd": "game_edit_add_dict_value",
            "NotesAdd" : "game_edit_add_dict_value",
            "StorageToList": "game_edit_add_from_dict_value",
            "StorageDelete": "game_edit_remove_from_list",
        }

        for k, v in self.buttons.items():
            self.ui.__dict__[self.button + k].clicked.connect(getattr(self, v))

        self.ui.listWidgetGameEditCollection.currentRowChanged.connect(self.game_edit_storage_filter)

        self.ui.progressBarGameEditAvgNote.setFormat(str(self.ui.progressBarGameEditAvgNote.value()).format(".2f"))

        self.game_edit_dictionaries()
        self.game_edit_difficulties()
        self.game_edit_collection()
        self.game_edit_notes()

        if self.game_id:
            self.game_edit_basic_info()

    def game_edit_basic_info(self):
        self.ui.lineEditGameEditId.setText(str(self.game_id))
        self.ui.lineEditGameEditTitle.setText(self.game.game["Data"].record(0).value("Name"))
        self.ui.dateEditGameEditRelease.setDate(
            QDate.fromString(self.game.game["Data"].record(0).value("Release_date"), "yyyy-MM-dd")
        )

    def game_edit_dictionaries(self):
        cb = ["Series", "Category", "Genre"]

        for i in cb:
            j = -1
            for k in range(self.game.game[i].rowCount()):
                self.ui.__dict__["comboBoxGameEdit" + i].addItem(self.game.game[i].record(k).value("Name"))
                if self.game_id:
                    if self.game.game[i].record(k).value("Id") == self.game.game["Data"].record(0).value(i + "_id"):
                        j = k

            self.ui.__dict__["comboBoxGameEdit" + i].setCurrentIndex(j)

    def game_edit_notes(self):
        for i in range(self.game.game["Notes"].rowCount()):
            note_category = self.game.game["Notes"].record(i).value("Name")
            note = str(self.game.game["Notes"].record(i).value("Note"))

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
            if self.game.game["Difficulties"].record(i).value("Game_id"):
                if self.game.game["Difficulties"].record(i).value("Completed"):
                    self.ui.listWidgetGameEditDifficultiesComplete.addItem(
                        self.game.game["Difficulties"].record(i).value("Name")
                    )
                else:
                    self.ui.listWidgetGameEditDifficulties.addItem(


                        self.game.game["Difficulties"].record(i).value("Name")
                    )

    def game_edit_collection(self):
        collection = list()
        for i in range(self.game.game["Collection"].rowCount()):
            if self.game.game["Collection"].record(i).value("Collection_name") not in collection and \
                    self.game.game["Collection"].record(i).value("Game_id"):
                self.ui.listWidgetGameEditCollection.addItem(
                    self.game.game["Collection"].record(i).value("Name")
                )
                collection.append(self.game.game["Collection"].record(i).value("Collection_name"))
                for j in range(self.game.game["Storage"].rowCount()):
                    if self.game.game["Storage"].record(j).value("Id") == \
                            self.game.game["Collection"].record(i).value("Id"):
                        self.ui.listWidgetGameEditStorage.addItem(
                            self.game.game["Storage"].record(i).value("Name")
                        )

    def game_edit_avg_note(self):
        notes_sum = 0
        notes_count = 0

        for i in self.ui.__dict__.keys():
            if i.startswith(self.label) and i.endswith("Note"):
                itype = i.replace(self.label, "").replace("Note", "")
                self.ui.__dict__[i].setText(str(self.ui.__dict__[self.slider + itype].value()))
                notes_sum += self.ui.__dict__[self.slider + itype].value()
                notes_count += 1

        try:
            notes_avg = notes_sum / notes_count
        except ZeroDivisionError:
            notes_avg = 0

        self.ui.progressBarGameEditAvgNote.setValue(int(notes_avg * 1000))
        self.ui.progressBarGameEditAvgNote.setFormat(str(round(notes_avg, 2)).format(".2f"))

    def game_edit_difficulty_completed(self):
        if bool(self.ui.listWidgetGameEditDifficulties.selectedItems()):
            rows = self.ui.listWidgetGameEditDifficulties.currentRow() + 1
            for i in range(rows):
                self.ui.listWidgetGameEditDifficultiesComplete.addItem(
                    self.ui.listWidgetGameEditDifficulties.item(0).text()
                )

                self.ui.listWidgetGameEditDifficulties.takeItem(0)

    def game_edit_difficulty_not_completed(self):
        if bool(self.ui.listWidgetGameEditDifficultiesComplete.selectedItems()):
            rows = self.ui.listWidgetGameEditDifficultiesComplete.currentRow()
            for i in range(self.ui.listWidgetGameEditDifficultiesComplete.count() - 1, rows - 1, -1):
                self.ui.listWidgetGameEditDifficulties.insertItem(
                    0, self.ui.listWidgetGameEditDifficultiesComplete.item(i).text()
                )
                self.ui.listWidgetGameEditDifficultiesComplete.takeItem(i)

    def game_edit_storage_filter(self):
        # filtrujemy liste nr 2 na podstawie listy nr 1
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
        dictionary = self.sender().objectName().replace(self.button, "").replace("Add", "")
        value, ok = QInputDialog.getText(self, dictionary, "Please input new value:")


        if value and ok:
            sql = "EXEC dbo.GamesDataManipulate @type = :dictionary, @value = :value"
            query = QSqlQuery()
            query.prepare(sql)

            query.bindValue(":dictionary", dictionary)
            query.bindValue(":value", value)

            if query.exec_():
                self.conn.db.commit()
                QMessageBox.warning(None, "Confirmation",
                                    "Value added")
            else:
                QMessageBox.warning(None, "Database Error",
                                    query.lastError().text())

            qry = QSqlQuery(self.conn.db)
            qry.prepare(self.game.sql[dictionary])

            if ":id" in self.game.sql[dictionary]:
                if self.game_id:
                    qry.bindValue(':id', self.game_id)
                else:
                    qry.bindValue(':id', 0)

            self.game.game[dictionary] = QSqlQueryModel()
            self.game.game[dictionary] = self.conn.sql_query_model_fetch(self.game.game[dictionary], qry)

        cb = ["Series", "Category", "Genre"]

        if dictionary in cb:
            for i in cb:
                self.ui.__dict__["comboBoxGameEdit" + i].clear()

            self.game_edit_dictionaries()

        if dictionary == "Notes":
            self.game_edit_notes()

    def game_edit_add_from_dict_value(self):
        dictionary = self.sender().objectName().replace(self.button, "").replace("ToList", "")

        items = set([self.ui.__dict__["listWidgetGameEdit" + dictionary].item(x).text() for x in
                 range(self.ui.__dict__["listWidgetGameEdit" + dictionary].count())])
        temp = set([self.game.game[dictionary].record(x).value("Name") for x in
                range(self.game.game[dictionary].rowCount())])

        temp = temp.difference(items)

        if len(temp):
            value, ok = QInputDialog.getItem(self, dictionary, "Please input new value:", temp)

            if value and ok:
                if value not in items:
                    self.ui.__dict__["listWidgetGameEdit" + dictionary].addItem(value)
        else:
            QMessageBox.warning(None, "Database Error", "Empty dict in database " + dictionary)

        # TODO jeżeli storage to trzeba jeszcze wywołać collection

    def game_edit_remove_from_list(self):
        dictionary = self.sender().objectName().replace(self.button, "").replace("Delete", "")
        self.ui.__dict__["listWidgetGameEdit" + dictionary].takeItem(self.ui.__dict__["listWidgetGameEdit" + dictionary].currentRow())

    def game_edit_save(self):
        check = [self.ui.lineEditGameEditTitle.text(), self.ui.comboBoxGameEditCategory.currentText(),
                 self.ui.comboBoxGameEditGenre.currentText()]

        if all(check) and self.conn.db.isOpen():
            query = QSqlQuery()

            sql = "EXEC dbo.GamesDataManipulate @name = :name, @category = :category, @date = :date, @genre = :genre, @series = :series, @type = 'ADDGAME'"

            if self.game_id:
                sql += ", @id = :id"

            query.prepare(sql)

            if self.game_id:
                query.bindValue(':id', self.game_id)

            query.bindValue(":name", self.ui.lineEditGameEditTitle.text())

            if self.ui.comboBoxGameEditSeries.currentIndex() == -1:
                query.bindValue(":series", "NULL")
            else:
                query.bindValue(":series", self.game.game["Series"].record(
                    self.ui.comboBoxGameEditSeries.currentIndex()).value("Id"))

            query.bindValue(":date", self.ui.dateEditGameEditRelease.text())

            query.bindValue(":category", self.game.game["Category"].record(self.ui.comboBoxGameEditCategory.currentIndex()).value(
                                "Id"))

            query.bindValue(":genre",
                            self.game.game["Genre"].record(self.ui.comboBoxGameEditGenre.currentIndex()).value(
                                "Id"))

            # cb = ["Series", "Category", "Genre"]
            #
            # for i in cb:
            #     print(i, self.ui.__dict__["comboBoxGameEdit" + i].currentIndex(),
            #           self.ui.__dict__["comboBoxGameEdit" + i].currentText())

            if query.exec_():
                self.conn.db.commit()
                QMessageBox.warning(None, "Confirmation",
                                    "Game added")
            else:
                QMessageBox.warning(None, "Database Error",
                                    query.lastError().text())

            if not self.game_id:
                self.game_id = query.lastInsertId()

            # NOTES

            if self.game_id:
                qry = QSqlQuery()

                for i in range(self.game.game["Notes"].rowCount()):
                    sql = "EXEC dbo.GamesDataManipulate @note_id = :note_id, @id = :id, @note = :note, @type = 'ADDNOTES'"
                    qry.prepare(sql)

                    qry.bindValue(":id", self.game_id)
                    qry.bindValue(":note_id", self.game.game["Notes"].record(i).value("Id"))
                    qry.bindValue(":note", self.ui.__dict__[self.slider + self.game.game["Notes"].record(i).value("Name")].value())

                    if qry.exec_():
                        self.conn.db.commit()


                    else:
                        QMessageBox.warning(None, "Database Error",
                                            qry.lastError().text())

                    print(qry.boundValues())

            # COLLECTION

            """ tutaj trzeba uwzględnić także usuwanie"""

            # DIFFICULTIES

            """ tutaj trzeba uwzględnić także usuwanie, czyli tak --- ustalamy listę wysyłamy do """


            # TODO jak rozwiązać dodawnie storage?

            self.close()

        else:
            QMessageBox.warning(None, "Data Error",
                                "You forgot about parameter")