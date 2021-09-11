import config
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class DatabaseConnector:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase('QODBC')
        self.db.setDatabaseName(config.conn_string)
        self.db.open()

    def __del__(self):
        self.db.close()

    def sql_query_model_fetch(self, query_model, qry):
        if self.db.isOpen():
            qry.exec_()

            query_model.setQuery(qry)

            while query_model.canFetchMore():
                query_model.fetchMore()
        else:
            print("Database not connected")

        return query_model