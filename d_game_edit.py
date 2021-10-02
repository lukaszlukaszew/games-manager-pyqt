# pylint: disable-msg=E0611
"""Main Window -> Subwindow Games -> Dialog Game Edit"""

from PyQt5.QtWidgets import QDialog, QMessageBox, QLabel, QSlider, QInputDialog, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QPixmap

from ui.DialogGameEdit import Ui_Dialog


class DGameEdit(QDialog):
    """Dialog dedicated to add new or edit existing game to the database.

    Every game can be described using these attributes:
    - id (non-editable),
    - title,
    - series (for example: Diablo, Halo etc.),
    - category (for example: remake, dlc, etc.),
    - genre (for example: fps, adventure, etc.),
    - notes (integers from 0 to 10),
    - collection (for example: Steam, Origin etc.),
    - storage (for example: HDD1, HDD2 etc.),
    - difficulty levels completed and not,
    - reviews,
    - covers (basic image handling, if you want images, you should place "id".jpg file in /images/games/ folder)
    """

    buttons = {
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

    def __init__(self, conn, data, game_id):
        super().__init__()
        self.gui = Ui_Dialog()
        self.gui.setupUi(self)

        self.params = {
            ":id": game_id,
        }

        self.graphics = {
            "scene": QGraphicsScene(self),
            "pixmap": QPixmap(),
        }

        self.graphics["image_item"] = QGraphicsPixmapItem(self.graphics["pixmap"])

        self.conn = conn
        self.game = data.Game(self.conn, self.params[":id"])

        for key, val in self.buttons.items():
            self.gui.__dict__["pushButton" + key].clicked.connect(getattr(self, val))

        self.gui.progressBarAvgNote.setFormat(str(self.gui.progressBarAvgNote.value()).format(".2f"))

        self.dictionaries()
        self.difficulties()
        self.collection()
        self.notes()

        if self.params[":id"]:
            self.basic_info()

        # TODO make dialog unmutable to check how it all will behave when more then one dialog is open

    def basic_info(self):
        """Insert basic data in the "INFO" & "REVIEW" tabs from game data: Id, Title, Release Date, Cover, Review."""
        self.gui.lineEditId.setText(str(self.params[":id"]))
        self.gui.lineEditTitle.setText(self.game.models["Data"].record(0).value("Name"))
        self.gui.dateEditRelease.setDate(
            QDate.fromString(self.game.models["Data"].record(0).value("Release_date"), "yyyy-MM-dd")
        )
        self.gui.textEditReview.setText(self.game.models["Review"].record(0).value("Review"))

        self.graphics["pixmap"].load("images/games/" + str(self.params[":id"]) + ".jpg")
        self.graphics["pixmap"] = self.graphics["pixmap"].scaled(
            self.gui.graphicsViewCover.width()-20,
            self.gui.graphicsViewCover.height()-20,
            aspectRatioMode=Qt.KeepAspectRatio
        )
        self.graphics["image_item"] = QGraphicsPixmapItem(self.graphics["pixmap"])
        self.graphics["scene"].addItem(self.graphics["image_item"])
        self.gui.graphicsViewCover.setScene(self.graphics["scene"])

    def dictionaries(self):
        """Fill in comboBoxes with the proper values."""
        com_box = ["Series", "Category", "Genre"]

        for i in com_box:
            j = -1
            for k in range(self.game.models[i].rowCount()):
                self.gui.__dict__["comboBox" + i].addItem(self.game.models[i].record(k).value("Name"))
                if self.params[":id"]:
                    if self.game.models[i].record(k).value("Id") == self.game.models["Data"].record(0).value(i + "_id"):
                        j = k

            self.gui.__dict__["comboBox" + i].setCurrentIndex(j)

        # TODO adding values to dicttionary clears current selection of all 3 comboboxes

    def notes(self):
        """Insert game notes category and notes if available in the "NOTES" tab."""
        for i in range(self.game.models["Notes"].rowCount()):
            note_category = self.game.models["Notes"].record(i).value("Name")
            note = str(self.game.models["Notes"].record(i).value("Note"))

            if self.gui.__dict__.get("label" + note_category, 0):
                self.gui.__dict__["label" + note_category].deleteLater()
                self.gui.__dict__["label" + note_category + "Note"].deleteLater()
                self.gui.__dict__["horizontalSlider" + note_category].deleteLater()

            self.gui.__dict__["label" + note_category] = QLabel(self.gui.scrollAreaWidgetContents)
            self.gui.__dict__["label" + note_category].setText(note_category)
            self.gui.__dict__["label" + note_category].setFixedHeight(40)
            self.gui.gridLayout_6.addWidget(self.gui.__dict__["label" + note_category], i, 0, 1, 1)

            self.gui.__dict__["label" + note_category + "Note"] = QLabel(self.gui.scrollAreaWidgetContents)
            self.gui.__dict__["label" + note_category + "Note"].setFixedWidth(35)
            self.gui.gridLayout_6.addWidget(self.gui.__dict__["label" + note_category + "Note"], i, 1, 1, 1)

            self.gui.__dict__["horizontalSlider" + note_category] = QSlider(self.gui.scrollAreaWidgetContents)
            self.gui.__dict__["horizontalSlider" + note_category].setMaximum(10)
            self.gui.__dict__["horizontalSlider" + note_category].setPageStep(1)
            self.gui.__dict__["horizontalSlider" + note_category].setOrientation(Qt.Horizontal)
            self.gui.gridLayout_6.addWidget(self.gui.__dict__["horizontalSlider" + note_category], i, 2, 1, 1)

            self.gui.__dict__["label" + note_category + "Note"].setText(note)
            self.gui.__dict__["horizontalSlider" + note_category].valueChanged.connect(self.avg_note)
            self.gui.__dict__["horizontalSlider" + note_category].setValue(int(note))

    def difficulties(self):
        """Insert difficulty levels divided into levels completed and incompleted in the "STATUS" tab."""
        for i in range(self.game.models["Difficulties"].rowCount()):
            if self.game.models["Difficulties"].record(i).value("Game_id"):
                if self.game.models["Difficulties"].record(i).value("Completed"):
                    self.gui.listWidgetDifficultiesComplete.addItem(
                        self.game.models["Difficulties"].record(i).value("Name")
                    )
                else:
                    self.gui.listWidgetDifficulties.addItem(
                        self.game.models["Difficulties"].record(i).value("Name")
                    )

    def collection(self):
        """Insert ovnership information in the "STATUS" tab."""
        own = ["Storage", "Collection"]
        for i in own:
            for j in range(self.game.models[i].rowCount()):
                if self.game.models[i].record(j).value("Game_id"):
                    self.gui.__dict__["listWidget"+i].addItem(self.game.models[i].record(j).value("Name"))

    def avg_note(self):
        """Set value of progress bar based on values of all notes sliders in the "NOTES" tab."""
        notes_sum = 0
        notes_count = 0

        for key, val in self.gui.__dict__.items():
            if key.startswith("horizontalSlider"):
                self.gui.__dict__["label" + key.replace("horizontalSlider", "") + "Note"].setText(str(val.value()))
                notes_sum += val.value()
                notes_count += 1

        try:
            notes_avg = notes_sum / notes_count
        except ZeroDivisionError:
            notes_avg = 0

        self.gui.progressBarAvgNote.setValue(int(notes_avg * 1000))
        self.gui.progressBarAvgNote.setFormat(str(round(notes_avg, 2)).format(".2f"))

        # TODO apparently there is something wrong with average note when starting dialog, it's bigger than it should

    def difficulty_completed(self):
        """Remove item and all items before from incomplete listWidget and put them to complete listWidget."""
        if bool(self.gui.listWidgetDifficulties.selectedItems()):
            rows = self.gui.listWidgetDifficulties.currentRow() + 1
            for _ in range(rows):
                self.gui.listWidgetDifficultiesComplete.addItem(self.gui.listWidgetDifficulties.item(0).text())
                self.gui.listWidgetDifficulties.takeItem(0)

    def difficulty_not_completed(self):
        """Remove item and all items after from complete listWidget and put them to incomplete listWidget."""
        if bool(self.gui.listWidgetDifficultiesComplete.selectedItems()):
            rows = self.gui.listWidgetDifficultiesComplete.currentRow()
            for i in range(self.gui.listWidgetDifficultiesComplete.count() - 1, rows - 1, -1):
                self.gui.listWidgetDifficulties.insertItem(0, self.gui.listWidgetDifficultiesComplete.item(i).text())
                self.gui.listWidgetDifficultiesComplete.takeItem(i)

    def add_from_dict_value(self):
        """Add unique values from proper dictionary to choosen listWidget."""
        dictionary = self.sender().objectName().replace("pushButton", "").replace("ToList", "")

        items = {
            self.gui.__dict__["listWidget" + dictionary].item(x).text() for x in range(
                self.gui.__dict__["listWidget" + dictionary].count()
            )
        }

        temp = {
            self.game.models[dictionary].record(x).value("Name") for x in range(
                self.game.models[dictionary].rowCount()
            )
        }

        if dictionary == "Difficulties":
            items_c = {
                self.gui.__dict__["listWidget" + dictionary+"Complete"].item(x).text() for x in range(
                    self.gui.__dict__["listWidget" + dictionary+"Complete"].count()
                )
            }

            temp = temp.difference(items_c)

        temp = temp.difference(items)

        if len(temp):
            value, result = QInputDialog.getItem(self, dictionary, "Please select new value:", temp, editable=False)

            if (value and result) and (value not in items):
                self.gui.__dict__["listWidget" + dictionary].addItem(value)
        else:
            QMessageBox.warning(None, "Error", "There are no more values to load")

    def remove_from_list(self):
        """Remove selected item from the listWidget."""
        dictionary = self.sender().objectName().replace("pushButton", "").replace("Delete", "")
        self.gui.__dict__["listWidget" + dictionary].takeItem(self.gui.__dict__["listWidget" + dictionary].currentRow())

    def add_dict_value(self):
        """Add value to the choosen database dictionary, refresh proper data and widgets."""
        dictionary = self.sender().objectName().replace("pushButton", "").replace("Add", "")
        value, result = QInputDialog.getText(self, dictionary, "Please input new value:")

        if value and result:
            self.params[":dictionary"] = dictionary
            self.params[":value"] = value
            if self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Dict"):
                QMessageBox.warning(None, "Confirmation", "Value added")

            self.game.data_refresh(self.conn, self.params[":id"], dictionary)

        com_box = ["Series", "Category", "Genre"]

        if dictionary in com_box:
            for i in com_box:
                self.gui.__dict__["comboBox" + i].clear()

            self.dictionaries()

        if dictionary == "Notes":
            self.notes()

    def save(self):
        """Check if saving is possible, if yes save all changes."""
        check = [self.gui.lineEditTitle.text(), self.gui.comboBoxCategory.currentText(),
                 self.gui.comboBoxGenre.currentText()]

        if all(check):
            self.save_data()
            self.save_notes()
            self.save_collection("Collection")
            self.save_collection("Storage")
            self.save_difficulties()
            self.save_review()

            QMessageBox.warning(None, "Congrats!", "Game added correctly")

            self.close()
        else:
            QMessageBox.warning(None, "Data Error", "You forgot about parameter")

    def save_data(self):
        """Save basic game data to the database."""
        self.params[":name"] = self.gui.lineEditTitle.text()
        self.params[":series"] = None
        self.params[":date"] = self.gui.dateEditRelease.text()
        self.params[":category"] = self.game.models["Category"].record(
            self.gui.comboBoxCategory.currentIndex()).value("Id")
        self.params[":genre"] = self.game.models["Genre"].record(self.gui.comboBoxGenre.currentIndex()).value("Id")

        if self.gui.comboBoxSeries.currentIndex() != -1:
            self.params[":series"] = self.game.models["Series"].record(
                self.gui.comboBoxSeries.currentIndex()).value("Id")

        if self.params[":id"]:
            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Data")
        else:
            self.params[":id"] = self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Data")

    def save_notes(self):
        """Save game notes to the database."""
        self.params[":note_id"] = None
        self.params[":note"] = None

        for i in range(self.game.models["Notes"].rowCount()):
            self.params[":note_id"] = self.game.models["Notes"].record(i).value("Id")
            self.params[":note"] = \
                self.gui.__dict__["horizontalSlider" + self.game.models["Notes"].record(i).value("Name")].value()
            self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Notes")

    def save_collection(self, dictionary):
        """Save game ownership information to the database."""
        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, dictionary + "1")

        self.params[":" + dictionary.lower()] = None

        for i in range(self.gui.listWidgetCollection.count()):
            for j in range(self.game.models[dictionary].rowCount()):
                if self.game.models[dictionary].record(j).value("Name") == \
                        self.gui.listWidgetCollection.item(i).text():
                    self.params[":" + dictionary.lower()] = self.game.models[dictionary].record(j).value("Id")
                    self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, dictionary + "2")

        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, dictionary + "3")

    def save_difficulties(self):
        """Save game difficulty levels to the database."""
        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Difficulties1")

        self.params[":diff"] = None
        self.params[":ign"] = 0

        for i in range(1, -1, -1):
            self.params[":complete"] = i
            for j in range(self.gui.__dict__["listWidgetDifficulties" + "Complete" * self.params[":complete"]].count()):
                for k in range(self.game.models["Difficulties"].rowCount()):
                    if self.game.models["Difficulties"].record(k).value("Name") == \
                            self.gui.__dict__[
                                "listWidgetDifficulties" + "Complete" * self.params[":complete"]
                            ].item(j).text():
                        self.params[":diff"] = self.game.models["Difficulties"].record(k).value("Id")
                        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Difficulties2")

                self.params[":ign"] += 1

        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Difficulties3")

    def save_review(self):
        """ Save game review to the database."""
        self.params[":text"] = self.gui.textEditReview.toPlainText()
        self.conn.sql_upload(self.params, self.game.sql_u, self.game.params, "Review")
