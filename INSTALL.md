# Installation

## Environment
Download third party libraries:
```shell
git clone https://github.com/Fitzgera1d/3DV_Reconstruction.git
cd 3DV_Reconstruction
git submodule update --init --recursive
```

Install python environment:
```shell
# Be sure that you are currently under the repo directory:
# NOTE: we assume the cuda version is 11.3 by default. If you are using other cuda version, please modify the environment.yaml accordingly (Line. 10).
# NOTE: Please look up for the version in https://pytorch.org/get-started/previous-versions/ for both PyTorch, TorchVision and TorchAudio dependencies, and modify the environment.yaml accordingly (Line. 17, 19, 20).
conda env create -f environment.yaml
conda activate reconstruction
```

Install [multi-view evaluation tool](https://github.com/ETH3D/multi-view-evaluation)(Optional) follow their instruction (used to evaluate ETH3D's triangulation metrics).

Download pretrained weights from [here](https://drive.google.com/file/d/1phP6U1CQ7jo1ZfUZ0xRYDf0IBZX_t9qb/view?usp=sharing) and place it under repo directory. Then unzip it by running the following command:
```shell
# Be sure that you are currently under the repo directory:
tar -xvf weight.tar
rm -rf weight.tar
```

## Modified COLMAP version installation
### Why?
This repo is partly based on COLMAP. We modified the COLMAP to support the following features:
1. Parallel-BA: We modified the COLMAP to support parallel bundle adjustment using CUDA.
2. Incremental Model Refinement: This is a core geometry part in our SfM refinement pipeline.
3. Reval image names instead image IDs during Mapping.

Before the installation, please make sure that your CUDA version is below than 11.8. Otherwise, GPU-based Parallel-BA will not work.

### Install 
```shell
apt-get install -y git \
    	cmake \
    	build-essential \
    	libboost-program-options-dev \
    	libboost-filesystem-dev \
    	libboost-graph-dev \
    	libboost-system-dev \
    	libboost-test-dev \
    	libeigen3-dev \
    	libsuitesparse-dev \
    	libfreeimage-dev \
        libgoogle-glog-dev \
    	libgflags-dev \
    	libglew-dev \
    	qtbase5-dev \
    	libqt5opengl5-dev \
    	libcgal-dev \
		libmetis-dev \
    	&& apt-get install -y libcgal-qt5-dev \
        && apt-get install -y libatlas-base-dev libsuitesparse-dev 
```

```shell
# Install ceres-solver:
cd path/to/your/desired/ceres/installation/directory
git clone https://github.com/ceres-solver/ceres-solver.git
cd ceres-solver && git checkout 1.14.x
mkdir build && cd build && cmake .. -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF && make -j && make install
```
```shell
# Install the folk-and-modified COLMAP:
cd path/to/your/desired/colmap/installation/directory
git clone https://github.com/hxy-123/colmap.git
cd colmap && mkdir build && cd build && cmake .. && make -j 

# If you have sudo permission, you can install COLMAP by:
sudo make install

# If you do not have sudo permission, keep in mind your colmap exe path and export it to your environment variable:
export COLMAP_PATH=/your/path/colmap/build/src/exe/colmap
```