"""run_extra.py — renderiza os ext_*.py e gera folhas de conferência."""
import glob, os, runpy, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
only = sys.argv[1:]; done = []
for p in sorted(glob.glob(os.path.join(HERE, 'ext_*.py'))):
    n = os.path.basename(p)[4:-3]
    if only and not any(n.startswith(o) for o in only):
        continue
    runpy.run_path(p, run_name='__main__'); done.append(n)
for k in range(0, len(done), 6):
    ims = [Image.open(os.path.join(HERE, '..', 'png', n + '.png')) for n in done[k:k+6]]
    w = 760; ims = [i.resize((w, int(i.height * w / i.width))) for i in ims]
    h = max(i.height for i in ims)
    sh = Image.new('RGBA', (w * 2 + 10, (h + 10) * 3), 'white')
    for j, im in enumerate(ims):
        sh.alpha_composite(im, ((j % 2) * (w + 10), (j // 2) * (h + 10)))
    sh.save(os.path.join(HERE, '..', f'ext_sheet_{k//6+1}.png'))
print(len(done), 'figuras extras')
