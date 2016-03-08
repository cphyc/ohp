#!/usr/bin/python
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting


def optimize_max_dummy(image, x_guess, y_guess):
    return x_guess, y_guess

def optimize_max_barycentre(image, x_guess, y_guess):
    r = 10
    x_bar = 0
    y_bar = 0
    tot = 0
    for i in range(-r, +r):
        for j in range(-r, +r):
            if i**2 + j**2 > r**2:
                break

            x_bar += image[x_guess+i,y_guess+j]*i
            y_bar += image[x_guess+i,y_guess+j]*j
            tot += image[x_guess+i,y_guess+j]
    x_bar /= tot
    y_bar /= tot

    return (int(x_bar + x_guess), int(y_bar + y_guess))

# Parameters
# offset = (140, 55)
# bg_file = 'jupiter_08032016_0040_bg'
# fg_file = 'jupiter_08032016_0039'

offset = (140, 60)
bg_file = 'jupiter_08032016_0046_bg'
fg_file = 'jupiter_08032016_0045'

threshold = 0.85 # no idea why

# Open files
print('Reading files...')
bg = fits.open(bg_file)
jupiter_raw = fits.open(fg_file)

# Take the median
bg_med = np.median(bg[0].data, axis=0)

# Remove background baby
jupiter = [_data - bg_med for _data in jupiter_raw[0].data]

# plt.imshow(jupiter[0], interpolation='none')

# Cut around io (man)
io = [jup[offset[0]:offset[0]+40, offset[1]:offset[1]+40] for jup in jupiter]

print('Locating speckles...')
# Find maximum
# argmax returns a single index, unravel converts it into x,y
maxis_dummy = [np.unravel_index(np.argmax(_io), _io.shape) for _io in io]
# try to optimize the maximum
maxis = np.array([optimize_max_dummy(io[i], maxis_dummy[i][0], maxis_dummy[i][1])
                  for i in range(len(io))])
maxs = [np.max(_io) for _io in io]
# convert maximum into absolute positions
maxis_abs = maxis + np.array(offset)
minx = np.min(maxis_abs[:,0])
miny = np.min(maxis_abs[:,1])
deltax = np.max(maxis_abs[:,0]) - minx 
deltay = np.max(maxis_abs[:,1]) - miny

# Big array that contains everything
cube = [np.zeros(np.array(jupiter[0].shape))
        for i in range(len(jupiter))]
width, height = jupiter[0].shape
for i in range(len(jupiter)):
    rolled_x = np.roll(jupiter[i], -(maxis_abs[i][0] - minx), axis=0)
    cube[i] = np.roll(rolled_x,  -(maxis_abs[i][1] - miny), axis=1)

# Darwin's time
print('Keeping most luminous speckles...')
stacked = np.zeros(jupiter[0].shape)
percentile = np.percentile(maxs, 100*threshold)
for i in range(len(cube)):
    if maxs[i] > percentile :
        stacked += cube[i]

plt.imshow(stacked, interpolation='none', cmap="gray")
plt.show()
