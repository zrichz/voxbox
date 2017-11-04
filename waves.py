import numpy as np
import scipy as sp

import voxbox.magicavoxel

def waves(freq, height):
    x,y = np.mgrid[0:row_count, 0:col_count]
    dist = np.hypot(x * freq, y * freq)
    #result = np.sin(dist) / np.sqrt(dist)
    result = sp.special.j0(dist)
    result += 0.4
    result *= (height / 1.4)
    return result

row_count = 126
col_count = 126
slice_count = 64

# See https://goo.gl/AP753K
# See https://goo.gl/W15gma
# See https://goo.gl/AXRypy
#x,y = np.mgrid[0:row_count, 0:col_count]
#height=np.sinc(np.hypot(x / row_count,y / col_count))
#height *= 39

height = waves(0.4, slice_count)

voxels = np.zeros((slice_count, col_count, row_count), dtype=np.uint8)
voxels[0x00][0x1a][0x0a] = 0x4f
 
for slice in range(0, slice_count):
    for col in range(0, col_count):
        for row in range(0, row_count):
            if slice < height[col][row]:
                voxels[slice][col][row] = 0x4f
    
    
result = voxbox.magicavoxel.write(voxels)

filename = "waves.vox"
file = open(filename, "wb")
file.write(result)
file.close()

# Open the file in the default application
# From: https://stackoverflow.com/a/434612/2337254
import subprocess, os, sys
if sys.platform.startswith('darwin'):
    subprocess.call(('open', filename))
elif os.name == 'nt':
    os.startfile(filename)
elif os.name == 'posix':
    subprocess.call(('xdg-open', filename))