# -----------------------------------------------------------
# @author dimakozin <dimakozin@gmail.com>
# @date 02.11.2021
# @version 1.0.0
# @about Класс для построения графиков для анализа wav-файла
#
# (C) 2021 Dmitry Kozin, Moscow, Russia
# -----------------------------------------------------------

import wave
import numpy as np
from scipy import fft


def getWavFileData(filename):
    """
    Возвращает параметры сигнала
    :param filename: WAV-файл
    :return: частота записи, амплитуды во времени для каждого канала
    """
    with wave.open(filename, 'r') as wav_file:
        frame_rate = wav_file.getframerate()
        signal = wav_file.readframes(-1)
        signal = np.fromstring(signal, dtype=np.int16)

        num_channels = wav_file.getnchannels()
        channels = [signal[channel::num_channels] for channel in range(num_channels)]

        return frame_rate, channels


def getFrequencySpectrum(channels, frame_rate):
    """
    Возвращает частотный спектр
    :param channels: все каналы записи
    :param frame_rate: частота записи
    :returns частоты и их распределение
    """
    freq_data = []

    for channel in channels:
        channel = channel - np.average(channel)

        n = len(channel)
        k = np.arange(n)

        tarr = n / float(frame_rate)
        frqarr = k / float(tarr)
        frqarr = frqarr[range(n // 2)]

        channel = fft.fft(channel) / n
        channel = channel[range(n // 2)]

        freq_data.append((frqarr, abs(channel)))

    return freq_data
