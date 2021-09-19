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
        self.ui.actionNotes.triggered.connect(self.subwindow_notes)

        self.ui.actionTags.triggered.connect(self.subwindow_tags)
        self.ui.actionStorage.triggered.connect(self.subwindow_storage)
        self.ui.actionReviews.triggered.connect(self.subwindow_reviews)
        self.ui.pushButtonGamesEdit.clicked.connect(self.dialog_game_edit)
        self.ui.pushButtonGamesAdd.clicked.connect(self.dialog_game_add)

        self.sql_games_list = "SELECT * FROM dbo.GamesMainView/* where COPIES is null or COPIES = 0 */order by Series, [Release date]"

        self.query_games_list = QSqlQueryModel()

        self.conn = conn
        self.data = data

    def subwindow_games(self):
        qry = QSqlQuery(self.conn.db)
        qry.prepare(self.sql_games_list)

        self.query_games_list = self.conn.sql_query_model_fetch(self.query_games_list, qry)

        # TODO tę listę trzeba będzie przerobić na taką, którą można ładnie filtrować i modyfikować

        self.ui.mdiArea.addSubWindow(self.ui.subwindowGames)
        self.ui.tableViewGamesList.setModel(self.query_games_list)
        self.ui.subwindowGames.showMaximized()

    def subwindow_notes(self):
        print("Notes editing to be implemented")

    def subwindow_tags(self):
        print("Tags editing to be implemented")

    def subwindow_reviews(self):
        print("Revievs to be implemented")

    def subwindow_storage(self):
        print("Storage editing to be implemented")

    def dialog_game_edit(self):
        index = self.ui.tableViewGamesList.currentIndex()
        index = self.ui.tableViewGamesList.model().index(index.row(), 0)
        dialog = DGameEdit(self.conn, self.data, self.ui.tableViewGamesList.model().data(index))
        dialog.exec_()

    def dialog_game_add(self):
        dialog = DGameEdit(self.conn, self.data, False)
        dialog.exec_()
