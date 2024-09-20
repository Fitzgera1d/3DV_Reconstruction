from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
import importlib
import random
import shutil

from omegaconf import DictConfig, OmegaConf
import hydra

from third_party import octree_gs
from third_party import dsfm

@hydra.main(version_base=None, config_path="configs", config_name="main.yaml")
def main(cfg: DictConfig):
    if 'sfm' in cfg.task_list:
        cfg.sfm.dataset_base_dir = str(Path(cfg.dataset.base_dir).resolve())
        cfg.sfm.dataset_name = str(cfg.dataset.name)
        cfg.sfm.scene_list = list(cfg.dataset.scene_list)
        cfg.sfm.results_output_dir = str(Path(cfg.output_dir).resolve() / 'sfm')
        cfg.sfm.exp_name = cfg.exp_name

        sfm_result_paths = dsfm.__dict__[cfg.sfm.type](cfg.sfm)
    else:
        sfm_result_paths = set([cfg.recon.source_path])
    
    if 'recon' in cfg.task_list:
        cfg.recon.exp_name = cfg.exp_name
        recon_module = importlib.import_module(f"third_party.{cfg.recon.model_name}")

        _dataset_output_dir = Path(cfg.output_dir).resolve() / '_dataset'

        if 'sfm' in cfg.task_list:
            for src_sparse_path in sfm_result_paths:
                _scene = Path(src_sparse_path).parents[1].name
                _dataset = Path(src_sparse_path).parents[2].name
                _scene_path = _dataset_output_dir / _dataset / _scene
                src_img_path = Path(src_sparse_path).parent / 'temp_images'
                dest_img_path = _scene_path / 'images'
                dest_sparse_path = _scene_path / 'sparse/0'
                for _src, _dest in [(src_img_path, dest_img_path),
                                    (src_sparse_path, dest_sparse_path)]:
                    if _dest.exists():
                        shutil.rmtree(_dest)
                    shutil.copytree(_src, _dest)
                cfg.recon.source_path = str(_scene_path)
                cfg.recon.model_path = str(Path(cfg.output_dir).resolve() / 
                    'recon' / _dataset / _scene / datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
                cfg.recon.model_paths = [cfg.recon.model_path]
                cfg.recon.port = random.randint(10000, 30000)
                for task in cfg.recon.task_list:
                    recon_module.__dict__[task](cfg.recon)
        else:
            for task in cfg.recon.task_list:
                recon_module.__dict__[task](cfg.recon)
            

if __name__ == "__main__":
    main()
    
