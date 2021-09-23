import sys
from PyQt5.QtWidgets import QApplication

from MWindow import *
from DatabaseConnector import *
from Data import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dbc = DatabaseConnector()
    dat = Data()
    win = AppGamesManager(conn=dbc, data=dat)

    win.show()

    sys.exit(app.exec_())

# TODO - projekt akcji refresh
# TODO - akcja refresh

# TODO - uzupełnić dokumentację

# TODO - projekt akcji about
# TODO - akcja about

# TODO - projekt akcji SETTINGS
# TODO - akcja settings (rozdzielczość, motyw,

# TODO - projekt okienka SERIES/GENRE/CATEGORY/COLLECTION/STORAGE
# TODO - akcja DICTIONARIES

# TODO - projekt okienka TAGS
# TODO - akcja TAGS

# TODO - projekt okienka REVIEWS
# TODO - akcja REVIEWS

# TODO - projekt raportów zdefiniowanych

# TODO - how handle data models with widgets better? is there a way to implement direct passing "id" to the procedures?
# TODO - storing reviews as XML file in the database - will it allow more formatting options for the text?
# TODO - how to pass more array of values to a database, for example all difficulty levels at once? - TUPLES
