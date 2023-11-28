# MIT License

# Copyright (c) 2023 Matt Curtis

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# TODO: Package this in Flask app

# TODO: Use Flask to call auto function, as well as adjust parameters by updating JSON file

# TODO: Create a dictionary or a shelf to store the associated randomly-generated folder strings with the original file names

# Attempt to import all necessary libraries
try:
    import os, time, sys # General
    from rich import print as rich_print # Pretty print
    from rich.traceback import install # Pretty traceback
    install() # Install traceback
except ImportError as e:
    print("[ERROR] You are missing one or more libraries. Please use PIP to install any missing libraries.")
    print("Try running `python3 -m pip install -r requirements.txt`")
    print(f"Traceback: {e}")
    quit()

# Determine the main project directory, for compatibility (the absolute path to this file)
maindirectory = os.path.join(os.path.dirname(os.path.abspath(__file__))) 

# Custom low-level functions
def print(text="", log_filename="", end="\n", max_file_mb=10):
    if log_filename != "":
        log_file_path = os.path.join(maindirectory, "logs", log_filename)
        if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > max_file_mb * 1024 * 1024:
            with open(log_file_path, "w") as f:
                f.write("")
        with open(log_file_path, "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text}")
    rich_print(text, end=end)

# [ MAIN ]
if __name__ == "__main__":
    # Print hello ASCII text
    print("""
                      _                  _       _            
                     | |                (_)     | |           
   __ _  ___ ___   __| | ___ _ __   __ _ _ _ __ | |_ ___ _ __ 
  / _` |/ __/ _ \ / _` |/ _ \ '_ \ / _` | | '_ \| __/ _ \ '__|
 | (_| | (_| (_) | (_| |  __/ |_) | (_| | | | | | ||  __/ |   
  \__, |\___\___/ \__,_|\___| .__/ \__,_|_|_| |_|\__\___|_|   
   __/ |                    | |                               
  |___/                     |_|                               
""")
    print("Welcome to gcodepainter, developed by Matt Curtis.")
    print()

    # Get arguments from kwargs
    try:
        sys_args = sys.argv[1:]
        arguments = {}
        for value in sys_args:
            if value.startswith("--"):
                value = value[2:]
            if "=" not in value:
                arguments[value] = True
            else:
                value = value.split("=")
                arguments[value[0]] = value[1]
    except IndexError:
        print(log_filename="errors.log", text="[ERROR]: No arguments were provided. You must provide arguments in the format of `argument=value`")
        print(log_filename="errors.log", text="Example: `python3 main.py input=\"FULL_PATH_TO_IMAGE.png\" output=\"FULL_PATH_TO_OUTPUT.gcode\"`")
        print(log_filename="errors.log", text="Please see the README for more info, or try `python3 main.py --help`")
        quit()

    # Override everything and show help-docs if user includes help in arguments
    if "help" in arguments:
        print("Welcome to gcodepainter!")
        print(f"usage: python3 {sys.argv[0]} [OPTIONS]")
        print("This script is used to convert an image, either from a webcam or a file, into a set of line segment g-code, similar to a CNC etch-a-sketch.")
        print("Under optimal conditions, the image should be 1:1 ratio, and be black and white.")
        print("[OPTIONS]")
        print("input: The input filename. If this is not provided, then the script will capture from a webcam.")
        print("output: The output filename. This is required.")
        print("help: Displays this help message.")
        quit()
    
    # Parse the arguments
    opts_dict = {}
    def parse_arg(opts_dict, arg_key, arg_val, default_val="", required=False):
        try:
            opts_dict[arg_key] = arg_val
            return arg_val
        except KeyError:
            if required:
                print(f"[ERROR]: No {arg_key} was provided. This is a required argument. Please see `python3 main.py --help` for more info.")
                quit()
            else:
                print(f"[INFO]: No {arg_key} was provided. Assuming value of `{default_val}`.")
                opts_dict[arg_key] = default_val
                return default_val
    
    # TODO: Remove the variable names and switch to a dictionary
        
    # Parse all arguments
    program_input_filename = parse_arg(opts_dict, "input", arguments["input"], "", required=True)
    program_output_filename = parse_arg(opts_dict, "output", arguments["output"], "output.gcode")
    program_maximum_x = int(parse_arg(opts_dict, "maximum_x", arguments["maximum_x"], 613))
    program_maximum_y = int(parse_arg(opts_dict, "maximum_y", arguments["maximum_y"], 548))
    program_initial_speed = int(parse_arg(opts_dict, "initial_speed", arguments["initial_speed"], 50000))
    program_border_x = int(parse_arg(opts_dict, "border_x", arguments["border_x"], 50))
    program_border_y = int(parse_arg(opts_dict, "border_y", arguments["border_y"], 50))
    program_debug = bool(parse_arg(opts_dict, "debug", arguments["debug"], False))
    program_display = bool(parse_arg(opts_dict, "display", arguments["display"], False))
    program_dwell_time = int(parse_arg(opts_dict, "dwell_time", arguments["dwell_time"], 10000))
    program_initial_acceleration = int(parse_arg(opts_dict, "acceleration", arguments["acceleration"], 1000))
    camera_number = int(parse_arg(opts_dict, "camera_number", arguments["camera_number"], 0))
    pi_mode = bool(parse_arg(opts_dict, "pi_mode", arguments["pi_mode"], False))
    input_pin = int(parse_arg(opts_dict, "input_pin", arguments["input_pin"], 17 if pi_mode else None))
    print_flag = bool(parse_arg(opts_dict, "execute", arguments["execute"], False))
    show_webui = bool(parse_arg(opts_dict, "webui", arguments["webui"], False))
    program_camera_bounds = parse_arg(opts_dict, "camera_bounds", arguments["camera_bounds"], "(0,0)(0,0)")
    
    # Convert camera bounds to the format of "(0,0)(0,0)" to [[0,0],[0,0]]
    program_camera_bounds = [[int(coord) for coord in program_camera_bounds.replace("(", "").replace(")", ",").split(",")] for program_camera_bounds in program_camera_bounds.split(")(")]

    # Display all arguments in console
    print(f"Arguments: \n{opts_dict}")