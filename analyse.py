#!/usr/bin/python
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
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
io = [jup[140:180, 50:100] for jup in jupiter]

# Find maximum
maxis = [np.unravel_index(np.argmax(_io), _io.shape) for _io in io]

# plt.ioff()
# for i in range(len(maxis)):
#     plt.cla()
#     plt.imshow(io[i])
#     plt.plot(maxis[i][1], maxis[i][0], 'ro')
#     plt.show()
io_stacked = np.mean(io, axis=0)
plt.imshow(io_stacked, interpolation='none')
plt.savefig('io_stacked.pdf')
