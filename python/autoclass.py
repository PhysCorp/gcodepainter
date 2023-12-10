# MIT License
# Copyright (c) 2023 Matt Curtis

# Attempt to import all necessary libraries
try:
    import os, time, sys, time, math, platform # General
    import cv2 # OpenCV
    import numpy as np # Numpy
    from rich import print as rich_print # Pretty print
    from rich.traceback import install # Pretty traceback
    install() # Install traceback
except ImportError as e:
    print("[INFO] You are missing one or more libraries. Please use PIP to install any missing libraries.")
    print("In addition, make sure you are running Python 3.8")
    print("Try running `python3 -m pip install -r requirements.txt`")
    print("Note: This file cannot be run standalone. You must run `python3 main.py`")
    print(f"Traceback: {e}")
    quit()

# Determine the main project directory, for compatibility (the absolute path to this file, up one dir)
maindirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") 

# Custom low-level functions
def print(text="", log_filename="", end="\n", max_file_mb=10):
    global maindirectory
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    if log_filename == "":
        log_filename = f"{script_name}.log"
    log_file_path = os.path.join(maindirectory, "logs", log_filename)
    if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > max_file_mb * 1024 * 1024:
        with open(log_file_path, "w") as f:
            f.write("")
    with open(log_file_path, "a") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")
    rich_print(text, end=end)

