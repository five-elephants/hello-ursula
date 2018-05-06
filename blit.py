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


def load_png(filename, gamma=2.2):
    img = imread(filename, mode='RGB')
    rgb = np.array(img[:,:,0:3] / 255.0, dtype=np.float)
    #gamma_corrected = rgb ** gamma
    # sRGB gamma correction
    gamma_corrected = np.where(rgb <= 0.04045,
            rgb / 12.92,
            ((rgb + 0.055) / (1.0 + 0.055)) ** 2.4)

    return np.array(gamma_corrected * 255.0, dtype=np.uint8)

