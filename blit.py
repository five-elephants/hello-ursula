import numpy as np
from scipy.ndimage import imread


def blit(dest, src, src_key=None, dest_key=None):
    # Do not copy pixels with src_key value
    if not src_key is None:
        sel_src = src != src_key
    else:
        sel_src = np.ones(src.shape, dtype=bool)

    # Overwrite pixels with dest_key value
    if not dest_key is None:
        sel_dest = dest == dest_key
    else:
        sel_dest = np.ones(dest.shape, dtype=bool)

    dest = np.where(np.logical_and(sel_src, sel_dest), src, dest)
    return dest


def load_png(filename):
    img = imread(filename, mode='RGB')
    rgb = np.array(img[:,:,0:3] / 255.0, dtype=np.float)
    #gamma_corrected = rgb ** gamma
    # sRGB gamma correction
    gamma_corrected = np.where(rgb <= 0.04045,
            rgb / 12.92,
            ((rgb + 0.055) / (1.0 + 0.055)) ** 2.4)

    # correct for relative luminosity
    #lum_target = 400
    #lum_red = 700
    #lum_green = 1400
    #lum_blue = 400

    #lum_corrected = np.zeros(gamma_corrected.shape)
    #lum_corrected[:,:,0] = np.clip(gamma_corrected[:,:,0] * (lum_target / lum_red), 0, 1.0)
    #lum_corrected[:,:,1] = np.clip(gamma_corrected[:,:,1] * (lum_target / lum_green), 0, 1.0)
    #lum_corrected[:,:,2] = np.clip(gamma_corrected[:,:,2] * (lum_target / lum_blue), 0, 1.0)

    #return np.array(lum_corrected * 255.0, dtype=np.uint8)

    return np.array(gamma_corrected * 255.0, dtype=np.uint8)

def load_png_xy(filename):
    img = load_png(filename)
    return np.flip(np.swapaxes(img, 0, 1), 1)
