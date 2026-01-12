# Raytrace
General purpose python ray tracing library implemented in on GPU in CUDA as a Cython extension

This code is based on Siddon's algorithm, which has been quite extensively used in medical physics for CT projection and radiation treatment planning.

## Usage
This library allows one to obtain the voxels a muon passes through and the length of the path within each voxel.

## Environment and installation
### CUDA
CUDA is needed to install this software. CUDA needs to be in your PATH and LD_LIBRARY_PATH variables. To do this for example on the UCR GPU machine, you can add the following to your `~/.bashrc`:
```
export PATH=$PATH:/usr/local/cuda-11.8/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-11.8/lib64
```
Then do `source ~/.bashrc` to load your changes.
### Python environment
There are few necessary packages needed for this software. Only `numpy` is strictly necessary and `matplotlib` is needed to run the main example. To set up a Python environment do the following:
```
python3 -m venv raytrace_venv
source raytrace_venv/bin/activate
pip install numpy matplotlib
```
### Installation
To install the software, simply do `pip install .` in the main directory.

## Example
The main example to demonstrate Siddon's algorithm is `test/demo_raytrace.py`. To run this, simply do `python test/demo_raytrace.py`. In this example, a 3D grid is made and muons are sent vertically through the grid. The grid is 11x11 voxels in x-y and has a 5 voxel height along z. The calculated path for a muon should be the intersection with the 5 vertical voxels, each with a path length of 1. The script then plots the paths of 10 randomly selected muons out of the 121 muons that are given to Siddon's algorithm. An example plot of the script is below.
<img width="1000" height="800" alt="image" src="https://github.com/user-attachments/assets/71526d04-fe2c-4ceb-af2e-487bb0bfee09" />

The main function used in this code is `raytrace()`. The function is used as follows:
```
all_muon_voxels, all_muon_lengths_in_voxels = raytrace(
   dests, # 3D array of the final muon positions
   sources, # 3D array of the initial muon positions
   vol, # Defintion of the grid
   vol_start=(0,0,0), # Where the voxels are positioned
   vol_spacing=(1,1,1) # The spacing between each voxel. If you want your voxels to be double this size in each axis for instance, do (2, 2, 2). The path length will then be 2.
)
```
`all_muon_voxels` is a nested list where each entry is a list of voxel indices for each muon. For instance, if an entry is `[array([1, 1, 4]), array([1, 1, 3]), array([1, 1, 2]), array([1, 1, 1]), array([1, 1, 0])]`, the muon intersects with voxel indices (1, 1, 4), (1, 1, 3), (1, 1, 2), (1, 1, 1), and (1, 1, 0). 

`all_muon_lengths_in_voxels` is a 2D list where each entry is a list of path lengths for each muon in the voxels it passed through. For the previous muon we were considering, we get an output of `[np.float64(0.9999999999999998), np.float64(0.9999999999999998), np.float64(0.9999999999999998), np.float64(0.9999999999999998), np.float64(1.0000000000000009)]`. This means the muon has a path length of 1 in the voxels (1, 1, 4), (1, 1, 3), (1, 1, 2), (1, 1, 1), and (1, 1, 0).
