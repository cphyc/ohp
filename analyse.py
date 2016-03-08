#!/usr/bin/python
import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt

# Open files
bg = fits.open('jupiter_08032016_0040_bg')
jupiter_raw = fits.open('jupiter_08032016_0039')

# Take the median
bg_med = np.median(bg[0].data, axis=0)

# Remove background baby
jupiter = [_data - bg_med for _data in jupiter_raw[0].data]

# 
