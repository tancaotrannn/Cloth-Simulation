import numpy as np
from PIL import Image, ImageDraw

W, H       = 512, 512
BG_COLOR   = (15, 15, 20)          # near-black background
LINE_COLOR = (80, 160, 255)        # cool blue structural lines
SHEAR_COLOR= (40, 100, 180)        # slightly dimmer for diagonals
NODE_COLOR = (200, 230, 255)       # bright nodes
NODE_R     = 2                     # node dot radius (px)
MARGIN     = 30                    # px padding on each side
 
 
def _project(pos, W=W, H=H, margin=MARGIN):
    """
    Map 3-D cloth positions → 2-D pixel coordinates.
    Uses (x, y) world axes; z is ignored for a frontal view.
    Returns (px, py) integer arrays of shape (ny, nx).
    """
    x = pos[..., 0]
    y = pos[..., 1]
 
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
 
    span = max(x_max - x_min, y_max - y_min, 1e-6)
    view_w = W - 2 * margin
    view_h = H - 2 * margin
 
    scale = min(view_w, view_h) / span
 
    px = ((x - x_min) * scale + margin).astype(int)
    py = ((y_max - y) * scale + margin).astype(int)   # flip y so +y = up
 
    px = np.clip(px, 0, W - 1)
    py = np.clip(py, 0, H - 1)
    return px, py
 
 
def render_cloth(pos, W=W, H=H):
    """
    Full cloth render: background + structural grid lines + nodes.
 
    Parameters
    ----------
    pos : np.ndarray  shape (ny, nx, 3)
    W, H : output image dimensions in pixels
 
    Returns
    -------
    np.ndarray  shape (H, W, 3)  uint8
    """
    img  = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
 
    ny, nx = pos.shape[:2]
    px, py = _project(pos, W, H)
 
    # ── horizontal structural lines (rows) ───────────────────────────────────
    for r in range(ny):
        for c in range(nx - 1):
            p0 = (px[r, c],   py[r, c])
            p1 = (px[r, c+1], py[r, c+1])
            draw.line([p0, p1], fill=LINE_COLOR, width=1)
 
    # ── vertical structural lines (columns) ──────────────────────────────────
    for c in range(nx):
        for r in range(ny - 1):
            p0 = (px[r,   c], py[r,   c])
            p1 = (px[r+1, c], py[r+1, c])
            draw.line([p0, p1], fill=LINE_COLOR, width=1)
 
    # ── nodes ────────────────────────────────────────────────────────────────
    for r in range(ny):
        for c in range(nx):
            cx, cy = int(px[r, c]), int(py[r, c])
            draw.ellipse(
                [cx - NODE_R, cy - NODE_R, cx + NODE_R, cy + NODE_R],
                fill=NODE_COLOR,
            )
 
    return np.array(img, dtype=np.uint8)
 
 
# ── Backwards-compatible alias used by the original run.py ───────────────────
def render_points(pos, W=W, H=H):
    """Alias so run.py works without modification."""
    return render_cloth(pos, W, H)