#TODO: Add another thread for the event handler.

import queue
import threading
from TheHub.web import app as web_app
from TheHub.logic import event_handler as event_loop

# Create an empty list in which to place our threads.
threads = []

event_queue = queue.Queue()

print("Creating threads.")
web_thread = threading.Thread(
        name = "Web App",
        target = web_app
)
event_thread = threading.Thread(
        name = "Event Loop",
        target = event_loop
)

threads.extend([web_thread, event_thread])

print("Starting threads.")
for thread in threads:
    thread.start()
    print("Started thread: {}".format(thread.name))
