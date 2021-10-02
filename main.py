# pylint: disable-msg=E0611
"""Main file of the project."""

import sys
from PyQt5.QtWidgets import QApplication

from m_window import AppGamesManager
from db_connector import DatabaseConnector
from db_data import Data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dbc = DatabaseConnector()
    dat = Data()
    win = AppGamesManager(conn=dbc, data=dat)

    win.show()

    sys.exit(app.exec_())
