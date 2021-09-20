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

# TODO - jak ładniej przekazywać ID do bazy? jak podpiąć modele do widgetow, zeby to spelnialo swoja funkcje?
# TODO - czy recenzje zapisywać jako XML, żeby można było wprowadzić jakieś ładne formatowanie? jak to zrobić?