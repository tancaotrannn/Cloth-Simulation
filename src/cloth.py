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
        self.struct = [(1,0),(0,1),(-1,0),(0,-1)]
        self.shear  = [(1,1),(-1,1),(1,-1),(-1,-1)]
        self.bend   = [(2,0),(0,2),(-2,0),(0,-2)]
        self.k = 5000.0

    def step(self, dt):
        """TODO: integrate one time step using Verlet; accumulate forces; enforce constraints."""
        raise NotImplementedError("step: implement me")

    # Helpers students will implement
    def _springs(self, deltas, scale):
        raise NotImplementedError("_springs: implement me")

    def _pin(self):
        raise NotImplementedError("_pin: implement me")

    def _collide_plane(self, n, h):
        raise NotImplementedError("_collide_plane: implement me")

    def _collide_sphere(self, c, r):
        raise NotImplementedError("_collide_sphere: implement me")