import numpy as np

class Cloth:
    def __init__(self, nx, ny, dx=0.02, gravity=(0,-9.8,0)):
        self.nx, self.ny = nx, ny
        X, Y = np.meshgrid(np.arange(nx), np.arange(ny))
        self.pos = np.stack([X*dx, -Y*dx, np.zeros_like(X)], axis=-1).astype(np.float32)
        self.prev = self.pos.copy()
        self.acc = np.zeros_like(self.pos)
        self.gravity = np.array(gravity, np.float32)
        self.pins = [(0,0), (nx-1,0)]
        # neighbor offsets
        self._pin_pos = {(c, r): self.pos[r, c].copy() for (c, r) in self.pins}
        self.struct = [(1,0),(0,1),(-1,0),(0,-1)]
        self.shear  = [(1,1),(-1,1),(1,-1),(-1,-1)]
        self.bend   = [(2,0),(0,2),(-2,0),(0,-2)]
        self.k = 5000.0
        self._dx = dx

    def step(self, dt, substeps=10):
        sub_dt = dt / substeps
        for _ in range(substeps):
            vel     = self.pos - self.prev
            new_pos = self.pos + vel * 0.995 + self.gravity * (sub_dt * sub_dt)
            self.prev = self.pos.copy()
            self.pos  = new_pos.astype(np.float32)
            for _ in range(2):          # ← was 5, fewer iterations = looser cloth
                self._springs(self.struct, scale=0.5)   # ← was 1.00
                self._springs(self.shear,  scale=0.2)   # ← was 0.50
                self._springs(self.bend,   scale=0.05)  # ← was 0.15
                self._pin()
 
    def _springs(self, deltas, scale):
        dx = self._dx
        for (dc, dr) in deltas:
            rest = np.sqrt(dc * dc + dr * dr) * dx
            r0 = max(0, -dr);  r1 = self.ny + min(0, -dr)
            c0 = max(0, -dc);  c1 = self.nx + min(0, -dc)
            rn0 = r0 + dr;     rn1 = r1 + dr
            cn0 = c0 + dc;     cn1 = c1 + dc
            p = self.pos[r0:r1,   c0:c1]
            q = self.pos[rn0:rn1, cn0:cn1]
            diff  = q - p
            dist  = np.linalg.norm(diff, axis=-1, keepdims=True)
            dist  = np.maximum(dist, 1e-8)
            corr  = 0.5 * scale * (dist - rest) * (diff / dist)
            self.pos[r0:r1,   c0:c1]   += corr
            self.pos[rn0:rn1, cn0:cn1] -= corr
 
    def _pin(self):
        for (col, row) in self.pins:
            init = self._pin_pos[(col, row)]
            self.pos [row, col] = init
            self.prev[row, col] = init
 
    def _collide_plane(self, n, h):
        dist = np.einsum('...k,k->...', self.pos, n)
        mask = dist < h
        if mask.any():
            penetration = (h - dist)[mask]
            self.pos[mask] += penetration[:, np.newaxis] * n
            vel = self.pos[mask] - self.prev[mask]
            v_n = np.einsum('...k,k->...', vel, n)[:, np.newaxis] * n
            self.prev[mask] += v_n
 
    def _collide_sphere(self, c, r):
        c = np.asarray(c, np.float32)
        diff = self.pos - c
        dist = np.linalg.norm(diff, axis=-1)
        mask = dist < r
        if mask.any():
            unit = diff[mask] / np.maximum(dist[mask, np.newaxis], 1e-8)
            self.pos[mask] = c + unit * r
            vel = self.pos[mask] - self.prev[mask]
            v_n = np.einsum('...k,k->...', vel, unit)[:, np.newaxis] * unit
            inward = (np.einsum('...k,k->...', vel, unit) < 0)[:, np.newaxis]
            self.prev[mask] -= v_n * inward