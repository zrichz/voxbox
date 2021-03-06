# For generating our heightmap
import math
import numpy as np

import skimage
import skimage.transform

# For saving the result
import voxbox.util
import voxbox.magicavoxel
        
# Define the size of the volume
row_count = 126
col_count = 126
plane_count = 64
frame_count = 1

# Create a NumPy array
voxels = np.zeros((frame_count, plane_count, col_count, row_count), dtype=np.uint8)

# For each voxel in the volume
for frame in range(0, frame_count):
    
    print("Generating frame {} of {}...".format(frame + 1, frame_count))
    
    a = np.random.rand(4, 4)
    heightmap = skimage.transform.resize(a, (row_count, col_count), order=3, mode='wrap')
    
    heightmap -= 0.5
    heightmap *= 0.2
    heightmap += 0.5

    for plane in range(0, plane_count):
        for col in range(0, col_count):
            for row in range(0, row_count):
                
                # Get the height from the heightmap, and
                # scale to the height of the volume
                height = heightmap[col, row]
                height *= plane_count
                
                # If the current voxel is below the
                # heightmap then set it to be solid.
                if plane <= height:
                    voxels[frame][plane][col][row] = 1
    

# Save the volume to disk as a MagicaVoxel file.
print("Saving results...")
filename = "waves.vox"
voxbox.magicavoxel.write(voxels, filename)
print("Done.")

# Open the file in the default app, which should be MagicaVoxel. Could instead
# try to run MagicaVoxel directly but then we need to know where it is.
voxbox.util.open_in_default_app(filename)
