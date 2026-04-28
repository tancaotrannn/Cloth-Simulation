# CSE4303 Project 4 — Cloth Simulation (Python)

**Goal**: Implement mass–spring cloth with Verlet integration, pin constraints, and plane/sphere collisions.

## Quick Start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
python src/run.py --nx 30 --ny 20 --steps 400 --out out/cloth.gif
```

## What to Implement
- `cloth.py` → `step`, `_springs`, `_pin`, `_collide_plane`, `_collide_sphere`
- `render.py` → simple point/line rendering to frames