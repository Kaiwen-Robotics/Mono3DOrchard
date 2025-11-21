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