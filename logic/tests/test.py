import queue
import bridge

bridgetest = bridge.bridge()

bridgetest.test = True

fromhardware = queue.Queue()

bridgetest.from_hw = fromhardware

print("pressing start")
bridgetest.start()

print("putting stuff in the queue")
bridgetest.to_hw.put_nowait("testmsg1")
bridgetest.to_hw.put_nowait("testmsg2")
bridgetest.to_hw.put_nowait("kill")
