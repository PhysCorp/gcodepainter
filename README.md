# gcodepainter
### A simple tool to convert PNG images to GCODE for plotting machines

## Environment info (Conda)

## Required dependencies

## Other info / installation

<!--  -->

## Requirements
- [x] Python == 3.8
- [x] python3-pip package to use PIP
- [x] (optional) conda env for cleaner setup
- [ ] (alternative) python3-virtualenv

## Installation
1. Install python3, python3-pip and anaconda. Anaconda can be retrieved from [here](https://www.anaconda.com/products/individual). If you are on Windows, you can install anaconda with [chocolatey](https://chocolatey.org/) using `choco install anaconda3`.
2. Create a conda environment with `conda create --name gcodepainter python=3.8`.
3. Activate the conda environment with `conda activate gcodepainter`.
4. Install the requirements with `python3 -m pip install -r requirements.txt`.

<!--  -->

## Usage
0. Download this project with `git clone https://github.com/PhysCorp/gcodepainter.git`
1. Activate the conda environment with `conda activate gcodepainter`.
2. Run `python3 main.py` to start the program. Here is an example command:
```python3 main.py --display --camera_bounds="(150,60)(515,435)" --execute```

Additional commands and documentation are available with `python3 main.py --help`.

### Alternate Instructions using virtualenv
Create a new virtualenv with `python3 -m venv venv`.
Activate the virtualenv with `source venv/bin/activate`.
Install the requirements with `python3 -m pip install -r requirements.txt`.

## Uninstall
1. Deactivate the conda environment with `conda deactivate`.
2. Remove the conda environment with `conda remove --name gcodepainter --all`.