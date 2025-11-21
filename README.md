<p align="center">

  <h1 align="center">🍎Mono3DOrchard：UAV-based Monocular 3D Panoptic Mapping for Fruit Shape Completion in Orchard</h1>
  
  <p align="center">
    <a href="https://kaiwen-robotics.github.io/"><strong>Kaiwen Wang</strong></a>
    ·
    <a href="https://www.ipb.uni-bonn.de/people/yue-pan/"><strong>Yue Pan</strong></a>
    ·
    <a href="https://www.ipb.uni-bonn.de/people/federico-magistri/index.html"><strong>Federico Magistri</strong></a>
    ·
    <a href="https://www.wur.nl/nl/personen/lammert-kooistra.htm"><strong>Lammert Kooistra</strong></a>
    ·
    <a href="https://www.ipb.uni-bonn.de/people/cyrill-stachniss/index.html"><strong>Cyrill Stachniss</strong></a>
    ·
    <a href=""><strong>Wensheng Wang</strong></a>
    ·
    <a href="https://www.joao-valente.com/doku.php?id=home"><strong>João Valente</strong></a>
  </p>
</p>

![image](https://github.com/Kaiwen-Robotics/Mono3DOrchard/blob/main/Figs/Framework.png)
*Our UAV-based 3D mapping framework for orchard fruit completion
----
![image](https://github.com/Kaiwen-Robotics/Mono3DOrchard/blob/main/Figs/Visualization.png)
----

## Dataset
The dataset used in this work is available at: https://zenodo.org/records/15635995

The dataset includes RGB videos in four differnt flight modes in real orchards and coresponding ground truth fruit diameters, and 3D fruit models collected with high accuracy 3D scanner in a controlled lab environment.

## Installation
### 1. Clone this repository
```bash
git clone https://github.com/Kaiwen-Robotics/Mono3DOrchard.git
cd Mono3DOrchard
```
### 2. Create a conda environment and install dependencies for Grounded-SAM2
Follow the instructions from the official Grounded-SAM2 repository:
First download the checkpoints of Grounded-SAM2 and Grounding-Dino by running the following commands:
```bash
cd Grounded-SAM2
cd checkpoints
bash download_ckpts.sh
cd ..
cd gdino_checkpoints
bash download_ckpts.sh
cd ../..
```
Then create a conda environment and install dependencies:
```bash
conda create -n GDSAM2 python=3.10 -y
conda activate GDSAM2
pip install torch torchvision torchaudio
pip install -e .
pip install --no-build-isolation -e grounding_dino
```

### 3. Install 3D shape completion dependencies
Set up a new conda environment and install dependencies:
```bash
conda create -n Mono3D python=3.8 -y
conda activate Mono3D
conda install pytorch==2.0.0 torchvision==0.15.1 torchaudio==2.0.0 pytorch-cuda=11.7 -c pytorch -c nvidia -y
pip install open3d==0.17 opencv-python scikit-image wandb tqdm plyfile
```

## Usage
### 1. Download the dataset
Download the dataset from https://zenodo.org/records/15635995 and create a Data directory. Unzip it to the data directory of this repository.

### 2. Process the videos to frames
Run the following script to extract frames from the videos:
```bash
ffmpeg -i <video_path> -qscale:v 2 <output_frame_path>/frame_%05d.jpg
```
### 3. Run the framework with Grounded-SAM2 to track fruits and get masks
Activate the GDSAM2 conda environment, change the path and text prompt in the script and run the following command:
```bash
cd Grounded-SAM2
conda activate GDSAM2
python grounded_sam2_tracking_demo_with_continuous_id_gd1.5.py
```
### 4. Run SfM in Metashape to get camera poses and depth maps
Import the extracted frames into Metashape and run the SfM pipeline to get camera poses and depth maps. Export the camera poses as a xml file. Export depth maps as 1 band 32-bit float tiff images.

### 5. Dataset preparation for 3D shape completion
First change the input and output paths in the script `scripts/Metashape_Camera_Pose.py`. Run the script to convert the camera poses from xml to txt format:
```bash
conda activate Mono3D
python scripts/Metashape_Camera_Pose.py
```
Then, change the input and output paths in the script `scripts/DatasetProcess.py` and run the script to prepare the dataset for 3D shape completion:
```bash
python scripts/DatasetProcess.py
```
### 6. Train a DeepSDF model, and run 3D shape completion
Follow the instructions in the DeepSDF repository to train a DeepSDF model on the training set.
Link to DeepSDF repository: https://github.com/facebookresearch/DeepSDF
After training the DeepSDF model, change the data_dir path in the config file `configs/shape_completion_challenge_apple.yaml` to the prepared dataset path. Then run the following command to perform 3D shape completion on the field environment apple dataset:
```bash
python run_shape_completion.py --config configs/shape_completion_challenge_apple.yaml
```


## Citation
If you find this work useful in your research, please cite our paper.
```bibtex
@article{wang2026uav,
  title={UAV-based monocular 3D panoptic mapping for fruit shape completion in orchard},
  author={Wang, Kaiwen and Pan, Yue and Magistri, Federico and Kooistra, Lammert and Stachniss, Cyrill and Wang, Wensheng and Valente, Jo{\~a}o},
  journal={ISPRS Journal of Photogrammetry and Remote Sensing},
  volume={231},
  pages={608--621},
  year={2026},
  publisher={Elsevier}
}
```