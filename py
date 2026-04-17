import webbrowser
import os

# Path to a local HTML file
file_path = os.path.abspath("index.html")
webbrowser.open(f"file://{file_path}")
import webbrowser

url = "https://www.google.com"

# Open in a new tab (if possible)
webbrowser.open_new_tab(url)

# Open in a new browser window (if possible)
webbrowser.open_new(url)

import webbrowser

# Open a URL in the default browser
webbrowser.open("https://www.python.org")
