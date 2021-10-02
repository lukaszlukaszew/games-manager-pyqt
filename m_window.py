# pylint: disable-msg=E0611
"""Main Window"""
from PyQt5.QtWidgets import QMainWindow
from ui import MainWindow  # type: ignore
from s_window_games import SubWindowGames
from s_window_dicts import SubWindowDicts


class AppGamesManager(QMainWindow):
    """Main window of the app with mdiArea and Menu Bar.

    At the moment you could use actions from Menu Bar:
    - Edit - > Games
    """

    actions = [
        "Games",
        "Dictionaries",
        "Notes",
        "Tags",
        "Reviews",
    ]  # type: ignore

    def __init__(self, conn, data):
        super().__init__()
        self.gui = MainWindow.Ui_MainWindow()
        self.gui.setupUi(self)
        self.showMaximized()

        for val in self.actions:
            self.gui.__dict__["action" + val].triggered.connect(
                getattr(self, "subwindow_" + val.lower())
            )

        self.conn = conn
        self.data = data

    def subwindow_games(self):
        """Add Subwindow Games to mdiArea."""
        # TODO how to modify tableView to be editable, for example filters and sorting...
        # TODO maybe it is reasonable to block creating another window when one is still open?
        # TODO how to adjust column width to contents
        sub_window_games = SubWindowGames(self.conn, self.data)
        self.gui.mdiArea.addSubWindow(sub_window_games)
        sub_window_games.showMaximized()

    def subwindow_dictionaries(self):
        """Add Subwindow Dictionaries to mdiArea."""
        sub_window_dictionaries = SubWindowDicts(self.conn, self.data)
        self.gui.mdiArea.addSubWindow(sub_window_dictionaries)
        sub_window_dictionaries.showMaximized()

    def subwindow_notes(self):
        """In progress"""

    def subwindow_tags(self):
        """In progress"""

    def subwindow_reviews(self):
        """In progress"""

    def subwindow_storage(self):
        """In progress"""
