# pylint: disable-msg=E0611
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QMessageBox

import config


class DatabaseConnector:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase('QODBC')
        self.db.setDatabaseName(config.conn_string)
        self.db.open()

    def __del__(self):
        self.db.close()

    def sql_query_model_fetch(self, model, qry):
        if self.db.isOpen():
            if not qry.exec_():
                QMessageBox.warning(None, "Database Error", qry.lastError().text())

            model.setQuery(qry)

            while model.canFetchMore():
                model.fetchMore()

            return model
        else:
            print("Database not connected")

    def sql_upload(self, params, sql, to_bind, key):
        if self.db.isOpen():
            qry = QSqlQuery()
            qry.prepare(sql[key])

            for i in to_bind[key]:
                qry.bindValue(i, params[i])

        #    print(qry.boundValues())

            if qry.exec_():
                self.db.commit()
                return qry.lastInsertId()
            else:
                QMessageBox.warning(None, "Database Error", qry.lastError().text())

    def sql_refresh(self, sql, game_id):
        model = QSqlQueryModel()
        if self.db.isOpen():
            qry = QSqlQuery(self.db)
            qry.prepare(sql)

            if ":id" in sql:
                if game_id:
                    qry.bindValue(':id', game_id)
                else:
                    qry.bindValue(':id', 0)

            model = self.sql_query_model_fetch(model, qry)
            return model