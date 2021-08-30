# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogGameEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonGameEditSave = QtWidgets.QPushButton(Dialog)
        self.pushButtonGameEditSave.setObjectName("pushButtonGameEditSave")
        self.gridLayout.addWidget(self.pushButtonGameEditSave, 1, 1, 1, 1)
        self.pushButtonGameEditCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonGameEditCancel.setObjectName("pushButtonGameEditCancel")
        self.gridLayout.addWidget(self.pushButtonGameEditCancel, 1, 2, 1, 1)
        self.tabWidgetGameEdit = QtWidgets.QTabWidget(Dialog)
        self.tabWidgetGameEdit.setObjectName("tabWidgetGameEdit")
        self.tabGameEditInfo = QtWidgets.QWidget()
        self.tabGameEditInfo.setObjectName("tabGameEditInfo")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabGameEditInfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.tabGameEditInfo)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.lineEditGameEditId = QtWidgets.QLineEdit(self.tabGameEditInfo)
        self.lineEditGameEditId.setObjectName("lineEditGameEditId")
        self.gridLayout_2.addWidget(self.lineEditGameEditId, 0, 1, 1, 2)
        self.graphicsViewGameEditCover = QtWidgets.QGraphicsView(self.tabGameEditInfo)
        self.graphicsViewGameEditCover.setObjectName("graphicsViewGameEditCover")
        self.gridLayout_2.addWidget(self.graphicsViewGameEditCover, 0, 5, 6, 2)
        self.label_3 = QtWidgets.QLabel(self.tabGameEditInfo)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEditGameEditTitle = QtWidgets.QLineEdit(self.tabGameEditInfo)
        self.lineEditGameEditTitle.setObjectName("lineEditGameEditTitle")
        self.gridLayout_2.addWidget(self.lineEditGameEditTitle, 1, 1, 1, 4)
        self.label_2 = QtWidgets.QLabel(self.tabGameEditInfo)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.comboBoxGameEditSeries = QtWidgets.QComboBox(self.tabGameEditInfo)
        self.comboBoxGameEditSeries.setObjectName("comboBoxGameEditSeries")
        self.gridLayout_2.addWidget(self.comboBoxGameEditSeries, 2, 1, 1, 2)
        self.pushButtonGameEditSeriesAdd = QtWidgets.QPushButton(self.tabGameEditInfo)
        self.pushButtonGameEditSeriesAdd.setObjectName("pushButtonGameEditSeriesAdd")
        self.gridLayout_2.addWidget(self.pushButtonGameEditSeriesAdd, 2, 3, 1, 1)
        self.pushButtonGameEditSeriesDelete = QtWidgets.QPushButton(self.tabGameEditInfo)
        self.pushButtonGameEditSeriesDelete.setObjectName("pushButtonGameEditSeriesDelete")
        self.gridLayout_2.addWidget(self.pushButtonGameEditSeriesDelete, 2, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tabGameEditInfo)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)
        self.comboBoxGameEditType = QtWidgets.QComboBox(self.tabGameEditInfo)
        self.comboBoxGameEditType.setObjectName("comboBoxGameEditType")
        self.gridLayout_2.addWidget(self.comboBoxGameEditType, 3, 1, 1, 2)
        self.pushButtonGameEditTypeAdd = QtWidgets.QPushButton(self.tabGameEditInfo)
        self.pushButtonGameEditTypeAdd.setObjectName("pushButtonGameEditTypeAdd")
        self.gridLayout_2.addWidget(self.pushButtonGameEditTypeAdd, 3, 3, 1, 1)
        self.pushButtonGameEditTypeDelete = QtWidgets.QPushButton(self.tabGameEditInfo)
        self.pushButtonGameEditTypeDelete.setObjectName("pushButtonGameEditTypeDelete")
        self.gridLayout_2.addWidget(self.pushButtonGameEditTypeDelete, 3, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.tabGameEditInfo)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 4, 0, 1, 1)
        self.comboBoxGameEditGenre = QtWidgets.QComboBox(self.tabGameEditInfo)
        self.comboBoxGameEditGenre.setObjectName("comboBoxGameEditGenre")
        self.gridLayout_2.addWidget(self.comboBoxGameEditGenre, 4, 1, 1, 2)
        self.pushButtonGameEditGenreAdd = QtWidgets.QPushButton(self.tabGameEditInfo)
        self.pushButtonGameEditGenreAdd.setObjectName("pushButtonGameEditGenreAdd")
        self.gridLayout_2.addWidget(self.pushButtonGameEditGenreAdd, 4, 3, 1, 1)
        self.pushButtonGameEditGenreDelete = QtWidgets.QPushButton(self.tabGameEditInfo)
        self.pushButtonGameEditGenreDelete.setObjectName("pushButtonGameEditGenreDelete")
        self.gridLayout_2.addWidget(self.pushButtonGameEditGenreDelete, 4, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.tabGameEditInfo)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 2)
        self.dateEditGameEditRelease = QtWidgets.QDateEdit(self.tabGameEditInfo)
        self.dateEditGameEditRelease.setObjectName("dateEditGameEditRelease")
        self.gridLayout_2.addWidget(self.dateEditGameEditRelease, 5, 2, 1, 1)
        self.pushButtonGameEditCoverAdd = QtWidgets.QPushButton(self.tabGameEditInfo)
        self.pushButtonGameEditCoverAdd.setObjectName("pushButtonGameEditCoverAdd")
        self.gridLayout_2.addWidget(self.pushButtonGameEditCoverAdd, 6, 5, 1, 1)
        self.pushButtonGameEditCoverDelete = QtWidgets.QPushButton(self.tabGameEditInfo)
        self.pushButtonGameEditCoverDelete.setObjectName("pushButtonGameEditCoverDelete")
        self.gridLayout_2.addWidget(self.pushButtonGameEditCoverDelete, 6, 6, 1, 1)
        self.tabWidgetGameEdit.addTab(self.tabGameEditInfo, "")
        self.tabGameEditNotes = QtWidgets.QWidget()
        self.tabGameEditNotes.setObjectName("tabGameEditNotes")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabGameEditNotes)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_10 = QtWidgets.QLabel(self.tabGameEditNotes)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)
        self.horizontalSliderGameEditGraphics = QtWidgets.QSlider(self.tabGameEditNotes)
        self.horizontalSliderGameEditGraphics.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderGameEditGraphics.setObjectName("horizontalSliderGameEditGraphics")
        self.gridLayout_3.addWidget(self.horizontalSliderGameEditGraphics, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.tabGameEditNotes)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 0, 1, 1)
        self.horizontalSliderGameEditSound = QtWidgets.QSlider(self.tabGameEditNotes)
        self.horizontalSliderGameEditSound.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderGameEditSound.setObjectName("horizontalSliderGameEditSound")
        self.gridLayout_3.addWidget(self.horizontalSliderGameEditSound, 1, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.tabGameEditNotes)
        self.label_16.setObjectName("label_16")
        self.gridLayout_3.addWidget(self.label_16, 2, 0, 1, 1)
        self.horizontalSliderGameEditOptimization = QtWidgets.QSlider(self.tabGameEditNotes)
        self.horizontalSliderGameEditOptimization.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderGameEditOptimization.setObjectName("horizontalSliderGameEditOptimization")
        self.gridLayout_3.addWidget(self.horizontalSliderGameEditOptimization, 2, 1, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.tabGameEditNotes)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 3, 0, 1, 1)
        self.horizontalSliderGameEditAmbience = QtWidgets.QSlider(self.tabGameEditNotes)
        self.horizontalSliderGameEditAmbience.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderGameEditAmbience.setObjectName("horizontalSliderGameEditAmbience")
        self.gridLayout_3.addWidget(self.horizontalSliderGameEditAmbience, 3, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.tabGameEditNotes)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 4, 0, 1, 1)
        self.horizontalSliderGameEditPlayability = QtWidgets.QSlider(self.tabGameEditNotes)
        self.horizontalSliderGameEditPlayability.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderGameEditPlayability.setObjectName("horizontalSliderGameEditPlayability")
        self.gridLayout_3.addWidget(self.horizontalSliderGameEditPlayability, 4, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.tabGameEditNotes)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 5, 0, 1, 1)
        self.horizontalSliderGameEditFun = QtWidgets.QSlider(self.tabGameEditNotes)
        self.horizontalSliderGameEditFun.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderGameEditFun.setObjectName("horizontalSliderGameEditFun")
        self.gridLayout_3.addWidget(self.horizontalSliderGameEditFun, 5, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.tabGameEditNotes)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 6, 0, 1, 1)
        self.horizontalSliderGameEditStory = QtWidgets.QSlider(self.tabGameEditNotes)
        self.horizontalSliderGameEditStory.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderGameEditStory.setObjectName("horizontalSliderGameEditStory")
        self.gridLayout_3.addWidget(self.horizontalSliderGameEditStory, 6, 1, 1, 1)
        self.line = QtWidgets.QFrame(self.tabGameEditNotes)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 7, 0, 1, 2)
        self.label_14 = QtWidgets.QLabel(self.tabGameEditNotes)
        self.label_14.setObjectName("label_14")
        self.gridLayout_3.addWidget(self.label_14, 8, 0, 1, 1)
        self.progressBarGameEditAvgNote = QtWidgets.QProgressBar(self.tabGameEditNotes)
        self.progressBarGameEditAvgNote.setMaximum(10000)
        self.progressBarGameEditAvgNote.setProperty("value", 0)
        self.progressBarGameEditAvgNote.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.progressBarGameEditAvgNote.setObjectName("progressBarGameEditAvgNote")
        self.gridLayout_3.addWidget(self.progressBarGameEditAvgNote, 8, 1, 1, 1)
        self.tabWidgetGameEdit.addTab(self.tabGameEditNotes, "")
        self.tabGameEditStatus = QtWidgets.QWidget()
        self.tabGameEditStatus.setObjectName("tabGameEditStatus")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabGameEditStatus)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_7 = QtWidgets.QLabel(self.tabGameEditStatus)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)
        self.comboBoxGameEditCollection = QtWidgets.QComboBox(self.tabGameEditStatus)
        self.comboBoxGameEditCollection.setObjectName("comboBoxGameEditCollection")
        self.gridLayout_4.addWidget(self.comboBoxGameEditCollection, 0, 1, 1, 2)
        self.pushButtonGameEditCollectionAdd = QtWidgets.QPushButton(self.tabGameEditStatus)
        self.pushButtonGameEditCollectionAdd.setObjectName("pushButtonGameEditCollectionAdd")
        self.gridLayout_4.addWidget(self.pushButtonGameEditCollectionAdd, 0, 3, 1, 1)
        self.pushButtonGameEfitCollectionDelete = QtWidgets.QPushButton(self.tabGameEditStatus)
        self.pushButtonGameEfitCollectionDelete.setObjectName("pushButtonGameEfitCollectionDelete")
        self.gridLayout_4.addWidget(self.pushButtonGameEfitCollectionDelete, 0, 4, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.tabGameEditStatus)
        self.label_25.setObjectName("label_25")
        self.gridLayout_4.addWidget(self.label_25, 1, 0, 1, 1)
        self.comboBoxGameEditStorage = QtWidgets.QComboBox(self.tabGameEditStatus)
        self.comboBoxGameEditStorage.setObjectName("comboBoxGameEditStorage")
        self.gridLayout_4.addWidget(self.comboBoxGameEditStorage, 1, 1, 1, 2)
        self.pushButtonGameEditStorageAdd = QtWidgets.QPushButton(self.tabGameEditStatus)
        self.pushButtonGameEditStorageAdd.setObjectName("pushButtonGameEditStorageAdd")
        self.gridLayout_4.addWidget(self.pushButtonGameEditStorageAdd, 1, 3, 1, 1)
        self.pushButtonGameEditStorageDelete = QtWidgets.QPushButton(self.tabGameEditStatus)
        self.pushButtonGameEditStorageDelete.setObjectName("pushButtonGameEditStorageDelete")
        self.gridLayout_4.addWidget(self.pushButtonGameEditStorageDelete, 1, 4, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.tabGameEditStatus)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout_4.addWidget(self.line_2, 2, 0, 1, 7)
        self.listWidgetGameEditDifficulty = QtWidgets.QListWidget(self.tabGameEditStatus)
        self.listWidgetGameEditDifficulty.setObjectName("listWidgetGameEditDifficulty")
        self.gridLayout_4.addWidget(self.listWidgetGameEditDifficulty, 4, 0, 1, 3)
        self.pushButtonGameEditDifficultyAdd = QtWidgets.QPushButton(self.tabGameEditStatus)
        self.pushButtonGameEditDifficultyAdd.setObjectName("pushButtonGameEditDifficultyAdd")
        self.gridLayout_4.addWidget(self.pushButtonGameEditDifficultyAdd, 5, 0, 1, 1)
        self.pushButtonGameEditDifficultyDelete = QtWidgets.QPushButton(self.tabGameEditStatus)
        self.pushButtonGameEditDifficultyDelete.setObjectName("pushButtonGameEditDifficultyDelete")
        self.gridLayout_4.addWidget(self.pushButtonGameEditDifficultyDelete, 5, 1, 1, 1)
        self.pushButtonGameEditDifficultyCompleted = QtWidgets.QPushButton(self.tabGameEditStatus)
        self.pushButtonGameEditDifficultyCompleted.setObjectName("pushButtonGameEditDifficultyCompleted")
        self.gridLayout_4.addWidget(self.pushButtonGameEditDifficultyCompleted, 5, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tabGameEditStatus)
        self.label_9.setObjectName("label_9")
        self.gridLayout_4.addWidget(self.label_9, 3, 3, 1, 1)
        self.listWidgetGameEditDifficultyComplete = QtWidgets.QListWidget(self.tabGameEditStatus)
        self.listWidgetGameEditDifficultyComplete.setObjectName("listWidgetGameEditDifficultyComplete")
        self.gridLayout_4.addWidget(self.listWidgetGameEditDifficultyComplete, 4, 3, 1, 3)
        self.label_8 = QtWidgets.QLabel(self.tabGameEditStatus)
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 3, 0, 1, 1)
        self.pushButtonGameEditDifficultyNotCompleted = QtWidgets.QPushButton(self.tabGameEditStatus)
        self.pushButtonGameEditDifficultyNotCompleted.setObjectName("pushButtonGameEditDifficultyNotCompleted")
        self.gridLayout_4.addWidget(self.pushButtonGameEditDifficultyNotCompleted, 5, 4, 1, 1)
        self.tabWidgetGameEdit.addTab(self.tabGameEditStatus, "")
        self.gridLayout.addWidget(self.tabWidgetGameEdit, 0, 0, 1, 3)

        self.retranslateUi(Dialog)
        self.tabWidgetGameEdit.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Game"))
        self.pushButtonGameEditSave.setText(_translate("Dialog", "Save"))
        self.pushButtonGameEditCancel.setText(_translate("Dialog", "Cancel"))
        self.label.setText(_translate("Dialog", "Id"))
        self.label_3.setText(_translate("Dialog", "Title"))
        self.label_2.setText(_translate("Dialog", "Series"))
        self.pushButtonGameEditSeriesAdd.setText(_translate("Dialog", "+"))
        self.pushButtonGameEditSeriesDelete.setText(_translate("Dialog", "-"))
        self.label_4.setText(_translate("Dialog", "Type"))
        self.pushButtonGameEditTypeAdd.setText(_translate("Dialog", "+"))
        self.pushButtonGameEditTypeDelete.setText(_translate("Dialog", "-"))
        self.label_5.setText(_translate("Dialog", "Genre"))
        self.pushButtonGameEditGenreAdd.setText(_translate("Dialog", "+"))
        self.pushButtonGameEditGenreDelete.setText(_translate("Dialog", "-"))
        self.label_6.setText(_translate("Dialog", "Release date"))
        self.pushButtonGameEditCoverAdd.setText(_translate("Dialog", "+"))
        self.pushButtonGameEditCoverDelete.setText(_translate("Dialog", "-"))
        self.tabWidgetGameEdit.setTabText(self.tabWidgetGameEdit.indexOf(self.tabGameEditInfo), _translate("Dialog", "Info"))
        self.label_10.setText(_translate("Dialog", "Graphics"))
        self.label_11.setText(_translate("Dialog", "Sound"))
        self.label_16.setText(_translate("Dialog", "Optimization"))
        self.label_15.setText(_translate("Dialog", "Ambience"))
        self.label_12.setText(_translate("Dialog", "Playability"))
        self.label_17.setText(_translate("Dialog", "\"FUN\""))
        self.label_13.setText(_translate("Dialog", "Story"))
        self.label_14.setText(_translate("Dialog", "Average note"))
        self.tabWidgetGameEdit.setTabText(self.tabWidgetGameEdit.indexOf(self.tabGameEditNotes), _translate("Dialog", "Notes"))
        self.label_7.setText(_translate("Dialog", "Collection"))
        self.pushButtonGameEditCollectionAdd.setText(_translate("Dialog", "+"))
        self.pushButtonGameEfitCollectionDelete.setText(_translate("Dialog", "-"))
        self.label_25.setText(_translate("Dialog", "Storage"))
        self.pushButtonGameEditStorageAdd.setText(_translate("Dialog", "+"))
        self.pushButtonGameEditStorageDelete.setText(_translate("Dialog", "-"))
        self.pushButtonGameEditDifficultyAdd.setText(_translate("Dialog", "+"))
        self.pushButtonGameEditDifficultyDelete.setText(_translate("Dialog", "-"))
        self.pushButtonGameEditDifficultyCompleted.setText(_translate("Dialog", ">"))
        self.label_9.setText(_translate("Dialog", "Completed"))
        self.label_8.setText(_translate("Dialog", "Difficulties"))
        self.pushButtonGameEditDifficultyNotCompleted.setText(_translate("Dialog", "-"))
        self.tabWidgetGameEdit.setTabText(self.tabWidgetGameEdit.indexOf(self.tabGameEditStatus), _translate("Dialog", "Status"))
