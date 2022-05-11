# -----------------------------------------------------------
# @author dimakozin <dimakozin@gmail.com>
# @date 08.11.2021
# @version 1.0.0
# @about Программа записи экспериментов по изучению акустических решеток
# @tags Acoustic Array, UMA-16
#
# (C) 2021 Dmitry Kozin, Moscow, Russia
# -----------------------------------------------------------3

__author__ = "Dmitry Kozin"
__copyright__ = "Copyright 2021"
__version__ = "1.0.0"

import threading

from PyQt6 import QtWidgets
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.uic.Compiler.qtproxies import QtGui

import RecordExperimentUI

import pyaudio
import cv2
import wave
import numpy as np

FRAME_RATE = 16000
SAMPLE_FORMAT = pyaudio.paInt16


class RecordExperimentApp(QtWidgets.QMainWindow, RecordExperimentUI.Ui_MainWindow):
    def __init__(self, log=print):
        def clickButtonConnect():
            self.UpdateDevicesButton.clicked.connect(self.updateDevices)
            self.StartRecordButton.clicked.connect(self.startRecordingButtonClicked)
            self.StopRecordButton.clicked.connect(self.stopRecordingButtonClicked)
            self.WAVFileToolButton.clicked.connect(lambda: self.getExistingDirectory(fileEdit=self.WAVFileEdit))

        self.devices = []
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

        self.video_stream = VideoStreamingWorker()
        self.video_stream.ImageUpdate.connect(self.ImageUpdateSlot)
        self.video_stream.start()
        self.make_picture = False

        super().__init__()
        self.setupUi(self)
        self.log = log

        clickButtonConnect()
        self.updateDevices()

    def updateDevices(self):
        self.devices.clear()
        for i in range(self.pyaudio_instance.get_device_count()):
            device = self.pyaudio_instance.get_device_info_by_index(i)
            self.devices.append(device)
        self.MicrophoneBox.clear()
        self.MicrophoneBox.addItems("%s: %s" % (i, device["name"]) for i, device in enumerate(self.devices))

    def ImageUpdateSlot(self, Image):
        self.CamImageLabel.setPixmap(QPixmap.fromImage(Image))
        if self.make_picture:
            try:
                filename = self.WAVFileEdit.text() + "/experiment.png"
                Image.save(filename)
                self.log("Image save to %s" % filename)
            except Exception as e:
                self.log(str(e))
            self.make_picture = False

    def SoundBarUpdateSlot(self, value):
        self.SoundBar.setValue(value)

    def startRecordingButtonClicked(self):
        device_index = self.MicrophoneBox.currentIndex()
        device = self.devices[device_index]

        self.StartRecordButton.setDisabled(True)
        self.StopRecordButton.setDisabled(False)
        self.log("Recording started")
        record_audio_thread = threading.Thread(self._recording_audio_thread(device=device, device_index=device_index))
        record_audio_thread.start()

    def _recording_audio_thread(self, device, device_index):
        self.channels = device['maxInputChannels']
        self.frames_per_buffer = FRAME_RATE // self.channels

        self.log("Device id: %s" % device_index)
        self.log("Channels: %s" % self.channels)
        self.log("Chunks size: %s" % self.frames_per_buffer)

        def recording_callback(in_data, frame_count, time_info, status):
            self.frames.append(in_data)
            data = np.frombuffer(in_data, dtype=np.int16)
            chunkMax = np.amax(data)
            self.SoundBarUpdateSlot(chunkMax)
            return in_data, pyaudio.paContinue

        self.stream = self.pyaudio_instance.open(
            format=SAMPLE_FORMAT,
            channels=self.channels,
            rate=FRAME_RATE,
            frames_per_buffer=self.frames_per_buffer,
            input=True,
            input_device_index=device_index,
            stream_callback=recording_callback
        )

        self.stream.start_stream()

    def stopRecordingButtonClicked(self):
        self.StartRecordButton.setDisabled(False)
        self.StopRecordButton.setDisabled(True)

        file_name = self.WAVFileEdit.text() + "/experiment.wav"
        wf = wave.open(file_name, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.pyaudio_instance.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(FRAME_RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        for frame in self.frames:
            self._out.write(frame)

        self._out.release()

        self.frames.clear()
        self.stream.stop_stream()
        self.stream.close()

        self.saveImage()

        self.log("Recording stopped. File saved to %s" % file_name)

    def getExistingDirectory(self, fileEdit=None):
        try:
            response = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
            if response != '' and fileEdit is not None:
                fileEdit.setText(response)
        except Exception as e:
            self.log(str(e))

    def saveImage(self):
        self.make_picture = True

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.pyaudio_instance = None
        self.frames.clear()
        self.frames = []
        if self.stream:
            self.stream.close()


class VideoStreamingWorker(QThread):
    ImageUpdate = pyqtSignal(QImage)


    def run(self):
        self.ThreadActive = True
        self._videoframes = []
        Capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
        W = 1920
        Capture.set(cv2.CAP_PROP_FRAME_WIDTH, W)
        H = 1080
        Capture.set(cv2.CAP_PROP_FRAME_HEIGHT, H)

        FPS = 30
        Capture.set(cv2.CAP_PROP_FPS, FPS)

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        Capture.set(cv2.CAP_PROP_FOURCC, fourcc)
        self._out = cv2.VideoWriter("experiment.avi", fourcc, FPS, (W, H))


        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ConvertToQtFormat = QImage(Image.data, Image.shape[1], Image.shape[0], QImage.Format.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)

    def stop(self):
        self.ThreadActive = False