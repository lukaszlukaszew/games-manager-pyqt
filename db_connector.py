# pylint: disable-msg=E0611
"""Database handler"""
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QMessageBox

import config


class DatabaseConnector:
    """Tool desired to maintain database connection.

    At the moment there are 4 main actions:
    - connect to the database,
    - fetch all data to models,
    - upload data to the database,
    - refresh of existing data in Data class.
    """

    def __init__(self):
        self.data_base = QSqlDatabase.addDatabase('QODBC')
        self.data_base.setDatabaseName(config.conn_string)
        self.data_base.open()

    def __del__(self):
        self.data_base.close()

    def sql_query_model_fetch(self, model, qry):
        """Fetch data until there is data to fetch."""
        if self.data_base.isOpen():
            if not qry.exec_():
                QMessageBox.warning(None, "Database Error", qry.lastError().text())

            model.setQuery(qry)

            while model.canFetchMore():
                model.fetchMore()

        return model

    def sql_upload(self, params, sql, to_bind, key):
        """Insert/update data in the database."""
        qry = QSqlQuery()
        qry.prepare(sql[key])
        for i in to_bind[key]:
            qry.bindValue(i, params[i])

        if self.data_base.isOpen():
            if qry.exec_():
                self.data_base.commit()
            else:
                QMessageBox.warning(None, "Database Error", qry.lastError().text())

        return qry.lastInsertId()

    def sql_refresh(self, sql, game_id):
        """Download data again and replace existing."""
        model = QSqlQueryModel()
        qry = QSqlQuery(self.data_base)
        qry.prepare(sql)

        if self.data_base.isOpen():
            if ":id" in sql:
                if game_id:
                    qry.bindValue(':id', game_id)
                else:
                    qry.bindValue(':id', 0)

        return self.sql_query_model_fetch(model, qry)
