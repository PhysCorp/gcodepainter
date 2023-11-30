from flask import Flask, render_template
import os

class WebUI:
    def __init__(self):
        self.app = Flask(__name__)

    def display_files(self):
        # Get the path to the "html" directory
        html_dir = os.path.join(os.path.dirname(__file__), 'html')

        # Get the list of files in the "html" directory
        files = os.listdir(html_dir)

        # Render the template and pass the list of files to it
        return render_template('index.html', files=files)

    def run(self):
        if __name__ == '__main__':
            self.app.run()
