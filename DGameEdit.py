from ui.DialogGameEdit import *
from PyQt5.QtWidgets import QDialog, QMessageBox, QLabel, QSlider, QInputDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap


class DGameEdit(QDialog):
    def __init__(self, conn, data, game_id):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.conn = conn
        self.game_id = game_id
        self.game = data.Game(self.conn, game_id)
        self.params = dict()
        self.scene = QGraphicsScene(self)
        self.pixmap = QPixmap()
        self.image_item = QGraphicsPixmapItem(self.pixmap)

        self.buttons = {
            "Save": "save",
            "Cancel": "close",
            "DifficultiesAdd": "add_dict_value",
            "DifficultiesToList": "add_from_dict_value",
            "DifficultiesDelete": "remove_from_list",
            "DifficultiesCompleted": "difficulty_completed",
            "DifficultiesNotCompleted": "difficulty_not_completed",
            "CollectionAdd": "add_dict_value",
            "CollectionToList": "add_from_dict_value",
            "CollectionDelete": "remove_from_list",
            "SeriesAdd": "add_dict_value",
            "CategoryAdd": "add_dict_value",
            "GenreAdd": "add_dict_value",
            "StorageAdd": "add_dict_value",
            "NotesAdd": "add_dict_value",
            "StorageToList": "add_from_dict_value",
            "StorageDelete": "remove_from_list",
        }

        for k, v in self.buttons.items():
            self.ui.__dict__["pushButton" + k].clicked.connect(getattr(self, v))

        self.ui.progressBarAvgNote.setFormat(str(self.ui.progressBarAvgNote.value()).format(".2f"))

        self.dictionaries()
        self.difficulties()
        self.collection()
        self.notes()

        if self.game_id:
            self.basic_info()

    def basic_info(self):
        self.ui.lineEditId.setText(str(self.game_id))
        self.ui.lineEditTitle.setText(self.game.models["Data"].record(0).value("Name"))
        self.ui.dateEditRelease.setDate(
            QDate.fromString(self.game.models["Data"].record(0).value("Release_date"), "yyyy-MM-dd")
        )
        self.ui.textEditReview.setText(self.game.models["Review"].record(0).value("Review"))

        self.pixmap.load("covers/" + str(self.game_id) + ".jpg")
        self.pixmap = self.pixmap.scaled(
            self.ui.graphicsViewCover.width()-20,
            self.ui.graphicsViewCover.height()-20,
            aspectRatioMode=Qt.KeepAspectRatio
        )
        self.image_item = QGraphicsPixmapItem(self.pixmap)
        self.scene.addItem(self.image_item)
        self.ui.graphicsViewCover.setScene(self.scene)

    def dictionaries(self):

        # TODO - jakiekolwiek dodanie do słownika usuwa niezapisany wybór, nie może tak być

        cb = ["Series", "Category", "Genre"]

        print("AAA")

        for i in cb:
            j = -1
            for k in range(self.game.models[i].rowCount()):
                self.ui.__dict__["comboBox" + i].addItem(self.game.models[i].record(k).value("Name"))
                if self.game_id:
                    if self.game.models[i].record(k).value("Id") == self.game.models["Data"].record(0).value(i + "_id"):
                        j = k

            self.ui.__dict__["comboBox" + i].setCurrentIndex(j)

    def notes(self):
        for i in range(self.game.models["Notes"].rowCount()):
            note_category = self.game.models["Notes"].record(i).value("Name")
            note = str(self.game.models["Notes"].record(i).value("Note"))

            if "label" + note_category in self.ui.__dict__.keys():
                self.ui.__dict__["label" + note_category].deleteLater()
                self.ui.__dict__["label" + note_category + "Note"].deleteLater()
                self.ui.__dict__["horizontalSlider" + note_category].deleteLater()

            self.ui.__dict__["label" + note_category] = QLabel(self.ui.scrollAreaWidgetContents)
            self.ui.__dict__["label" + note_category].setText(note_category)
            self.ui.__dict__["label" + note_category].setFixedHeight(40)
            self.ui.gridLayout_6.addWidget(self.ui.__dict__["label" + note_category], i, 0, 1, 1)

            self.ui.__dict__["label" + note_category + "Note"] = QLabel(self.ui.scrollAreaWidgetContents)
            self.ui.__dict__["label" + note_category + "Note"].setFixedWidth(35)
            self.ui.gridLayout_6.addWidget(self.ui.__dict__["label" + note_category + "Note"], i, 1, 1, 1)

            self.ui.__dict__["horizontalSlider" + note_category] = QSlider(self.ui.scrollAreaWidgetContents)
            self.ui.__dict__["horizontalSlider" + note_category].setMaximum(10)
            self.ui.__dict__["horizontalSlider" + note_category].setPageStep(1)
            self.ui.__dict__["horizontalSlider" + note_category].setOrientation(Qt.Horizontal)
            self.ui.gridLayout_6.addWidget(self.ui.__dict__["horizontalSlider" + note_category], i, 2, 1, 1)

            self.ui.__dict__["label" + note_category + "Note"].setText(note)
            self.ui.__dict__["horizontalSlider" + note_category].valueChanged.connect(self.avg_note)
            self.ui.__dict__["horizontalSlider" + note_category].setValue(int(note))

            # TODO jak rozwiązać kwestię tłumaczenia w powyższym?

    def difficulties(self):
        for i in range(self.game.models["Difficulties"].rowCount()):
            if self.game.models["Difficulties"].record(i).value("Game_id"):
                if self.game.models["Difficulties"].record(i).value("Completed"):
                    self.ui.listWidgetDifficultiesComplete.addItem(
                        self.game.models["Difficulties"].record(i).value("Name")
                    )
                else:
                    self.ui.listWidgetDifficulties.addItem(
                        self.game.models["Difficulties"].record(i).value("Name")
                    )

    def collection(self):
        cs = ["Storage", "Collection"]
        for i in cs:
            for j in range(self.game.models[i].rowCount()):
                if self.game.models[i].record(j).value("Game_id"):
                    self.ui.__dict__["listWidget"+i].addItem(self.game.models[i].record(j).value("Name"))

    def avg_note(self):
        notes_sum = 0
        notes_count = 0

        for i in self.ui.__dict__.keys():
            if i.startswith("label") and i.endswith("Note"):
                itype = i.replace("label", "").replace("Note", "")
                self.ui.__dict__[i].setText(str(self.ui.__dict__["horizontalSlider" + itype].value()))
                notes_sum += self.ui.__dict__["horizontalSlider" + itype].value()
                notes_count += 1

        try:
            notes_avg = notes_sum / notes_count
        except ZeroDivisionError:
            notes_avg = 0

        self.ui.progressBarAvgNote.setValue(int(notes_avg * 1000))
        self.ui.progressBarAvgNote.setFormat(str(round(notes_avg, 2)).format(".2f"))

    def difficulty_completed(self):
        if bool(self.ui.listWidgetDifficulties.selectedItems()):
            rows = self.ui.listWidgetDifficulties.currentRow() + 1
            for i in range(rows):
                self.ui.listWidgetDifficultiesComplete.addItem(self.ui.listWidgetDifficulties.item(0).text())
                self.ui.listWidgetDifficulties.takeItem(0)

    def difficulty_not_completed(self):
        if bool(self.ui.listWidgetDifficultiesComplete.selectedItems()):
            rows = self.ui.listWidgetDifficultiesComplete.currentRow()
            for i in range(self.ui.listWidgetDifficultiesComplete.count() - 1, rows - 1, -1):
                self.ui.listWidgetDifficulties.insertItem(0, self.ui.listWidgetDifficultiesComplete.item(i).text())
                self.ui.listWidgetDifficultiesComplete.takeItem(i)

    def add_from_dict_value(self):
        dictionary = self.sender().objectName().replace("pushButton", "").replace("ToList", "")

        items = set(
            [self.ui.__dict__["listWidget" + dictionary].item(x).text() for x in range(
                self.ui.__dict__["listWidget" + dictionary].count())]
        )

        temp = set(
            [self.game.models[dictionary].record(x).value("Name") for x in range(
                self.game.models[dictionary].rowCount())]
        )

        if dictionary == "Difficulties":
            items_c = set(
                [self.ui.__dict__["listWidget" + dictionary+"Complete"].item(x).text() for x in range(
                    self.ui.__dict__["listWidget" + dictionary+"Complete"].count())]
            )
            temp = temp.difference(items_c)

        temp = temp.difference(items)

        if len(temp):
            value, ok = QInputDialog.getItem(self, dictionary, "Please select new value:", temp, editable=False)

            if (value and ok) and (value not in items):
                self.ui.__dict__["listWidget" + dictionary].addItem(value)
        else:
            QMessageBox.warning(None, "Error", "There are no more values to load")

    def remove_from_list(self):
        dictionary = self.sender().objectName().replace("pushButton", "").replace("Delete", "")
        self.ui.__dict__["listWidget" + dictionary].takeItem(self.ui.__dict__["listWidget" + dictionary].currentRow())

    def add_dict_value(self):
        dictionary = self.sender().objectName().replace("pushButton", "").replace("Add", "")
        value, ok = QInputDialog.getText(self, dictionary, "Please input new value:")

        if value and ok:
            self.params[":dictionary"] = dictionary
            self.params[":value"] = value
            if self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Dict"):
                QMessageBox.warning(None, "Confirmation", "Value added")

            self.game.data_refresh(self.conn, self.game_id, dictionary)

        cb = ["Series", "Category", "Genre"]

        if dictionary in cb:
            for i in cb:
                self.ui.__dict__["comboBox" + i].clear()

            self.dictionaries()

        if dictionary == "Notes":
            self.notes()

    def save(self):
        check = [self.ui.lineEditTitle.text(), self.ui.comboBoxCategory.currentText(),
                 self.ui.comboBoxGenre.currentText()]

        if all(check):
            # DATA
            self.params[":id"] = self.game_id
            self.params[":name"] = self.ui.lineEditTitle.text()
            self.params[":series"] = None
            self.params[":date"] = self.ui.dateEditRelease.text()
            self.params[":category"] = self.game.models["Category"].record(
                self.ui.comboBoxCategory.currentIndex()).value("Id")
            self.params[":genre"] = self.game.models["Genre"].record(self.ui.comboBoxGenre.currentIndex()).value("Id")

            if self.ui.comboBoxSeries.currentIndex() != -1:
                self.params[":series"] = self.game.models["Series"].record(
                    self.ui.comboBoxSeries.currentIndex()).value("Id")

            if self.game_id:
                self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Data")
            else:
                self.params[":id"] = self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Data")

            # NOTES
            self.params[":note_id"] = None
            self.params["note"] = None

            for i in range(self.game.models["Notes"].rowCount()):
                self.params[":note_id"] = self.game.models["Notes"].record(i).value("Id")
                self.params[":note"] = \
                    self.ui.__dict__["horizontalSlider" + self.game.models["Notes"].record(i).value("Name")].value()
                self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Notes")

            # COLLECTION
            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Collection1")

            self.params[":collection"] = None

            for i in range(self.ui.listWidgetCollection.count()):
                for j in range(self.game.models["Collection"].rowCount()):
                    if self.game.models["Collection"].record(j).value("Name") ==\
                            self.ui.listWidgetCollection.item(i).text():
                        self.params[":collection"] = self.game.models["Collection"].record(j).value("Id")
                        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Collection2")

            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Collection3")

            # STORAGE
            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Storage1")

            self.params[":storage"] = None

            for i in range(self.ui.listWidgetStorage.count()):
                for j in range(self.game.models["Storage"].rowCount()):
                    if self.game.models["Storage"].record(j).value("Name") ==\
                            self.ui.listWidgetStorage.item(i).text():
                        self.params[":storage"] = self.game.models["Storage"].record(j).value("Id")
                        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Storage2")

            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Storage3")

            # DIFFICULTIES
            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Difficulties1")

            self.params[":diff"] = None
            self.params[":ign"] = 0
            self.params[":complete"] = 1

            for i in range(self.ui.listWidgetDifficultiesComplete.count()):
                for j in range(self.game.models["Difficulties"].rowCount()):
                    if self.game.models["Difficulties"].record(j).value("Name") ==\
                            self.ui.listWidgetDifficultiesComplete.item(i).text():
                        self.params[":diff"] = self.game.models["Difficulties"].record(j).value("Id")
                        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Difficulties2")

                self.params[":ign"] += 1

            self.params[":complete"] = 0

            for i in range(self.ui.listWidgetDifficulties.count()):
                for j in range(self.game.models["Difficulties"].rowCount()):
                    if self.game.models["Difficulties"].record(j).value("Name") ==\
                            self.ui.listWidgetDifficulties.item(i).text():
                        self.params[":diff"] = self.game.models["Difficulties"].record(j).value("Id")
                        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Difficulties2")

                self.params[":ign"] += 1

            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Difficulties3")

            # REVIEW
            self.params[":text"] = self.ui.textEditReview.toPlainText()
            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Review")

            QMessageBox.warning(None, "Congrats!", "Game added correctly")
            self.close()
        else:
            QMessageBox.warning(None, "Data Error", "You forgot about parameter")
