# -----------------------------------------------------------
# @author dimakozin <dimakozin@gmail.com>
# @date 02.11.2021
# @version 1.0.0
# @about Набор функций для конвертирования аудио-файлов
#
# (C) 2021 Dmitry Kozin, Moscow, Russia
# -----------------------------------------------------------

from scipy.io import wavfile
import tables
import numpy as np
import os


def convertToH5(filename):
    fs, data = wavfile.read(filename)

    new_file = os.path.splitext(filename)[0] + '.h5'

    float64_data = np.ascontiguousarray(data, dtype=np.float64)
    h5file = tables.open_file(new_file, mode='w', title='samples.h5')
    h5file.create_earray('/', 'time_data', atom=None, title='', obj=float64_data)

    h5file.set_node_attr('/time_data', 'sample_freq', fs)
    h5file.set_node_attr('/time_data', 'sample_time', 10.0)
    h5file.set_node_attr('/time_data', 'z_distance', 0.5)

    h5file.close()

    return new_file
