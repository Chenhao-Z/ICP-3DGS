# ICP-3DGS, ICIP'25
Official PyTorch implementaton of ICIP'2025 paper 'ICP-3DGS: SfM-Free 3D Gaussian Splatting for large-scale unbounded scenes'

### Training
```bash
python run_cf3dgs.py -s data/your_scene \ # change the scene path
              --mode train \
```

### Evaluation
```bash
# pose estimation
python run_cf3dgs.py --source data/your_scene \
                     --mode eval_pose \
                     --model_path ${CKPT_PATH} 

# novel view synthesis
python run_cf3dgs.py --source data/your_scene \
                     --mode eval_nvs \
                     --model_path ${CKPT_PATH} 
``` 
