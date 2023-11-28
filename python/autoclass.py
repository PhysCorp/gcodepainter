# MIT License
# Copyright (c) 2023 Matt Curtis

# Attempt to import all necessary libraries
try:
    import os, sys, math, cv2, platform, time
    import numpy as np
    from rich import print as rich_print
    from rich.traceback import install
    install() # Install rich traceback
except ImportError as e:
    print("[ERROR] You are missing one or more libraries. Please use PIP to install any missing libraries.")
    print("Try running `python3 -m pip install -r requirements.txt`")
    print(f"Traceback: {e}")
    quit()

# Determine the main project directory, for compatibility (the absolute path to this file, up one dir)
maindirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") 

# Define the class itself
class AutoClass:
    def __init__(self):
        self.test = ""