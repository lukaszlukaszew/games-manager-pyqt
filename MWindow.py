# pylint: disable-msg=E0611
from PyQt5.QtWidgets import QMainWindow
from ui import MainWindow
from SWindowGames import SubWindowGames
from SWindowDicts import SubWindowDicts


class AppGamesManager(QMainWindow):
    def __init__(self, conn, data) -> None:
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()

        self.ui.actionGames.triggered.connect(self.subwindow_games)
        self.ui.actionDictionaries.triggered.connect(self.subwindow_dictionaries)

        self.ui.actionNotes.triggered.connect(self.subwindow_notes)
        self.ui.actionTags.triggered.connect(self.subwindow_tags)
        self.ui.actionReviews.triggered.connect(self.subwindow_reviews)

        self.conn = conn
        self.data = data

    def subwindow_games(self):
        # TODO how to modify tableView to be editable, for example filters and sorting...
        # TODO maybe it is reasonable to block creating another window when one is still open?
        # TODO how to adjust column width to contents
        sub_window_games = SubWindowGames(self.conn, self.data)
        self.ui.mdiArea.addSubWindow(sub_window_games)
        sub_window_games.showMaximized()

    def subwindow_dictionaries(self):
        sub_window_dictionaries = SubWindowDicts(self.conn, self.data)
        self.ui.mdiArea.addSubWindow(sub_window_dictionaries)
        sub_window_dictionaries.showMaximized()


    def subwindow_notes(self):
        pass

    def subwindow_tags(self):
        pass

    def subwindow_reviews(self):
        pass

    def subwindow_storage(self):
        pass
