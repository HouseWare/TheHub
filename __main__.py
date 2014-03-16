#TODO: Add another thread for the event handler.

import threading
from TheHub.web import app as web_app

print("TheHub is running.")
print("Starting web app...")

web_thread = threading.Thread(target = web_app)
web_thread.start()
