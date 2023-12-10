# MIT License
# Copyright (c) 2023 Matt Curtis

# Attempt to import all necessary libraries
try:
    import os, time # General
    from flask import Flask, render_template # Flask
    from rich import print as rich_print # Pretty print
    from rich.traceback import install # Pretty traceback
    install() # Install traceback
except ImportError as e:
    print("[INFO] You are missing one or more libraries. Please use PIP to install any missing libraries.")
    print("In addition, make sure you are running Python 3.8")
    print("Try running `python3 -m pip install -r requirements.txt`")
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

class WebUI:
    def __init__(self):
        # Hello message
        print("[indian_red1][WEBUI][/indian_red1] Initializing WebUI...")
        
        # Initialize Flask
        self.app = Flask(__name__, template_folder=os.path.join(maindirectory, "html"))
        
        # Define the options dictionary
        self.opts_dict = opts_dict
        
        # Create the AutoClass object
        self.auto_obj = AutoClass(self.opts_dict)

        # Route for serving index.html
        @self.app.route('/')
        def index():
            return render_template('index.html')

    def run(self):
        self.app.run()
