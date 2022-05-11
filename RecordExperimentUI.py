# Form implementation generated from reading ui file '.\RecordExperimentUI.ui'
#
# Created by: PyQt6 UI code generator 6.2.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(440, 472)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.SoundBar = QtWidgets.QProgressBar(self.centralwidget)
        self.SoundBar.setGeometry(QtCore.QRect(10, 300, 456, 23))
        self.SoundBar.setMaximum(255)
        self.SoundBar.setProperty("value", 0)
        self.SoundBar.setFormat("")
        self.SoundBar.setObjectName("SoundBar")
        self.MicrophoneBox = QtWidgets.QComboBox(self.centralwidget)
        self.MicrophoneBox.setGeometry(QtCore.QRect(70, 360, 361, 22))
        self.MicrophoneBox.setObjectName("MicrophoneBox")
        self.CameraLabel = QtWidgets.QLabel(self.centralwidget)
        self.CameraLabel.setGeometry(QtCore.QRect(10, 334, 47, 13))
        self.CameraLabel.setObjectName("CameraLabel")
        self.MicrophoneLabel = QtWidgets.QLabel(self.centralwidget)
        self.MicrophoneLabel.setGeometry(QtCore.QRect(10, 360, 61, 16))
        self.MicrophoneLabel.setObjectName("MicrophoneLabel")
        self.StartRecordButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartRecordButton.setGeometry(QtCore.QRect(130, 420, 111, 41))
        self.StartRecordButton.setObjectName("StartRecordButton")
        self.UpdateDevicesButton = QtWidgets.QPushButton(self.centralwidget)
        self.UpdateDevicesButton.setGeometry(QtCore.QRect(10, 420, 111, 41))
        self.UpdateDevicesButton.setObjectName("UpdateDevicesButton")
        self.DefaultCamLabel = QtWidgets.QLabel(self.centralwidget)
        self.DefaultCamLabel.setGeometry(QtCore.QRect(71, 335, 47, 13))
        self.DefaultCamLabel.setObjectName("DefaultCamLabel")
        self.StopRecordButton = QtWidgets.QPushButton(self.centralwidget)
        self.StopRecordButton.setGeometry(QtCore.QRect(250, 420, 111, 41))
        self.StopRecordButton.setObjectName("StopRecordButton")
        self.WAVFileEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.WAVFileEdit.setGeometry(QtCore.QRect(70, 390, 331, 20))
        self.WAVFileEdit.setObjectName("WAVFileEdit")
        self.WAVFileToolButton = QtWidgets.QToolButton(self.centralwidget)
        self.WAVFileToolButton.setGeometry(QtCore.QRect(410, 389, 25, 22))
        self.WAVFileToolButton.setObjectName("WAVFileToolButton")
        self.WAVFileLabel = QtWidgets.QLabel(self.centralwidget)
        self.WAVFileLabel.setGeometry(QtCore.QRect(10, 390, 61, 16))
        self.WAVFileLabel.setObjectName("WAVFileLabel")
        self.CamImageLabel = QtWidgets.QLabel(self.centralwidget)
        self.CamImageLabel.setGeometry(QtCore.QRect(10, 10, 421, 281))
        self.CamImageLabel.setObjectName("CamImageLabel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Record Experiment"))
        self.CameraLabel.setText(_translate("MainWindow", "Camera"))
        self.MicrophoneLabel.setText(_translate("MainWindow", "Mic:"))
        self.StartRecordButton.setText(_translate("MainWindow", "Record"))
        self.UpdateDevicesButton.setText(_translate("MainWindow", "Update Devices"))
        self.DefaultCamLabel.setText(_translate("MainWindow", "Default "))
        self.StopRecordButton.setText(_translate("MainWindow", "Stop"))
        self.WAVFileToolButton.setText(_translate("MainWindow", "..."))
        self.WAVFileLabel.setText(_translate("MainWindow", "Save to:"))
        self.CamImageLabel.setText(_translate("MainWindow", "Waiting for image..."))