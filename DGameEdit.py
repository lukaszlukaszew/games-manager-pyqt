from PyQt5 import QtCore

import DialogGameEdit
from PyQt5.QtWidgets import QDialog, QMessageBox, QLabel, QSlider, QInputDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap


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
        self.cover = 1
        self.game = data.Game(self.conn, game_id)
        self.scene = QGraphicsScene(self)
        self.pixmap = QPixmap()
        self.image_item = QGraphicsPixmapItem(self.pixmap)

        self.buttons = {
            "Save": "game_edit_save",
            "Cancel": "close",
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

        #self.ui.listWidgetGameEditCollection.currentRowChanged.connect(self.game_edit_storage_filter)

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
        self.ui.textEditGameEditReview.setText(self.game.game["Review"].record(0).value("Review"))


        self.pixmap.load("covers/" + str(self.game_id) + ".jpg")
        self.pixmap = self.pixmap.scaled(self.ui.graphicsViewGameEditCover.width()-20, self.ui.graphicsViewGameEditCover.height()-20, aspectRatioMode=Qt.KeepAspectRatio)
        self.image_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.image_item)
        self.ui.graphicsViewGameEditCover.setScene(self.scene)

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
        cs = ["Storage", "Collection"]
        for i in cs:
            for j in range(self.game.game[i].rowCount()):
                if self.game.game[i].record(j).value("Game_id"):
                    self.ui.__dict__["listWidgetGameEdit"+i].addItem(
                        self.game.game[i].record(j).value("Name")
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

        if dictionary == "Difficulties":
            itemsc = set([self.ui.__dict__["listWidgetGameEdit" + dictionary+"Complete"].item(x).text() for x in
                 range(self.ui.__dict__["listWidgetGameEdit" + dictionary+"Complete"].count())])

            temp = temp.difference(itemsc)

        temp = temp.difference(items)

        if len(temp):
            value, ok = QInputDialog.getItem(self, dictionary, "Please input new value:", temp)

            if value and ok:
                if value not in items:
                    self.ui.__dict__["listWidgetGameEdit" + dictionary].addItem(value)
        else:
            QMessageBox.warning(None, "Database Error", "Empty dict in database " + dictionary)

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
                query.bindValue(":series", None)
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


                # COLLECTION

                """ tutaj trzeba uwzględnić także usuwanie"""

                qry2 = QSqlQuery()
                sql2 = "EXEC dbo.GamesDataManipulate @id = :id, @type = 'FINDCOLL'"

                qry2.prepare(sql2)
                qry2.bindValue(":id", self.game_id)

                if qry2.exec_():
                    self.conn.db.commit()

                else:
                    QMessageBox.warning(None, "Database Error",
                                        qry2.lastError().text())

                for i in range(self.ui.listWidgetGameEditCollection.count()):
                    qry = QSqlQuery()
                    sql = "EXEC dbo.GamesDataManipulate @collection = :collection, @id = :id, @type = 'ADDCOLL'"
                    qry.prepare(sql)
                    # to bedzie slabe, bo sie bedzie wywalac jak slownik bedzie pusty... trzeba bedzie przetestowac na pustej bazie
                    for j in range(self.game.game["Collection"].rowCount()):
                        if self.game.game["Collection"].record(j).value("Name") == self.ui.listWidgetGameEditCollection.item(i).text():
                            qry.bindValue(":collection", self.game.game["Collection"].record(j).value("Id"))


                    qry.bindValue(":id", self.game_id)

                    if qry.exec_():
                        self.conn.db.commit()

                    else:
                        QMessageBox.warning(None, "Database Error",
                                            qry.lastError().text())

                qry2 = QSqlQuery()
                sql2 = "EXEC dbo.GamesDataManipulate @id = :id, @type = 'CLEANCOLL'"

                qry2.prepare(sql2)

                qry2.bindValue(":id", self.game_id)

                if qry2.exec_():
                    self.conn.db.commit()

                else:
                    QMessageBox.warning(None, "Database Error",
                                        qry2.lastError().text())

                # STORAGE

                qry2 = QSqlQuery()
                sql2 = "EXEC dbo.GamesDataManipulate @id = :id, @type = 'FINDSTOR'"

                qry2.prepare(sql2)
                qry2.bindValue(":id", self.game_id)

                if qry2.exec_():
                    self.conn.db.commit()

                else:
                    QMessageBox.warning(None, "Database Error",
                                        qry2.lastError().text())

                for i in range(self.ui.listWidgetGameEditStorage.count()):
                    qry = QSqlQuery()
                    sql = "EXEC dbo.GamesDataManipulate @storage = :storage, @id = :id, @type = 'ADDSTOR'"
                    qry.prepare(sql)
                    # to bedzie slabe, bo sie bedzie wywalac jak slownik bedzie pusty... trzeba bedzie przetestowac na pustej bazie
                    for j in range(self.game.game["Storage"].rowCount()):
                        if self.game.game["Storage"].record(j).value(
                                "Name") == self.ui.listWidgetGameEditStorage.item(i).text():
                            qry.bindValue(":storage", self.game.game["Storage"].record(j).value("Id"))

                    qry.bindValue(":id", self.game_id)

                    if qry.exec_():
                        self.conn.db.commit()

                    else:
                        QMessageBox.warning(None, "Database Error",
                                            qry.lastError().text())

                qry2 = QSqlQuery()
                sql2 = "EXEC dbo.GamesDataManipulate @id = :id, @type = 'CLEANSTOR'"

                qry2.prepare(sql2)

                qry2.bindValue(":id", self.game_id)

                if qry2.exec_():
                    self.conn.db.commit()

                else:
                    QMessageBox.warning(None, "Database Error",
                                        qry2.lastError().text())

                # DIFFICULTIES

                """ tutaj trzeba uwzględnić także usuwanie, czyli tak --- ustalamy listę wysyłamy do """
                # TODO to na pewno bedzie trzeba przerobic, troche slabe rozwiazanie, ale to trzeba sie wiecej dowiedziec - jak przekazywać do bazy kilka wartości na raz? taką tabelkę

                qry2 = QSqlQuery()
                sql2 = "EXEC dbo.GamesDataManipulate @id = :id, @type = 'FINDDIFF'"

                qry2.prepare(sql2)
                qry2.bindValue(":id", self.game_id)

                if qry2.exec_():
                    self.conn.db.commit()

                else:
                    QMessageBox.warning(None, "Database Error",
                                        qry2.lastError().text())

                in_game_number = 0
                # TODO to poprawic, zeby przekazywalo ID, a nie name
                for i in range(self.ui.listWidgetGameEditDifficultiesComplete.count()):
                    qry = QSqlQuery()
                    sql = "EXEC dbo.GamesDataManipulate @id = :id, @name = :name, @complete = 1, @ign = :ign, @type = 'ADDDIFF'"
                    qry.prepare(sql)

                    qry.bindValue(":id", self.game_id)
                    qry.bindValue(":name", self.ui.listWidgetGameEditDifficultiesComplete.item(i).text())
                    qry.bindValue(":ign", in_game_number)

                    if qry.exec_():
                        self.conn.db.commit()

                    else:
                        QMessageBox.warning(None, "Database Error",
                                            qry.lastError().text())
                    in_game_number += 1

                for i in range(self.ui.listWidgetGameEditDifficulties.count()):
                    qry = QSqlQuery()
                    sql = "EXEC dbo.GamesDataManipulate @id = :id, @name = :name, @complete = 0, @ign = :ign, @type = 'ADDDIFF'"
                    qry.prepare(sql)

                    qry.bindValue(":id", self.game_id)
                    qry.bindValue(":name", self.ui.listWidgetGameEditDifficulties.item(i).text())
                    qry.bindValue(":ign", in_game_number)

                    if qry.exec_():
                        self.conn.db.commit()

                    else:
                        QMessageBox.warning(None, "Database Error",
                                            qry.lastError().text())

                    in_game_number += 1

                qry2 = QSqlQuery()
                sql2 = "EXEC dbo.GamesDataManipulate @id = :id, @type = 'CLEANDIFF'"

                qry2.prepare(sql2)

                qry2.bindValue(":id", self.game_id)

                if qry2.exec_():
                    self.conn.db.commit()

                else:
                    QMessageBox.warning(None, "Database Error",
                                        qry2.lastError().text())

                qry2 = QSqlQuery()
                sql2 = "EXEC dbo.GamesDataManipulate @id = :id, @text = :text, @type = 'REVIEW'"

                qry2.prepare(sql2)
                qry2.bindValue(":id", self.game_id)
                qry2.bindValue(":text", self.ui.textEditGameEditReview.toPlainText())

                if qry2.exec_():
                    self.conn.db.commit()

                else:
                    QMessageBox.warning(None, "Database Error",
                                        qry2.lastError().text())

            self.close()

        else:
            QMessageBox.warning(None, "Data Error",
                                "You forgot about parameter")
