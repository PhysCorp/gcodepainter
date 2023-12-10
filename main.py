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

# [ Structure of my code ]
# main.py: The main file that runs the program
# autoclass.py: The main class that handles all of the image processing and gcode generation
# webui.py: The webui class that handles the web interface

# Attempt to import all necessary libraries
try:
    import os, time, sys, time # General
    from rich import print as rich_print # Pretty print
    from rich.traceback import install # Pretty traceback
    install() # Install traceback
    from python.autoclass import AutoClass # Main class
    from python.webui import WebUI # WebUI class
except ImportError as e:
    print("[INFO] You are missing one or more libraries. Please use PIP to install any missing libraries.")
    print("In addition, make sure you are running Python 3.8")
    print("Try running `python3 -m pip install -r requirements.txt`")
    print(f"Traceback: {e}")
    quit()

# Determine the main project directory, for compatibility (the absolute path to this file)
maindirectory = os.path.join(os.path.dirname(os.path.abspath(__file__))) 

# Custom low-level functions
def print(text="", log_filename="", end="\n", max_file_mb=10):
    global maindirectory
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    if log_filename == "":
        log_filename = f"{script_name}.log"
    log_file_path = os.path.join(maindirectory, "logs", log_filename)
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > max_file_mb * 1024 * 1024:
        try:
            with open(log_file_path, "w") as f:
                f.write("")
        except Exception as e:
            rich_print(f"[red][ERROR][/red]: {e}")
            rich_print(f"[red][ERROR][/red]: Could not clear log file at {log_file_path}.")
    try:
        with open(log_file_path, "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")
    except Exception as e:
        rich_print(f"[red][ERROR][/red]: {e}")
        rich_print(f"[red][ERROR][/red]: Could not write to log file at {log_file_path}.")
    rich_print(text, end=end)

