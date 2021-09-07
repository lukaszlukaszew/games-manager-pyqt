import MainWindow
from PyQt5.QtWidgets import QMainWindow
from DGameEdit import *


class AppGamesManager(QMainWindow):
    def __init__(self, conn, data):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.showMaximized()

        self.ui.actionGames.triggered.connect(self.subwindow_games)
        self.ui.pushButtonGamesEdit.clicked.connect(self.dialog_game_edit)
        self.ui.pushButtonGamesAdd.clicked.connect(self.dialog_game_add)

        self.sql_games_list = 'select * from dbo.Games_View where id = 4 order by ReleaseDate'
        self.query_games_list = QSqlQueryModel()

        self.conn = conn

    def subwindow_games(self):
        self.query_games_list = self.connector.sql_query_model_fetch(self.query_games_list, self.sql_games_list)

        self.ui.mdiArea.addSubWindow(self.ui.subwindowGames)
        self.ui.tableViewGamesList.setModel(self.query_games_list)
        self.ui.subwindowGames.showMaximized()

    def dialog_game_edit(self):
        index = self.ui.tableViewGamesList.currentIndex()
        index = self.ui.tableViewGamesList.model().index(index.row(), 0)
        dialog = DGameEdit(self.connector, self.ui.tableViewGamesList.model().data(index))
        dialog.exec_()

    def dialog_game_add(self):
        dialog = DGameEdit(self.connector, None)
        dialog.exec_()

