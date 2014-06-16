import queue
import threading
from TheHub.web import app as web_app
from TheHub.database import db
#from TheHub.logic import event_handler
#from TheHub.logic import bridge

devices = db.session.query(db.Device).all()

# Create queue object to be shared between bridges and event loop.
#event_queue = queue.Queue()

# Instantiate bridge object(s).
#bridge_devices = [bridge.Bridge(event_queue, devices[0].id, devices[0].sensors)]#devices[0], devices[0].sensors)]

# Create a list of bridge devices to give to the event loop. 
#devices = [device]

# Create an empty list in which to place our threads.
threads = []

print("Creating threads.")

# Create web thread object.
web_thread = threading.Thread(
    name = "Web App",
    target = web_app
)

# Create event thread object, give it parameters with kwargs.

#event_loop = event_handler.EventHandler(event_queue, bridge_devices)

#event_thread = threading.Thread(
#    name = "Event Loop",
#    target = event_loop.run,
#)


# Add thread objects to the list of threads.
threads.extend([web_thread])

#threads.extend([event_thread])

print("Starting threads.")
for thread in threads:
    thread.start()
    print("Started thread: {}".format(thread.name))
