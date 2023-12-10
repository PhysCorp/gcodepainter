# Intro/motivation
I've always enjoyed playing with 3D printers and plotting machines. I've also always enjoyed playing with computer vision. I wanted to combine these two interests into a project that would allow me to create a simple, easy-to-use tool to convert images into GCODE for plotting machines. This project is the result of that, allowing users to either take a photo with their webcam (using the console-based tool), or upload an image via the web interface, to process and convert into usable GCODE for a plotting machine to trace the image.

# Methods
## What I did to meet basic requirements
This project is written in Python 3.8 specifically. 

## What else did I do to achieve proposed idea
This project utilizes a variety of libraries, including `opencv-python`, `opencv-contrib-python`, `numpy`, `rich`, and `flask`. The `opencv` libraries are used for image processing, `numpy` is used for array manipulation, `rich` is used for console output, and `flask` is used for the web interface. This project also utilizes `Pronterface` to execute the GCODE directly to a plotting machine.

# Results
## Visualization of outcomes
This project has both a command-line tool, as well as a fancy web interface via Flask API. The Flask webpage allows for users to learn about the project, upload a photo, view each processing step's image output, and download/print the resulting GCODE. Each step is visualized on the webpage in the form of a small text snippet and a modified image based on what the user uploads. After the GCODE is converted, it offers an option to copy the GCODE to the clipboard and view it on an open-source plotting webpage at https://nraynaud.github.io/webgcode/ `(you are required to paste in the GCODE yourself)`. Alternatively, you can download the GCODE file directly. This program also supports the ability to execute the GCODE directly to a plotting machine, if you have one connected to your computer and if you have `Pronterface` installed on your *WINDOWS* computer.

# Reminder: Compress into ZIP