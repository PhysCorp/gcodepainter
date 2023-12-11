```
                      _                  _       _            
                     | |                (_)     | |           
   __ _  ___ ___   __| | ___ _ __   __ _ _ _ __ | |_ ___ _ __ 
  / _` |/ __/ _ \ / _` |/ _ \ '_ \ / _` | | '_ \| __/ _ \ '__|
 | (_| | (_| (_) | (_| |  __/ |_) | (_| | | | | | ||  __/ |   
  \__, |\___\___/ \__,_|\___| .__/ \__,_|_|_| |_|\__\___|_|   
   __/ |                    | |                               
  |___/                     |_|                               
```

### A simple tool to convert PNG images to GCODE for plotting machines

<!-- Badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

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
Please clone my git repository with `git clone https://github.com/PhysCorp/gcodepainter.git`.

1. Ensure that python3, python3-pip, and anaconda are installed on your system. Anaconda can be retrieved from [here](https://www.anaconda.com/products/individual). If you are on Windows, you can install anaconda with [chocolatey](https://chocolatey.org/) using `choco install anaconda3`.
2. If not done from above, create a conda environment with `conda create --name gcodepainter python=3.8`.
3. Activate the conda environment with `conda activate gcodepainter`.
4. Install the requirements with `python3 -m pip install -r requirements.txt`.
5. Run `python3 main.py` to start the program. By default, it launches the Flask GUI, available at `http://localhost:5000/`.
6. *(Optional)* To install Pronterface for direct printing to plotting machines, please follow the instructions [here](https://www.pronterface.com/). Pronterface standalone EXE must be placed in the `tools` directory, and named `pronterface.exe`.

Here are some example commands to run the program:
```bash
# Run the program with the GUI with all defaults
python3 main.py

# Run in standalone mode with input filename = "test.png" in the temp folder, and output filename = "test.gcode" in the temp folder
python3 main.py --webui=false --input="test.png" --output="test.gcode"
```

Additional commands and documentation are available with `python3 main.py --help`.

*Coming soon: Task Runner support!*

## Program defaults
```bash
input -> "input.png"
output -> "output.gcode"
maximum_x -> 613
maximum_y -> 548
initial_speed -> 50000
border_x -> 50
border_y -> 50
debug -> False
display -> False
dwell_time -> 10000
acceleration -> 1000
camera_number -> 0
pi_mode -> False
input_pin -> 17 if "pi_mode" == False, else 0
execute -> False
webui -> True
camera_bounds -> "(150,60)(515,435)"
```

## Note
To view the generated GCODE, we include a link to view the GCODE on an open-source plotting webpage at https://nraynaud.github.io/webgcode/. `You are required to paste in the GCODE yourself.` Alternatively, you can download the GCODE file directly. This program also supports the ability to execute the GCODE directly to a plotting machine, if you have one connected to your computer and if you have `Pronterface` installed on your *WINDOWS* computer.

## Uninstall
1. Deactivate the conda environment with `conda deactivate`.
2. Remove the conda environment with `conda remove --name gcodepainter --all`.

### More Info
For more information, please also refer to the `docs` folder in the repository, which contains a project report!