# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SubWindowGames.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Games(object):
    def setupUi(self, Games):
        Games.setObjectName("Games")
        Games.resize(400, 304)
        self.gridLayout = QtWidgets.QGridLayout(Games)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonEdit = QtWidgets.QPushButton(Games)
        self.pushButtonEdit.setObjectName("pushButtonEdit")
        self.gridLayout.addWidget(self.pushButtonEdit, 2, 1, 1, 1)
        self.pushButtonAdd = QtWidgets.QPushButton(Games)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout.addWidget(self.pushButtonAdd, 2, 0, 1, 1)
        self.tableView = QtWidgets.QTableView(Games)
        self.tableView.setObjectName("tableView")
        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 2)

        self.retranslateUi(Games)
        QtCore.QMetaObject.connectSlotsByName(Games)

    def retranslateUi(self, Games):
        _translate = QtCore.QCoreApplication.translate
        Games.setWindowTitle(_translate("Games", "Games"))
        self.pushButtonEdit.setText(_translate("Games", "Edit"))
        self.pushButtonAdd.setText(_translate("Games", "Add"))
