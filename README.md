# 3DV_Reconstruction

## Installation

Please refer to [INSTALL.md](INSTALL.md) for installation instructions.


## Obtain updates
Our system will be gradually completed and updated. To obtain the latest updates, please pull the newest `main` branch:
```shell
git pull origin main:main

# Very important! Update the submodules:
git submodule update --init --recursive
```

## Installation

Please refer to [INSTALL.md](INSTALL.md) for installation instructions.

## Prepare Dataset
### SfM dataset
The data structure of our system is organized as follows:
```
repo_path/dataset
    - dataset_name1
        - scene_name_1
            - images
                - image_name_1.jpg or .png or ...
                - image_name_2.jpg
                - ...
            - intrins (optional, used for evaluation)
                - camera_name_1.txt
                - camera_name_2.txt
                - ...
            - poses (optional, used for evaluation)
                - pose_name_1.txt
                - pose_name_2.txt
                - ...
        - scene_name_2
            - ...
    - dataset_name2
        - ...
```
The folder naming of `images`, `intrins` and `poses` is **compulsory**, for the identification by our system.

Now, download the training and evaluation datasets, and then format them to required structure following instructions in [DATASET_PREPARE.md](DATASET_PREPARE.md).

### dense reconstruction dataset
The data structure for dense reconstruction is organized as follows, which is the output of our sfm part:
```
outputs/_dataset/
├── dataset_name
│   ├── scene1/
│   │   ├── images
│   │   │   ├── IMG_0.jpg
│   │   │   ├── IMG_1.jpg
│   │   │   ├── ...
│   │   ├── sparse/
│   │       └──0/
│   ├── scene2/
│   │   ├── images
│   │   │   ├── IMG_0.jpg
│   │   │   ├── IMG_1.jpg
│   │   │   ├── ...
│   │   ├── sparse/
│   │       └──0/
...
```

## Prepare Config Files
In this repo, you can either run NVS after SFM, or you can run either part independently by using different configurations with `pipeline.py`. To specify the tasks to be conduct, you can simply change contents of `task_list`.
First modify `configs/dataset/demo_church.yaml` to specify the path of dataset relative to the repo, but you should also get your input in `configs/recon/your_config.yaml` correct if you run recon separately.

## Run Demo data
You can use the following command to get start demo:
```
python pipeline.py +dataset=demo_church.yaml +sfm=hydra_configs/demo/dfsfm.yaml +recon=octreegs/full.yaml task_list=\[sfm,recon\] output_dir=outputs exp_name=baseline
```
SfM result will be saved in `outputs/sfm/demo/church/DetectorFreeSfM_loftr_official_coarse_only__scratch_no_intrin/colmap_refined` in COLMAP format, and can be visualized by `colmap gui`.
Reconstruction result will be saved in `outputs/recon/demo/church/`.

## Viewer
Follow the instructions in [README.md](./third_party/octree_gs/SIBR_viewers/README.md) to set up viewer for your environment.

For more details, you can look at `README.md` for [DetectorFreeSfM](./third_party/dsfm/README.md) and [Octree-Gs](./third_party/octree_gs/README.md)
