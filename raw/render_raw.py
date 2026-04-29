import numpy as np
from PIL import Image

def render_points(P, W=256, H=256):
    x = P[...,0]; y = P[...,1]
    img = np.ones((H,W,3), np.uint8)*255
    xs = ((x - x.min())/(x.max()-x.min()+1e-8)*(W-1)).astype(int)
    ys = ((y - y.min())/(y.max()-y.min()+1e-8)*(H-1)).astype(int)
    img[ys, xs] = (0,0,0)
    return img