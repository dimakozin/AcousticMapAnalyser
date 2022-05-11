# -----------------------------------------------------------
# @author dimakozin <dimakozin@gmail.com>
# @date 01.11.2021
# @version 1.0.0
# @about Класс для определения звукового давления
#
# (C) 2021 Dmitry Kozin, Moscow, Russia
# -----------------------------------------------------------

import acoular
from PIL import Image
from matplotlib import pyplot as plt
from pylab import colorbar
import numpy as np
import os.path


def evaluate(datafile, imagefile, micgeofile, lower_freq, higher_freq, z_dist, threshold, calibration_file):
    ts = acoular.TimeSamples(name=datafile)

    if os.path.isfile(calibration_file):
        ts.calib = acoular.Calib(from_file=calibration_file)

    invalid = []
    # ts.invalid_channels = invalid

    ps = acoular.PowerSpectra(time_data=ts, block_size=1024, window='Hanning')

    im = Image.open(imagefile)
    width, height = im.size  # Get dimensions
    new_width = width
    new_height = height
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    im = im.crop((left, top, right, bottom))
    px2cm = 3780.2717
    dims = [new_width / px2cm, new_height / px2cm]

    rg = acoular.RectGrid(x_min=-dims[0], x_max=dims[0], y_min=-dims[1], y_max=dims[1], z=z_dist,
                          increment=0.01)

    mg = acoular.MicGeom(from_file=micgeofile)
    # mg.invalid_channels = invalid

    env = acoular.Environment(c=346.64)
    st = acoular.SteeringVector(grid=rg, mics=mg, env=env)  # sound propagation model

    bb = acoular.BeamformerBase(freq_data=ps, steer=st)
    pm = bb.synthetic(lower_freq, higher_freq)

    Lm = acoular.L_p(pm)  # convert to decibels

    plt.imshow(im, extent=rg.extend())
    plt.xlabel('[m]')
    plt.ylabel('[m]', rotation=0)
    plt.grid(True, alpha=0.2)

    maxSPL = Lm.max()
    minSPL = Lm.min()

    minMapValue = maxSPL - threshold

    plt.imshow(Lm.T, origin='lower', vmin=minMapValue, vmax=maxSPL, extent=rg.extend(),
           interpolation='bicubic', alpha=0.5, cmap='nipy_spectral')

    colorbarTicks = np.linspace(minMapValue, maxSPL, 6, endpoint=True)
    cbar = colorbar(ticks=colorbarTicks)
    cbar.solids.set_edgecolor("face")
    cbar.ax.set_ylabel('SPL [db]', rotation=0)

    plt.title('Frequency range: {lf} - {hf} Hz\n\nDistance: {z} m'.format(lf=lower_freq, hf=higher_freq,
                                                                      z=z_dist))
    plt.tight_layout()

    plt.show()
