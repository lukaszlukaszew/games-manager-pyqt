# pylint: disable-msg=E0611
"""Main file of the project - without terminal."""

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

# TODO - uzupełnić dokumentację
# TODO - uzupełnić adnotacje
# TODO - akcja DICTIONARIES

# TODO - poprawić wygląd procki do manipulacji danych

# TODO - projekt akcji refresh
# TODO - akcja refresh

# TODO - projekt akcji about
# TODO - akcja about

# TODO - projekt akcji SETTINGS
# TODO - akcja settings (rozdzielczość, motyw,

# TODO - projekt okienka TAGS
# TODO - akcja TAGS

# TODO - projekt okienka REVIEWS
# TODO - akcja REVIEWS

# TODO - projekt raportów zdefiniowanych

# TODO - how handle data models with widgets better? is there a way to implement direct passing "id" to the procedures?
# TODO - storing reviews as XML file in the database - will it allow more formatting options for the text?
# TODO - how to pass more array of values to a database, for example all difficulty levels at once? - TUPLES
