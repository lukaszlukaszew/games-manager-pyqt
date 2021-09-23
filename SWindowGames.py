from DGameEdit import *
from ui.SubWindowGames import *


class SubWindowGames(QDialog):
    def __init__(self, conn, data):
        super().__init__()
        self.ui = Ui_Games()
        self.ui.setupUi(self)

        self.conn = conn
        self.data = data
        self.game_list = self.data.GameList(self.conn)

        self.ui.pushButtonEdit.clicked.connect(self.dialog_game_edit)
        self.ui.pushButtonAdd.clicked.connect(self.dialog_game_add)

        self.ui.tableView.setModel(self.game_list.model)

    def dialog_game_edit(self):
        index = self.ui.tableView.currentIndex()
        index = self.ui.tableView.model().index(index.row(), 0)
        dialog = DGameEdit(self.conn, self.data, self.ui.tableView.model().data(index))
        dialog.exec_()

    def dialog_game_add(self):
        dialog = DGameEdit(self.conn, self.data, None)
        dialog.exec_()
