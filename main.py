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

# TODO - reformat nr III

# TODO - projekt akcji refresh
# TODO - akcja refresh

# TODO - projekt akcji about
# TODO - akcja about

# TODO - projekt akcji SETTINGS
# TODO - akcja settings (rozdzielczość, motyw,

# TODO - projekt okienka NOTES
# TODO - akcja NOTES

# TODO - projekt okienka DICTS
# TODO - akcja DICTS

# TODO - projekt okienka TAGS
# TODO - akcja TAGS

# TODO - projekt okienka REVIEWS
# TODO - akcja REVIEWS

# TODO - projekt okienka STORAGE
# TODO - akcja STORAGE

# TODO - projekt okienka COLLECTION
# TODO - akcja COLLECTION

# TODO - projekt raportów zdefiniowanych

# TODO - how handle data models with widgets better? is there a way to implement direct passing "id" to the procedures?
# TODO - storing reviews as XML file in the database - will it allow more formatting options for the text?
# TODO - how to pass more array of values to a database, for example all difficulty levels at once?