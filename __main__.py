import queue
import threading
from TheHub.web import app as web_app
from TheHub.logic import event_handler as event_loop
from TheHub.logic import bridge

# Create queue object to be shared between bridges and event loop.
event_queue = queue.Queue()

# Instantiate bridge object(s).
device = bridge.Bridge()

# Create a list of bridge devices to give to the event loop. 
devices = [device]

# Create an empty list in which to place our threads.
threads = []

print("Creating threads.")

# Create web thread object.
web_thread = threading.Thread(
    name = "Web App",
    target = web_app
)

# Create event thread object, give it parameters with kwargs.
event_thread = threading.Thread(
    name = "Event Loop",
    target = event_loop,
    kwargs = {
        'inbox':event_queue,
        'devices':devices
    }
)

# Add thread objects to the list of threads.
threads.extend([web_thread, event_thread])

print("Starting threads.")
for thread in threads:
    thread.start()
    print("Started thread: {}".format(thread.name))
