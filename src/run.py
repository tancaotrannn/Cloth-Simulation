import argparse
from PIL import Image
from cloth import Cloth
from render import render_points

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nx', type=int, default=30)
    ap.add_argument('--ny', type=int, default=20)
    ap.add_argument('--steps', type=int, default=300)
    ap.add_argument('--dt', type=float, default=0.016)
    ap.add_argument('--out', type=str, required=True)
    args = ap.parse_args()

    c = Cloth(args.nx, args.ny)
    frames=[]
    for _ in range(args.steps):
        c.step(args.dt)
        frames.append(Image.fromarray(render_points(c.pos)))
    frames[0].save(args.out, save_all=True, append_images=frames[1:], duration=33, loop=0)
    print('Wrote', args.out)

if __name__ == '__main__':
    main()