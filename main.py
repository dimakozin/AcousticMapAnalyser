# -----------------------------------------------------------
# @author dimakozin <dimakozin@gmail.com>
# @date 01.11.2021
# @version 1.0.0
# @about Программа для визуализации данных, получаемых с акустической решетки
# @tags Acoustic Array, UMA-16
#
# (C) 2021 Dmitry Kozin, Moscow, Russia
# -----------------------------------------------------------

__author__ = "Dmitry Kozin"
__copyright__ = "Copyright 2021"
__version__ = "1.0.0"

from PyQt6 import QtWidgets

import sys
import os
from datetime import datetime

import AMAnalyserUI
import RecordExperiment
from AudioAnalyser import *


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AMAnalyserApp()
    window.show()
    app.exec()


class AMAnalyserApp(QtWidgets.QMainWindow, AMAnalyserUI.Ui_MainWindow):
    def __init__(self):
        def clickButtonConnect():
            self.MicrophoneFileToolButton.clicked.connect(lambda: self.getFileName(fileEdit=self.MicrophoneGeometryEdit,
                                                                                   filter='*.xml'))
            self.HDF5ToolButton.clicked.connect(lambda: self.getFileName(fileEdit=self.HDF5Edit, filter='*.h5'))
            self.WavFileToolButton.clicked.connect(lambda: self.getFileName(fileEdit=self.WavFileEdit, filter='*.wav'))
            self.ImageFileToolButton.clicked.connect(lambda: self.getFileName(
                fileEdit=self.ImageFileEdit,
                filter="*.jpg; *.bmp; *.png"
            ))
            self.RunAnalysisButton.clicked.connect(self.analysisProcess)
            self.InspectSignalButton.clicked.connect(self.inspectProcess)
            self.ConvertToH5Button.clicked.connect(self.convertToH5)
            self.RecordExperimentButton.clicked.connect(self.openRecWindow)
            self.MicrophoneCalibrationFileToolButton.clicked.connect(lambda: self.getFileName(fileEdit=self.MicrophoneCalibrationFileEdit,
                                                                                              filter='*.xml'))

        super().__init__()
        self.recordingWindow = None
        self.setupUi(self)
        self.frame_rate = 0
        self.maxChannels = 0
        self.channels = []
        self.frequencies = []

        self.ChannelSpinBox.valueChanged.connect(self.onChannelChange)
        clickButtonConnect()
        self.updateSpinBoxLimits()

    def getFileName(self, fileEdit=None, filter='*'):
        try:
            response = QtWidgets.QFileDialog.getOpenFileName(
                parent=self,
                caption='Select a data file',
                directory=os.getcwd(),
                filter=filter
            )
            if response[0] != '' and fileEdit is not None:
                fileEdit.setText(response[0])
        except Exception as e:
            self.log(str(e))

    def updateSpinBoxLimits(self):
        self.ChannelSpinBox.setMaximum(self.maxChannels)
        self.LowerFreqBox.setMaximum(self.frame_rate)
        self.HighFreqBox.setMaximum(self.frame_rate)

    def analysisProcess(self):
        try:
            distance = self.DistanceEdit.text().replace(",", ".")
            z_dist = float(distance)
            BeamformEvaluator.evaluate(
                datafile=self.HDF5Edit.text(),
                imagefile=self.ImageFileEdit.text(),
                micgeofile=self.MicrophoneGeometryEdit.text(),
                lower_freq=self.LowerFreqBox.value(),
                higher_freq=self.HighFreqBox.value(),
                z_dist=z_dist,
                threshold=self.MapThresholdBox.value(),
                calibration_file=self.MicrophoneCalibrationFileEdit.text()
            )
            self.log("Analysed")
        except Exception as e:
            self.log(str(e))

    def convertToH5(self):
        try:
            h5file = AudioConverter.convertToH5(self.WavFileEdit.text())
            self.HDF5Edit.setText(h5file)
            self.log("H5 File saved to %s" % h5file)
        except Exception as e:
            self.log(str(e))

    def inspectProcess(self):
        try:
            self.frame_rate, self.channels = ViewsPlotter.getWavFileData(self.WavFileEdit.text())
            self.frequencies = ViewsPlotter.getFrequencySpectrum(self.channels, self.frame_rate)

            self.FrequencyValueLabel.setText(str(self.frame_rate))

            self.maxChannels = len(self.channels)-1
            self.setChannel(0)
            self.updateSpinBoxLimits()
            self.onChannelChange()

            self.log("File inspected")
        except Exception as e:
            self.log(str(e))

    def onChannelChange(self):
        selected_channel = int(self.ChannelSpinBox.value())
        self.AmplitudeView.clear()
        self.AmplitudeView.plot(self.channels[selected_channel])

        self.MagnitudeView.clear()
        self.MagnitudeView.plot(self.frequencies[selected_channel][0], self.frequencies[selected_channel][1])

    def setChannel(self, value):
        self.ChannelSpinBox.setValue(value)

    def log(self, text):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        self.textBrowser.append("[%s | %s ]" % (time, text))

    def openRecWindow(self):
        if not self.recordingWindow:
            self.recordingWindow = RecordExperiment.RecordExperimentApp(log=self.log)
        self.recordingWindow.show()


if __name__ == '__main__':
    main()
