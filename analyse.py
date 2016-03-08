#!/usr/bin/python
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
plt.ion()
# Open files
bg = fits.open('jupiter_08032016_0040_bg')
jupiter_raw = fits.open('jupiter_08032016_0039')

# Take the median
bg_med = np.median(bg[0].data, axis=0)

# Remove background baby
jupiter = [_data - bg_med for _data in jupiter_raw[0].data]

# plt.imshow(jupiter[0], interpolation='none')

# Cut around io (man)
offset = (140, 55)
io = [jup[offset[0]:offset[0]+40, offset[1]:offset[1]+40] for jup in jupiter]

# Find maximum
maxis = np.array([np.unravel_index(np.argmax(_io), _io.shape) for _io in io])
maxis_abs = maxis + np.array(offset)
minx = np.min(maxis_abs[:,0])
miny = np.min(maxis_abs[:,1])
deltax = np.max(maxis_abs[:,0]) - minx 
deltay = np.max(maxis_abs[:,1]) - miny

# plt.ioff()
# for i in range(10):#len(maxis)):
#     plt.cla()
#     plt.imshow(jupiter[i])
#     plt.plot(maxis_abs[i][1], maxis_abs[i][0], 'ro')
#     plt.show()

# Big array that contains everything
stacked = np.zeros(np.array(jupiter[0].shape) + np.array([deltax, deltay]))
width, height = jupiter[0].shape
for i in range(len(jupiter)):
    stacked[maxis_abs[i][0] - minx:maxis_abs[i][0] - minx + width,
            maxis_abs[i][1] - miny:maxis_abs[i][1] - miny + height] += jupiter[i]
