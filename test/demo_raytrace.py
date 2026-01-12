import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

from raytrace.raytracers import raytrace

# setup volume. This is the shape of the 3D grid through which muons will be traced
# The vol variable is used simply for the 3D grid dimensions. There's no density values here like the original repository had
vol = np.ones((5, 11, 11))

# create 3D source-destination pairs
sources = (
    np.stack(
        [
            *np.meshgrid(
                np.arange(0.5, 11.5, 1),
                np.arange(0.5, 11.5, 1),
            ),
            -10.0 * np.ones((11, 11)),
        ]
    )
    .reshape((3, -1))
    .T
)
dests = sources.copy()
dests[:, 2] = 10.0  # z moves from -10 → 10

# run raytrace
# For each muon, we get the voxel indices it passes through and the lengths in each voxel
all_muon_voxels, all_muon_lengths_in_voxels = raytrace(
    dests, sources, vol, vol_start=(0, 0, 0), vol_spacing=(1, 1, 1)
)
print(all_muon_lengths_in_voxels[0])
# We'll now visualize a subset of the muons and their voxel intersections
# choose 10 random muons

n_muons = len(all_muon_voxels)

# randomly select 10 muons (or fewer if there are less than 10)
n_draw = min(10, n_muons)
selected_muons = np.random.choice(n_muons, size=n_draw, replace=False)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

# compute global max path length for normalization
all_lengths_flat = np.hstack(
    [
        all_muon_lengths_in_voxels[m]
        for m in selected_muons
        if len(all_muon_lengths_in_voxels[m]) > 0
    ]
)
norm = mcolors.Normalize(vmin=0, vmax=all_lengths_flat.max())
cmap = cm.viridis

for m in selected_muons:
    voxels = np.array(all_muon_voxels[m])
    lengths = np.array(all_muon_lengths_in_voxels[m])

    if len(voxels) == 0:
        continue

    x = voxels[:, 0]
    y = voxels[:, 1]
    z = voxels[:, 2]

    # get colors for this muon
    colors = cmap(norm(lengths))

    # scatter points
    ax.scatter(x, y, z, c=colors, s=50 + 100 * lengths / lengths.max(), alpha=0.8)

    # line connecting the points
    ax.plot(x, y, z, linewidth=2, alpha=0.7, color="gray")

ax.set_xlabel("x voxel index")
ax.set_ylabel("y voxel index")
ax.set_zlabel("z voxel index")
ax.set_title(f"{n_draw} randomly selected muons voxel intersections")

# axes limits match volume
ax.set_xlim(0, vol.shape[2])
ax.set_ylim(0, vol.shape[1])
ax.set_zlim(0, vol.shape[0])

# create a colorbar using ScalarMappable
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # dummy array
fig.colorbar(sm, ax=ax, label="Path length in voxel")

plt.show()
plt.savefig("random_muons_voxels.png")
