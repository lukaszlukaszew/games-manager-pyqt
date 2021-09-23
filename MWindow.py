from ui import MainWindow
from PyQt5.QtWidgets import QMainWindow
from SWindowGames import *


class AppGamesManager(QMainWindow):
    def __init__(self, conn, data):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()

        self.ui.actionGames.triggered.connect(self.subwindow_games)
        self.ui.actionNotes.triggered.connect(self.subwindow_notes)
        self.ui.actionTags.triggered.connect(self.subwindow_tags)
        self.ui.actionStorage.triggered.connect(self.subwindow_storage)
        self.ui.actionReviews.triggered.connect(self.subwindow_reviews)

        self.conn = conn
        self.data = data

    def subwindow_games(self):
        # TODO how to modify tableView to be editable, for example filters and sorting...
        sub_window_games = SubWindowGames(self.conn, self.data)
        self.ui.mdiArea.addSubWindow(sub_window_games)
        sub_window_games.showMaximized()

    def subwindow_notes(self):
        print("Notes editing to be implemented")

    def subwindow_tags(self):
        print("Tags editing to be implemented")

    def subwindow_reviews(self):
        print("Revievs to be implemented")

    def subwindow_storage(self):
        print("Storage editing to be implemented")
