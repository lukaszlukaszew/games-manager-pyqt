# pylint: disable-msg=E0611
"""Main Window -> Subwindow Games"""

from PyQt5.QtWidgets import QDialog
from d_game_edit import DGameEdit
from ui.SubWindowGames import Ui_Games


class SubWindowGames(QDialog):
    """SubWindow containing list of all games in the database.

     At the moment list is ordered by id of the game. From this subwindow you could add new game to the database or edit
     existing.
     """

    def __init__(self, conn, data):
        super().__init__()
        self.gui = Ui_Games()
        self.gui.setupUi(self)

        self.conn = conn
        self.data = data
        self.game_list = self.data.GameList(self.conn)

        self.gui.pushButtonEdit.clicked.connect(self.dialog_game_edit)
        self.gui.pushButtonAdd.clicked.connect(self.dialog_game_add)

        self.gui.tableView.setModel(self.game_list.model)

    def dialog_game_edit(self):
        """Extract game id for current selection then run games edition window."""
        index = self.gui.tableView.currentIndex()
        index = self.gui.tableView.model().index(index.row(), 0)
        dialog = DGameEdit(self.conn, self.data, self.gui.tableView.model().data(index))
        dialog.exec_()

    def dialog_game_add(self):
        """Run games addition version of games edition window."""
        dialog = DGameEdit(self.conn, self.data, None)
        dialog.exec_()
