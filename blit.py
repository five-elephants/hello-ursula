import numpy as np
from scipy.ndimage import imread
from PIL import Image, ImageDraw, ImageFont
import screen


def blit(dest, src, src_key=None, dest_key=None):
    # Do not copy pixels with src_key value
    if not src_key is None:
        sel_src = src != src_key
        sel_src = np.reshape(np.repeat(np.logical_or.reduce(sel_src, axis=2), 3), src.shape)
    else:
        sel_src = np.ones(src.shape, dtype=bool)

    # Overwrite pixels with dest_key value
    if not dest_key is None:
        sel_dest = dest == dest_key
        sel_dest = np.logical_and.reduce(sel_dest, axis=2)
        sel_dest = np.reshape(np.repeat(np.logical_and.reduce(sel_dest, axis=2), 3), dest.shape)
    else:
        sel_dest = np.ones(dest.shape, dtype=bool)

    #print("sel_src = {}\n\nsel_dest = {}".format(sel_src, sel_dest))

    rv = np.where(np.logical_and(sel_src, sel_dest), src, dest)
    return rv


def blitxy(dest, src, dest_xy, src_rect=None, src_key=None, dest_key=None):
    # Extract source rectangle from image
    if not src_rect is None:
        x, y, w, h = src_rect
        src_part = src[x:(x+w), y:(y+h),:]
    else:
        src_part = src

    # Coordinate ranges
    x0, y0 = dest_xy
    x1 = min(dest.shape[0], x0 + src_part.shape[0])
    y1 = min(dest.shape[1], y0 + src_part.shape[1])

    # Do not copy pixels with src_key value
    if not src_key is None:
        sel_src = src_part != src_key
        sel_src = np.reshape(np.repeat(np.logical_or.reduce(sel_src, axis=2), 3), src_part.shape)
    else:
        sel_src = np.ones(src_part.shape, dtype=bool)

    # Overwrite pixels with dest_key value
    if not dest_key is None:
        sel_dest = dest == dest_key
        sel_dest = np.logical_and.reduce(sel_dest, axis=2)
        sel_dest = np.reshape(np.repeat(np.logical_and.reduce(sel_dest, axis=2), 3), dest.shape)
    else:
        sel_dest = np.ones(dest.shape, dtype=bool)

    # Copy pixels
    rv = np.copy(dest)
    if (x1 - x0 > 0) and (y1 - y0 > 0):
        rv[x0:x1, y0:y1, :] = np.where(np.logical_and(sel_src[0:(x1-x0), 0:(y1-y0)], sel_dest[x0:x1, y0:y1]),
                src_part[0:(x1-x0), 0:(y1-y0), :],
                dest[x0:x1, y0:y1, :])
    return rv


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


def text(txt, color, scroll=0.0, offset=(0,0)):
    font = ImageFont.truetype('5x5_pixel.ttf', size=7)
    img_size = font.getsize(txt)
    img_size = (img_size[0] + offset[0],
                img_size[1] + offset[1])
    #img_size = (max(screen.SCREEN_SZ_X, img_size[0]),
    #            max(screen.SCREEN_SZ_Y, img_size[1]))
    img = Image.new('RGB', img_size, (0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text(offset, txt, color, font)
    bmp = np.array(img)
    bmp = np.flip(np.swapaxes(img, 0, 1), 1)
    num_screens = (float(img_size[0]) / float(screen.SCREEN_SZ_X))
    off = int(scroll * screen.SCREEN_SZ_X)

    #return num_screens, bmp[off:off+screen.SCREEN_SZ_X,:,:]
    return num_screens, bmp
