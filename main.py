import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import QSortFilterProxyModel

import MainWindow, DialogGameEdit
import config


class AppGamesManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.showMaximized()

        self.ui.actionGames.triggered.connect(self.subwindow_games)
        self.ui.pushButtonGamesEdit.clicked.connect(self.dialog_game_edit)



    def subwindow_games(self):

        self.querymodel = QSqlQueryModel()
        db = QSqlDatabase.addDatabase('QODBC')
        db.setDatabaseName(config.conn_string)

        if db.open():
            SQL_STATEMENT = 'select * from dbo.Games'

            qry = QSqlQuery(db)
            qry.prepare(SQL_STATEMENT)
            qry.exec()

            self.querymodel.setQuery(qry)

            while self.querymodel.canFetchMore():
                self.querymodel.fetchMore()

        self.proxymodel = QSortFilterProxyModel()
        self.proxymodel.setSourceModel(self.querymodel)
        self.ui.mdiArea.addSubWindow(self.ui.subwindowGames)
        self.ui.tableViewGamesList.setModel(self.proxymodel)
        self.ui.subwindowGames.showMaximized()
        #self.ui.subwindow.show()

    def dialog_game_edit(self):
        index = self.ui.tableViewGamesList.currentIndex()
        print(self.proxymodel.data(index))
        print(self.proxymodel.index(index.row(), index.column()))
        _dialog = DGameEdit(self.proxymodel.data(index))
        _dialog.exec_()


class DGameEdit(QDialog):
    def __init__(self, value):
        super().__init__()
        self.ui = DialogGameEdit.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.lineEditGameEditId.setText(str(value))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppGamesManager()
    win.show()
    sys.exit(app.exec_())


