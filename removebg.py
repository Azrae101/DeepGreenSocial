from PIL import Image
import numpy as np
from collections import deque


def remove_outer_background(input_path, output_path, threshold=220):
    img = Image.open(input_path).convert("RGBA")
    data = np.array(img)

    h, w = data.shape[:2]

    r = data[:, :, 0]
    g = data[:, :, 1]
    b = data[:, :, 2]

    # detect near-white pixels
    bg = (r > threshold) & (g > threshold) & (b > threshold)

    visited = np.zeros((h, w), dtype=bool)
    q = deque()

    # add border pixels
    for x in range(w):
        for y in [0, h-1]:
            if bg[y, x]:
                visited[y, x] = True
                q.append((y, x))

    for y in range(h):
        for x in [0, w-1]:
            if bg[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))

    # flood fill
    while q:
        y, x = q.popleft()

        for ny, nx in [(y+1,x),(y-1,x),(y,x+1),(y,x-1)]:
            if 0 <= ny < h and 0 <= nx < w:
                if not visited[ny, nx] and bg[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))

    # make only outer background transparent
    data[visited, 3] = 0

    Image.fromarray(data).save(output_path)


# example usage
remove_outer_background("images/farlig.png","images/farlig_no_bg.png")