# Define the class itself
class AutoClass:
    def __init__(self, opts_dict):
        # Hello message
        print("[purple4][AUTOCLASS][/purple4] Initializing AutoClass...")
        
        # Define the options dictionary
        self.opts_dict = opts_dict

        # If any values are not set in the opts_dict, raise an error
        for key, value in opts_dict.items():
            if value == "":
                print(f"[red][ERROR][/red] The value for {key} is not set. Please set it when instantiating the AutoClass class.")
                quit()

        # Set program arguments
        self.program_input_filename = str(self.opts_dict['input'])
        self.program_output_filename = str(self.opts_dict['output'])
        self.program_maximum_x = int(self.opts_dict['maximum_x'])
        self.program_maximum_y = int(self.opts_dict['maximum_y'])
        self.program_initial_speed = int(self.opts_dict['initial_speed'])
        self.program_border_x = int(self.opts_dict['border_x'])
        self.program_border_y = int(self.opts_dict['border_y'])
        self.program_debug = bool(self.opts_dict['debug'])
        self.program_display = bool(self.opts_dict['display'])
        self.program_dwell_time = int(self.opts_dict['dwell_time'])
        self.program_initial_acceleration = int(self.opts_dict['acceleration'])
        self.camera_number = int(self.opts_dict['camera_number'])
        self.pi_mode = bool(self.opts_dict['pi_mode'])
        self.input_pin = int(self.opts_dict['input_pin'])
        self.print_flag = bool(self.opts_dict['execute'])
        self.show_webui = bool(self.opts_dict['webui'])
        self.program_camera_bounds = str(self.opts_dict['camera_bounds'])

        # Convert camera bounds to the format of "(0,0)(0,0)" to [[0,0],[0,0]]
        temp_bounds = self.program_camera_bounds.replace(")(",",").replace("(","").replace(")","").split(",")
        self.program_camera_bounds = [[int(temp_bounds[0]), int(temp_bounds[1])], [int(temp_bounds[2]), int(temp_bounds[3])]]

        # Set the full paths for input and output filenames
        self.program_input_filename = os.path.join(maindirectory, "temp", self.program_input_filename)
        self.program_output_filename = os.path.join(maindirectory, "temp", self.program_output_filename)

        # If pi_mode is set, import GPIO and set the pins
        if self.pi_mode:
            print("[purple4][AUTOCLASS][/purple4] Initializing GPIO...")
            try:
                import RPi.GPIO as GPIO
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            except Exception as e:
                print(f"[red][ERROR][/red] Failed to initialize GPIO. Are you running this on a Pi? Traceback: {e}")
                quit()
        
    # Cleanup function to be called when the program is exiting
    def cleanup(self):
        if self.pi_mode:
            try:
                import RPi.GPIO as GPIO
                GPIO.cleanup()
            except Exception as e:
                print(f"[red][ERROR][/red] Failed to cleanup GPIO. Are you running this on a Pi? Traceback: {e}")
                quit()
    
    # Function to return contents of a variable
    def get_prefs(self, var):
        return self.opts_dict.get(var, None)
    
    # Function to get whether or not an image is ready at the program_input_filename
    def is_image_ready(self):
        return os.path.exists(self.program_input_filename)

    # Function to get whether output is configured
    def is_output_configured(self):
        return self.program_output_filename != ""

    # Function to save the current image to the program_input_filename, with "_modified" appended to the end
    def save_image(self, image=None):
        if image is None:
            image = self.image
        print("[purple4][AUTOCLASS][/purple4] Saving image...")
        # Get the current folder from the program_input_filename
        current_folder = os.path.dirname(self.program_input_filename)
        # Get the current filename from the program_input_filename
        current_filename = os.path.basename(self.program_input_filename)
        # Get the current filename without the extension
        current_filename_without_extension = os.path.splitext(current_filename)[0]
        # Get the current extension
        current_extension = os.path.splitext(current_filename)[1]
        # Get the new filename
        new_filename = current_filename_without_extension + "_modified" + current_extension
        # Save the image
        cv2.imwrite(os.path.join(current_folder, new_filename), image)
        print("[purple4][AUTOCLASS][/purple4] Image saved.")
        return os.path.join(current_folder, new_filename)
    
    # Function to display an image
    def display_image(self, image=None, window_name="Output"):
        if image is None:
            image = self.image
        if not self.show_webui and self.program_display:
            temp_resized_image = cv2.resize(image, (512, 512))
            print(f"[gold1][INFO][/gold1]: Showing \"{window_name}\", press q to close.")
            cv2.imshow(window_name, temp_resized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        return image
    
    # Function to attempt to get an image from the camera
    def get_image(self):
        # If camera_number is -1, get a blank image
        if self.camera_number == -1:
            return np.zeros((self.program_maximum_y, self.program_maximum_x, 3), np.uint8)
        else:
            # Prep to take photo
            image_looks_good = False
            while not image_looks_good:
                # If webUI is not enabled, wait for user to press enter
                if not self.show_webui and self.program_display:
                    print("[INFO]: Press [yellow]ENTER[/yellow] to capture an image from the webcam.")
                    input()
                # Take photo
                print("[purple4][AUTOCLASS][/purple4] Capturing image from webcam...")
                cap = cv2.VideoCapture(self.camera_number)
                frame = cap.read()[1]
                cv2.imwrite(self.program_input_filename, frame)
                print("[purple4][AUTOCLASS][/purple4] Image captured.")
                # If webUI is not enabled, display the image
                if not self.show_webui and self.program_display:
                    print("[purple4][AUTOCLASS][/purple4] Displaying image...")
                    self.display_image(frame, "Captured Image")
                    print("[purple4][AUTOCLASS][/purple4] Image displayed.")
                    image_looks_good = input("[ASK] Does the image look good? Y/n ").lower() == "y"
                    if not image_looks_good:
                        print("[purple4][AUTOCLASS][/purple4] Retrying...")
                    else:
                        print("[purple4][AUTOCLASS][/purple4] Image looks good.")
                else:
                    image_looks_good = True
            return frame
        
    # Import image
    def import_image(self):
        print("[purple4][AUTOCLASS][/purple4] Importing image...")
        try:
            self.image = cv2.imread(self.program_input_filename)
        except Exception as e:
            print(f"[red][ERROR][/red] Failed to import image. Please check the input filename. Traceback: {e}")
            quit()
        print("[purple4][AUTOCLASS][/purple4] Image imported.")
    
    # Rotate image 180 degrees
    def rotate_image(self):
        print("[purple4][AUTOCLASS][/purple4] Rotating image...")
        self.image = cv2.rotate(self.image, cv2.ROTATE_180)
        print("[purple4][AUTOCLASS][/purple4] Image rotated.")
    
    # Crop image
    def crop_image(self):
        print("[purple4][AUTOCLASS][/purple4] Cropping image based on camera bounds...")
        if self.program_camera_bounds != [[0, 0], [0, 0]]:
            print("[purple4][AUTOCLASS][/purple4] Camera bounds: " + str(self.program_camera_bounds))
            self.image = self.image[self.program_camera_bounds[0][1]:self.program_camera_bounds[1][1], self.program_camera_bounds[0][0]:self.program_camera_bounds[1][0]]
        print("[purple4][AUTOCLASS][/purple4] Image cropped.")

    # Convert image to grayscale
    def grayscale_image(self):
        print("[purple4][AUTOCLASS][/purple4] Converting image to grayscale...")
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        print("[purple4][AUTOCLASS][/purple4] Image converted to grayscale.")

    # Convert image to black and white
    def invert_image(self):
        print("[purple4][AUTOCLASS][/purple4] Converting image to black and white...")
        self.image = cv2.bitwise_not(self.image)
        print("[purple4][AUTOCLASS][/purple4] Image converted to black and white.")

    # Threshold image
    def threshold_image(self):
        print("[purple4][AUTOCLASS][/purple4] Thresholding image...")
        self.image = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY)[1]
        print("[purple4][AUTOCLASS][/purple4] Image thresholded.")
    
    # Convert image to fixed size
    def resize_image_fixed(self, width=1000, height=1000):
        print("[purple4][AUTOCLASS][/purple4] Resizing image to fixed size...")
        self.image = cv2.resize(self.image, (width, height))
        print(f"[purple4][AUTOCLASS][/purple4] Image resized to fixed size of \"{width}x{height}\"")
    
    # Apply Euclidean Distance Transform to get distance map
    def get_distance_map(self):
        print("[purple4][AUTOCLASS][/purple4] Getting distance map...")
        self.distance_map = cv2.distanceTransform(self.image, cv2.DIST_L2, 5)
        print("[purple4][AUTOCLASS][/purple4] Distance map obtained.")
        return self.distance_map
    
    # Normalize distance map
    def normalize_distance_map(self):
        print("[purple4][AUTOCLASS][/purple4] Normalizing distance map...")
        cv2.normalize(self.distance_map, self.distance_map, 0, 255, cv2.NORM_MINMAX)
        print("[purple4][AUTOCLASS][/purple4] Distance map normalized.")
    
    # Use thinning method to get skeleton of the image
    def get_skeleton(self):
        print("[purple4][AUTOCLASS][/purple4] Getting skeleton...")
        self.skeleton = cv2.ximgproc.thinning(self.image, cv2.ximgproc.THINNING_ZHANGSUEN)
        self.skeleton = self.skeleton.astype(np.uint8)
        self.skeleton = cv2.cvtColor(self.skeleton, cv2.COLOR_GRAY2BGR)
        print("[purple4][AUTOCLASS][/purple4] Skeleton obtained and converted back to image.")
        return self.skeleton

    # "Solve" pixels with my method to gather all white pixels and compare coords to build list of nearest ones
    # [NOTE]: This is *essential* to writing the gcode as otherwise it would plot random points instead of our drawn line
    def solve_pixels(self):
        print("[purple4][AUTOCLASS][/purple4] Solving pixels by computing nearest neighbors...")
        print("[hot_pink3][SOLVING][/hot_pink3] Finding coords of all white pixels...")
        # Gather coords of all white pixels in a list
        white_pixels = []
        for y in range(0, 1000):
            for x in range(0, 1000):
                if self.skeleton[y][x][0] == 255:
                    white_pixels.append([x, y])
        print("[hot_pink3][SOLVING][/hot_pink3] Coords gathered.")
        # Create a new list of solved_white_pixels
        solved_white_pixels = []
        # Loop through the list of white_pixels and identify the ordered pair that has the least neighbors
        least_neighbors = 2
        least_neighbors_index = 0
        # Print progress bar with 50 hashtags
        print("[INFO]: Progress: [                                                 ]", end=f"\r[INFO]: Progress: [")
        for i in range(0, len(white_pixels)):
            neighbors = 0
            for j in range(0, len(white_pixels)):
                # Print hashtags for progress bar based on len(white_pixels)*len(white_pixels) iterations, limited to 50
                if len(white_pixels)*len(white_pixels) > 50:
                    if (i*len(white_pixels) + j) % (len(white_pixels)*len(white_pixels) // 50) == 0:
                        print("#", end="")
                if i != j:
                    if abs(white_pixels[i][0] - white_pixels[j][0]) <= 1:
                        if abs(white_pixels[i][1] - white_pixels[j][1]) <= 1:
                            neighbors += 1
            if neighbors < least_neighbors:
                least_neighbors = neighbors
                least_neighbors_index = i
        print("]")
        # Add the pixel with the least neighbors to solved_white_pixels
        try:
            solved_white_pixels.append(white_pixels[least_neighbors_index])
            # Pop the pixel with the least neighbors from the white_pixels list
            white_pixels.pop(least_neighbors_index)
        except IndexError:
            print("[red][ERROR][/red]: No white pixels found in image.")
            return []
        # Loop through white_pixels, identifying the closest pixel to the current pixel and popping it from the list
        print("[hot_pink3][SOLVING][/hot_pink3] Solving white pixels...")
        # Print progress bar with 50 hashtags
        print("[INFO]: Progress: [                                                 ]", end=f"\r[INFO]: Progress: [")
        ii = 0
        iii = len(white_pixels)
        for i in range(0, len(white_pixels)):
            # Get the current pixel
            current_pixel = solved_white_pixels[-1]
            # Get the distance between the current pixel and the first pixel in white_pixels
            distance = math.sqrt(((white_pixels[0][0] - current_pixel[0]) ** 2) + ((white_pixels[0][1] - current_pixel[1]) ** 2))
            # Get the index of the closest pixel
            closest_pixel_index = 0
            # Loop through white_pixels, finding the closest pixel
            for j in range(0, len(white_pixels)):
                # Print hashtags for progress bar based on len(white_pixels)*len(white_pixels) iterations, limited to 50
                if iii*iii > 50:
                    if (ii*iii + j) % (iii*iii // 50) == 0:
                        print("#", end="")
                # Get the distance between the current pixel and the current pixel in white_pixels
                current_distance = math.sqrt(((white_pixels[j][0] - current_pixel[0]) ** 2) + ((white_pixels[j][1] - current_pixel[1]) ** 2))
                # If the current distance is less than the distance, then set the distance to the current distance and set the closest pixel index to the current index
                if current_distance < distance:
                    distance = current_distance
                    closest_pixel_index = j
            # Add the closest pixel to the solved_white_pixels list
            solved_white_pixels.append(white_pixels[closest_pixel_index])
            # Pop the closest pixel from the white_pixels list
            white_pixels.pop(closest_pixel_index)
            ii += 1
        print("]")
        print("[hot_pink3][SOLVING][/hot_pink3] White pixels solved.")
        return solved_white_pixels

    # Function to get the gcode for a list of points
    def get_gcode(self, points):
        print("[purple4][AUTOCLASS][/purple4] Getting gcode...")
        # Convert the list of pixels to gcode
        print("[dark_olive_green3][GCODE][/dark_olive_green3] Configuring initial settings...")
        gcode = []
        # If the initial speed is not 0, then set the initial speed
        if self.program_initial_speed != 0:
            gcode.append(f"G0 F{self.program_initial_speed}\n")
        # If the initial acceleration is not 0, then set the initial acceleration
        if self.program_initial_acceleration != 0:
            gcode.append(f"M204 X{self.program_initial_acceleration} Y{self.program_initial_acceleration} Z{self.program_initial_acceleration}\n")
        # Convert the list of pixels to gcode
        print("[dark_olive_green3][GCODE][/dark_olive_green3] Initial settings configured.")
        print("[dark_olive_green3][GCODE][/dark_olive_green3] Converting pixels to gcode...")
        for point in points:
            # Convert the point coordinates to printer coordinates
            printer_x = (((self.program_maximum_x-(2*self.program_border_x))/1000) * point[0]) + self.program_border_x
            printer_y = (((self.program_maximum_y-(2*self.program_border_y))/1000) * point[1]) + self.program_border_y

            if self.program_debug:
                printer_z = 0
            else:
                printer_z = float(printer_y)

            # Round all values to 3 decimal places
            printer_x = round(printer_x, 3)
            printer_y = round(printer_y, 3)
            printer_z = round(printer_z, 3)

            # Append the point to gcode
            gcode.append(f"G0 X{printer_x} Y{printer_y} Z{printer_z}\n")
        print("[dark_olive_green3][GCODE][/dark_olive_green3] Contours converted to gcode.")
        # Insert a dwell at line 4 (found this was essential later)
        gcode.insert(3, f"G04 P{self.program_dwell_time}\n")
        # Convert the gcode list to a string
        gcode = "".join(gcode)
        print("[purple4][AUTOCLASS][/purple4] Gcode obtained.")
        return gcode

    # Write gcode to file
    def write_gcode(self, gcode):
        print("[purple4][AUTOCLASS][/purple4] Writing gcode to file...")
        with open(self.program_output_filename, "w") as f:
            f.write(gcode)
        print(f"[purple4][AUTOCLASS][/purple4] Gcode written to \"{self.program_output_filename}\"")
    
    # Print gcode by opening Pronterface
    # NOTE: This has only been tested on WINDOWS
    def print_gcode(self):
        print("[purple4][AUTOCLASS][/purple4] Printing gcode...")
        # Print the gcode
        print("[wheat4][PRINT][/wheat4] Beginning to print/draw gcode...")
        # Run the pronterface -b & command (if on Linux) or pronterface.exe -b & command (if on Windows)
        if platform.system() == "Linux":
            # Get the filename path of program_output_filename without the other directories
            temp_program_output_filename = self.program_output_filename.split("/")[-1]
            # Check if Pronterface is installed
            if not os.path.exists("/usr/bin/pronterface"):
                print("[red][ERROR][/red]: Pronterface is not installed. Please install it with `sudo apt install pronterface`.")
                return False
            # CD into maindirectory and then run the command "sudo pronterface -a -e \"load temp_program_output_filename print\"
            os.system(f"cd \"{os.path.join(maindirectory, 'temp')}\" && sudo pronterface -a -e \"load {temp_program_output_filename}\"")
        elif platform.system() == "Windows":
            # Get the filename path of program_output_filename without the other directories
            temp_program_output_filename = self.program_output_filename.split("\\")[-1]
            # CD into maindirectory and then run the command "pronterface.exe -a -e \"load temp_program_output_filename print\"
            os.system(f"cd \"{os.path.join(maindirectory, 'temp')}\" && ..\\pronterface.exe -a -e \"load {temp_program_output_filename}\"")
        else:
            print("[red][ERROR][/red]: Unsupported operating system. Please use Linux or Windows. Gcode will not be printed.")
            return False
        print("[purple4][AUTOCLASS][/purple4] Gcode printed.")
        return True