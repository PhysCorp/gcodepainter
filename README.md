# gcodepainter
### A simple tool to convert PNG images to GCODE for plotting machines

## Environment Info (conda)
This project utilizes conda to manage the environment. To create the environment, run `conda create --name gcodepainter python=3.8` and activate the environment with `conda activate gcodepainter`.

## Required Dependencies
The following dependencies are required to run this project (included in `requirements.txt`):
- [x] Python 3.8 (this is SPECIFICALLY required to ensure compatibility)
- [x] rich
- [x] opencv-python
- [x] numpy
- [x] opencv-contrib-python
- [x] flask

## Other Info & Installation
This project is currently in development. Please clone the git repository with `git clone https://github.com/PhysCorp/gcodepainter.git`.

1. Ensure that python3, python3-pip, and anaconda are installed on your system. Anaconda can be retrieved from [here](https://www.anaconda.com/products/individual). If you are on Windows, you can install anaconda with [chocolatey](https://chocolatey.org/) using `choco install anaconda3`.
2. Create a conda environment with `conda create --name gcodepainter python=3.8`.
3. Activate the conda environment with `conda activate gcodepainter`.
4. Install the requirements with `python3 -m pip install -r requirements.txt`.
5. Run `python3 main.py` to start the program. Here is an example command:
```python3 main.py --display --camera_bounds="(150,60)(515,435)" --execute```

Additional commands and documentation are available with `python3 main.py --help`.

Coming soon: Task Runner support!

## Uninstall
1. Deactivate the conda environment with `conda deactivate`.
2. Remove the conda environment with `conda remove --name gcodepainter --all`.