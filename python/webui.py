# MIT License
# Copyright (c) 2023 Matt Curtis

# Attempt to import all necessary libraries
try:
    import os, time # General
    from flask import Flask, render_template, send_from_directory, request, url_for, send_file # Flask
    from rich import print as rich_print # Pretty print
    from rich.traceback import install # Pretty traceback
    install() # Install traceback
    from python.autoclass import AutoClass # AutoClass
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
        rich_print(f"[red][ERROR][/red]: Could not clear log file at {log_file_path}.")
    rich_print(text, end=end)

class WebUI:
    def __init__(self, opts_dict):
        # Hello message
        print("[indian_red1][WEBUI][/indian_red1] Initializing WebUI...")
        
        # Initialize Flask
        self.app = Flask(__name__, template_folder=os.path.join(maindirectory, "html"), static_folder=os.path.join(maindirectory, "html", "static"))

        # Define the options dictionary
        self.opts_dict = opts_dict

        # Modify opts_dict[]
        
        # Create the AutoClass object
        self.auto_obj = AutoClass(self.opts_dict)

        # Init the main website text log
        self.web_text = ""

        # Route for serving index.html
        @self.app.route('/')
        @self.app.route('/index.html')
        def index():
            return render_template('index.html')
        
        # Route for serving about.html
        @self.app.route('/about.html')
        def about():
            return render_template('about.html')
        
        # Route to serve the image
        @self.app.route('/files/<filename>')
        def serve_custom_file(filename):
            return send_file(os.path.join(maindirectory, "temp", filename))
        
        # Route for serving live demo
        @self.app.route('/demo.html', methods=['GET', 'POST'])
        def demo():
            try:
                task = str(request.args.get('task'))  # Get the value of the 'task' GET variable
            except TypeError:
                task = "1"
            if request.method == 'POST':
                print("[indian_red1][WEBUI][/indian_red1] POST request received, saving image...")
                # Check if file is uploaded
                if 'file' in request.files:
                    file = request.files['file']
                    # Save the uploaded file as "web_input.png"
                    file.save(os.path.join(maindirectory, "temp", "input.png"))
                    print(f"[indian_red1][WEBUI][/indian_red1] Image saved successfully to \"{os.path.join(maindirectory, 'temp', 'input.png')}\"")
                    # Run build_html function to get HTML based on task and processing
                    heading, content = self.build_html(task="2")
                    return render_template('demo.html', app_heading=str(heading), app_content=str(content))
            # Serve page based on task
            heading, content = self.build_html(task)
            return render_template('demo.html', app_heading=str(heading), app_content=str(content))
        
        # Route to serve the terminal logs
        @self.app.route('/logs/<filename>')
        def send_log_file(filename):
            return send_from_directory(os.path.join(maindirectory, "logs"), filename)

    def run(self):
        self.app.run()
    
    def display_image_html(self, img_path="input.png", img_width="100%", img_height="auto"):
        # If the file doesn't exist, return an error
        if not os.path.exists(os.path.join(maindirectory, "temp", img_path)):
            return "<p>ERROR: Image not found.</p>"
        # Return the HTML of the image
        return f'<img src="{url_for("serve_custom_file", filename=img_path)}" width="{img_width}" height="{img_height}">'
    
    def build_html(self, task=-1):        
        # If task is not set, set it to 1
        if task == -1:
            task = "1"
        
        # Depending on the task, run different functions
        if task == "1":
            # Task 1: Show the initial file/camera upload page
            print("[indian_red1][WEBUI][/indian_red1] Showing demo welcome message...")
            # Display the program welcome message
            welcome_text = "Welcome to gcodepainter interactive demo"
            text_content = "<p>To begin the demo, please select a file to upload.</p><p>Note: For photos, you MUST use a photo with a solid-white color background with as little noise as possible, and draw on the canvas with black marker or pen. In addition, make sure the photo isn't too large as that takes MUCH more time to process.</p><p>Don't know what to do? Upload one of our example images in the `examples` folder of the project!</p><hr>"
            # Add a form to upload a png or jpg file
            text_content += "<form action='/demo.html' method='post' enctype='multipart/form-data' class='form-inline'><input type='hidden' name='task' value='2'><div class='form-group'><input type='file' name='file' accept='image/png, image/jpeg' class='form-control-file' required></div><span style='height: 12px; display: inline-block;'></span><button type='submit' class='btn btn-primary'><i data-feather='upload'></i> Upload</button></form>"
            # Return the heading and content
            return (welcome_text, text_content)
        elif task == "2":
            # Display the uploaded/captured image
            print("[indian_red1][WEBUI][/indian_red1] Displaying uploaded/captured image...")
            # Get the uploaded/captured image
            welcome_text = "Uploaded/Captured Image"
            text_content = "<div>"
            text_content += "<p>Does this image look correct? If not, please go back and try again. Note: Remember that this image must be a solid white background if possible, and must be drawn in black marker or pen.</p><a class='btn btn-primary' href='/demo.html?task=3'><i data-feather='check'></i> Looks good</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='x'></i> Try again</a>"
            text_content += "</div><hr>"
            text_content += self.display_image_html(img_width="512px")
            # Return the heading and content
            return (welcome_text, text_content)
        elif task == "3":
            # Run routine to capture, convert, and create gcode
            # Make sure that an output filename is configured
            welcome_text = "Initial Checks & Image Import"
            text_content = ""
            if not self.auto_obj.is_output_configured():
                text_content = "<p>[ERROR]: No output filename was provided. Please see `python3 main.py --help` for more info.</p>"
                text_content += "<hr><div>"
                text_content += "<a class='btn btn-primary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
                text_content += "</div>"
                return (welcome_text, text_content)
            # Import the image
            self.auto_obj.import_image()
            self.auto_obj.save_image()
            # Show the initial image
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>This is the initial image that was successfully imported. Now, we will rotate the image 180 degrees, as the camera is mounted upside down in our project.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "4":
            # Rotate the image 180 degrees (we mounted camera upside down)
            self.auto_obj.rotate_image()
            self.auto_obj.save_image()
            # Display the image progress
            welcome_text = "Flipped Image"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Next, we will crop the image based on the camera bounds to remove any extra whitespace.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "5":
            # Crop the image based on camera bounds
            self.auto_obj.crop_image()
            self.auto_obj.save_image()
            # Display the image progress
            welcome_text = "Cropped Image"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Next, we will convert the image to grayscale to remove any color noise.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "6":
            # Convert the image to grayscale
            self.auto_obj.grayscale_image()
            self.auto_obj.save_image()
            # Display the image progress
            welcome_text = "Grayscale Image"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Next, we will invert the image to make the background black and the drawing white.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "7":
            # Invert the image
            self.auto_obj.invert_image()
            self.auto_obj.save_image()
            # Display the image progress
            welcome_text = "Inverted Image"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Next, we will threshold the image to make the image closer to pure black and white.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "8":
            # Threshold the image
            self.auto_obj.threshold_image()
            self.auto_obj.save_image()
            # Display the image progress
            welcome_text = "Thresholded Image"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Next, we will resize the image to a fixed size as this is how we map gcode to pixels.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "9":
            # Convert the image to a fixed size
            self.auto_obj.resize_image_fixed(width=1000, height=1000)
            self.auto_obj.save_image()
            # Display the image progress
            welcome_text = "Resized Image"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Next, we are going to apply a Euclidean distance transform to the image. Distance transforms are used to find the distance of each pixel from the nearest boundary of the image. This will help us find the skeleton of the image.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "10":
            # Apply Euclidean distance transform
            self.distance_map = self.auto_obj.get_distance_map()
            self.auto_obj.save_image(self.distance_map)
            # Display the image progress
            welcome_text = "Distance Map"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Here is the distance map. It may be very dark, but it exists! Now, we will normalize the distance map.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "11":
            # Normalize the distance map
            self.distance_map = self.auto_obj.normalize_distance_map()
            self.auto_obj.save_image(self.distance_map)
            # Display the image progress
            welcome_text = "Normalized Distance Map"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Now, we will use a thinning algorithm to get the skeleton of the image. The skeleton will be used to find adjacent points.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "12":
            # Use thinning method to get skeleton of the image
            self.skeleton = self.auto_obj.get_skeleton()
            self.auto_obj.save_image(self.skeleton)
            # Display the image progress
            welcome_text = "Skeleton"
            text_content = ""
            text_content += self.display_image_html(img_path="input_modified.png", img_width="512px")
            text_content += "<hr><div>"
            text_content += "<p>Now, we will solve the skeleton by finding adjacent points. This converts the skeleton into a list of points, sorted by distance to one another.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "13":
            # Solve the skeleton by finding adjacent points
            self.solved_pixels = self.auto_obj.solve_pixels()
            # Convert to string
            self.solved_pixels_string = [str(i) for i in self.solved_pixels]
            # Display the image progress
            welcome_text = "Solved Skeleton Coordinates"
            text_content = ""
            text_content += "<textarea rows='10' cols='80' readonly>" + str(self.solved_pixels_string) + "</textarea>"
            text_content += "<hr><div>"
            text_content += "<p>Now, we will generate gcode based on the solved pixels. This will be the final gcode that will be printed.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='arrow-right'></i> Continue to next step</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "14":
            # Get the gcode from the solved pixels
            self.gcode = self.auto_obj.get_gcode(self.solved_pixels)
            welcome_text = "Gcode"
            text_content = ""
            text_content += "<p>Here is the gcode that was generated! Please view the code in text-form below, and/or click the button to copy the code to your clipboard, then open an online gcode viewer for you to see the code in action!</p>"
            text_content += "<textarea rows='10' cols='80' readonly id='gcode' name='gcode'>" + self.gcode + "</textarea>"
            text_content += "<hr><div>"
            text_content += "<p>Please click one of the buttons to either copy and view the code in a new tab (you need to paste), or to write the code to a file.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='file-plus'></i> Write gcode to file</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            # Button to copy to clipboard and open in new tab
            text_content += "<span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='javascript:void(0)' onclick='copyToClipboard()'><i data-feather='clipboard'></i> Copy to clipboard and open in new tab</a>"
            text_content += "<script>function copyToClipboard() { var copyText = document.getElementById('gcode'); copyText.select(); copyText.setSelectionRange(0, 99999); document.execCommand('copy'); alert('Reminder: This is opening in a new tab, but the gcode is NOT autofilled. You MUST paste it in the window and click Simulate to view. If the window does not open, make sure to allow popups in your browser.'); window.open('https://nraynaud.github.io/webgcode/', '_blank'); }</script>"
            # Button to download the gcode using f'<a href="{url_for("serve_custom_file", filename="output.gcode")}">'
            text_content += "<span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' class='no-load' href='" + url_for("serve_custom_file", filename="output.gcode") + "' target='_blank'><i data-feather='download'></i> Download gcode</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "15":
            # Write the gcode to the output file
            self.auto_obj.write_gcode(self.gcode)
            welcome_text = "Gcode Written"
            text_content = ""
            text_content += "<p>The gcode has been written to the output file.</p>"
            text_content += "<hr><div>"
            text_content += "<p>Now, we will print the gcode using Pronterface.</p>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='printer'></i> Print gcode</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a><span style='width: 10px; display: inline-block;'></span><a class='btn btn-secondary' href='/demo.html?task=17'><i data-feather='loader'></i> Cleanup Autoclass</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "16":
            # If get_prefs("execute") is enabled, then we print the gcode using Pronterface
            # NOTE: PRONTERFACE ONLY WORKS ON WINDOWS
            if self.auto_obj.get_prefs("execute"):
                self.auto_obj.print_gcode()
                welcome_text = "Gcode is being Printed"
                text_content = ""
                text_content += "<p>If Pronterface is installed and running, the gcode is currently being printed. Next, please cleanup this job before continuing.</p>"
            else:
                welcome_text = "Gcode is not being Printed"
                text_content = ""
                text_content += "<p>The launch args with this program specified not to use Pronterface. Make sure to enable it and install Pronterface if you would like to directly print the gcode. This is <em>not</em> an error! The gcode generation was still successful. Next, please cleanup this job before continuing.</p>"
            text_content += "<div>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=" + str(int(task)+1) + "'><i data-feather='loader'></i> Cleanup Autoclass</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        elif task == "17":
            # Cleanup
            self.auto_obj.cleanup()
            del self.auto_obj
            # Create the AutoClass object
            self.auto_obj = AutoClass(self.opts_dict)
            welcome_text = "Demo Complete"
            text_content = ""
            text_content += "<p>The demo is complete. You can now go back to the beginning and try again.</p>"
            text_content += "<div>"
            text_content += "<a class='btn btn-primary' href='/demo.html?task=1'><i data-feather='rotate-cw'></i> Restart from beginning</a>"
            text_content += "</div>"
            return (welcome_text, text_content)
        
        # Failsafe, return empty strings
        return ("Error has occurred","<p>There was an issue setting the task, please check your syntax.</p>")