# [ MAIN ]
if __name__ == "__main__":
    # Print hello ASCII text
    print("""[white]
                      _                  _       _            
                     | |                (_)     | |           
   __ _  ___ ___   __| | ___ _ __   __ _ _ _ __ | |_ ___ _ __ 
  / _` |/ __/ _ \ / _` |/ _ \ '_ \ / _` | | '_ \| __/ _ \ '__|
 | (_| | (_| (_) | (_| |  __/ |_) | (_| | | | | | ||  __/ |   
  \__, |\___\___/ \__,_|\___| .__/ \__,_|_|_| |_|\__\___|_|   
   __/ |                    | |                               
  |___/                     |_|                               
[/white]""", log_filename="startup.log")
    # Print my welcome text in cycling colors
    welcome_text = "Welcome to gcodepainter, developed by Matt Curtis."
    color_cycling = ["red", "orange1", "yellow", "green", "blue", "blue_violet", "violet"]
    for i, letter in enumerate(welcome_text):
        rich_print(f"[{color_cycling[i % len(color_cycling)]}]{letter}[/{color_cycling[i % len(color_cycling)]}]", end="")
        time.sleep(0.01)
    print("\n")
    time.sleep(1)

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
        print(log_filename="errors.log", text="[red][ERROR][/red]: No arguments were provided. You must provide arguments in the format of `argument=value`")
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
            if str(arg_val).lower() == "true":
                arg_val = True
            elif str(arg_val).lower() == "false":
                arg_val = False
            opts_dict[arg_key] = arg_val
            return arg_val
        except KeyError:
            if required:
                print(f"[red][ERROR][/red]: No {arg_key} was provided. This is a required argument. Please see `python3 main.py --help` for more info.")
                quit()
            else:
                print(f"[gold1][INFO][/gold1]: No {arg_key} was provided. Assuming value of `{default_val}`.")
                opts_dict[arg_key] = default_val
                return default_val
    
    # Parse all arguments
    parse_arg(opts_dict, "input", str(arguments.get("input", "input.png")), "", required=True)
    parse_arg(opts_dict, "output", str(arguments.get("output", "output.gcode")))
    parse_arg(opts_dict, "maximum_x", int(arguments.get("maximum_x", 613)))
    parse_arg(opts_dict, "maximum_y", int(arguments.get("maximum_y", 548)))
    parse_arg(opts_dict, "initial_speed", int(arguments.get("initial_speed", 50000)))
    parse_arg(opts_dict, "border_x", int(arguments.get("border_x", 50)))
    parse_arg(opts_dict, "border_y", int(arguments.get("border_y", 50)))
    parse_arg(opts_dict, "debug", arguments.get("debug", False))
    parse_arg(opts_dict, "display", arguments.get("display", False))
    parse_arg(opts_dict, "dwell_time", int(arguments.get("dwell_time", 10000)))
    parse_arg(opts_dict, "acceleration", int(arguments.get("acceleration", 1000)))
    parse_arg(opts_dict, "camera_number", int(arguments.get("camera_number", 0)))
    parse_arg(opts_dict, "pi_mode", arguments.get("pi_mode", False))
    parse_arg(opts_dict, "input_pin", int(arguments.get("input_pin", 17 if opts_dict.get("pi_mode", False) else 0)))
    parse_arg(opts_dict, "execute", arguments.get("execute", False))
    parse_arg(opts_dict, "webui", arguments.get("webui", True))
    parse_arg(opts_dict, "camera_bounds", str(arguments.get("camera_bounds", "(150,60)(515,435)")))

    # Display all arguments in console
    print(f"Arguments: {opts_dict}\n")

    # [ Run the program ]
    # If show_webui enabled, then run the webui interface
    # Otherwise, run the program via command line and opencv interface
    if opts_dict.get("webui", False):
        print("[gold1][INFO][/gold1]: WebUI enabled, running webui...")
        webui = WebUI(opts_dict)
        webui.run()
    else:
        print("[gold1][INFO][/gold1]: WebUI disabled, running program in standalone mode...")
        while True:
            # Create the AutoClass object
            auto_obj = AutoClass(opts_dict)
            try:
                # Run routine to capture, convert, and create gcode
                # Make sure that an output filename is configured
                if not auto_obj.is_output_configured():
                    print("[red][ERROR][/red]: No output filename was provided. Please see `python3 main.py --help` for more info.")
                    quit()
                # Check if there is an image already ready from input
                if not auto_obj.is_image_ready():
                    # If not, then capture an image
                    auto_obj.get_image()
                # Import the image
                auto_obj.import_image()
                # Show the initial image
                auto_obj.display_image(window_name="Initial Image")
                # Rotate the image 180 degrees (we mounted camera upside down)
                auto_obj.rotate_image()
                # Display the image progress
                auto_obj.display_image(window_name="Flipped Image")
                # Crop the image based on camera bounds
                auto_obj.crop_image()
                # Display the image progress
                auto_obj.display_image(window_name="Cropped Image")
                # Convert the image to grayscale
                auto_obj.grayscale_image()
                # Display the image progress
                auto_obj.display_image(window_name="Grayscale Image")
                # Invert the image
                auto_obj.invert_image()
                # Display the image progress
                auto_obj.display_image(window_name="Inverted Image")
                # Threshold the image
                auto_obj.threshold_image()
                # Display the image progress
                auto_obj.display_image(window_name="Thresholded Image")
                # Convert the image to a fixed size
                auto_obj.resize_image_fixed(width=1000, height=1000)
                # Display the image progress
                auto_obj.display_image(window_name="Resized Image")
                # Apply Euclidean distance transform
                distance_map = auto_obj.get_distance_map()
                # Display the image progress
                auto_obj.display_image(image=distance_map, window_name="Distance Transform")
                # Normalize distance map
                auto_obj.normalize_distance_map()
                # Display the image progress
                auto_obj.display_image(window_name="Normalized Distance Transform")
                # Use thinning method to get skeleton of the image
                skel = auto_obj.get_skeleton()
                # Display the image progress
                auto_obj.display_image(image=skel, window_name="Skeleton")
                # "Solve" the skeleton by finding adjacent points
                solved_pixels = auto_obj.solve_pixels()
                # Get the gcode from the solved pixels
                gcode = auto_obj.get_gcode(solved_pixels)
                # Write the gcode to the output file
                auto_obj.write_gcode(gcode)
                # If get_prefs("execute") is enabled, then we print the gcode using Pronterface
                # NOTE: PRONTERFACE ONLY WORKS ON WINDOWS
                if auto_obj.get_prefs("execute"):
                    auto_obj.print_gcode()
                # Ask user if they want to convert another image
                if auto_obj.get_prefs("pi_mode"):
                    # Wait for button press from GPIO pin 17
                    print("[INFO]: Press the button to convert another image, or [bright_red]CTRL+C[/bright_red] to exit.")
                    try:
                        GPIO.wait_for_edge(auto_obj.get_prefs("input_pin"), GPIO.FALLING)
                    except Exception as e:
                        print(f"[ERROR]: {e}")
                        print("[INFO]: You may not be running this on a Pi, or you may not have the GPIO library installed. Exiting...")
                        auto_obj.cleanup()
                        quit()
                else:
                    # Wait for user input
                    response = input("[ASK]: Do you want to convert another image? Y/n ")
                    if response.lower() != "y":
                        print("[gold1][INFO][/gold1]: Exiting...")
                        auto_obj.cleanup()
                        quit()
                # Cleanup and run again (loop to beginning)
                auto_obj.cleanup()
            except KeyboardInterrupt:
                print("[gold1][INFO][/gold1]: Keyboard interrupt detected, exiting...")
                auto_obj.cleanup()
                quit()
            # Delete the AutoClass object and loop
            del auto_obj
            print("[gold1][INFO][/gold1]: Restarting program...")