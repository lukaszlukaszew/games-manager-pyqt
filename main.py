import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

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


# TODO - storage po stronie bazy
# TODO - filtrowanie listy storage, gdy jest focus na collection odpowiednim
# TODO - zapisywanie i edycja bazy
# TODO - wywalenie % z progressBara
# TODO - reformat nr II
# TODO - dodawanie nowej gry
# TODO - dodawanie serii
# TODO - dodawanie typu
# TODO - dodawanie gatunku
# TODO - dodawanie kolekcji
# TODO - dodawanie storage
# TODO - dodawanie poziomu trudności (zabezpieczneie, żeby nie dodawać tego samego)
# TODO - dodawanie okładki
# TODO - reformat nr III
# TODO - zakładka recenzji
# TODO - oprzeć się na procedurach w bazie


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