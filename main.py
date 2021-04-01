import multiprocessing
import display
import time

def display_launcher(queue:multiprocessing.Queue):
    d = display.Display()
    d.run(queue)


class Message:
    """For sending updates to the display """
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value


if __name__ == "__main__":
    # launch display in another thread
    display_queue = multiprocessing.Queue()
    p = multiprocessing.Process(target=display_launcher, args=(display_queue,))
    p.start()

    # main loop, for processing messages, updating the display and logging data
    i = 0
    display_queue.put(Message("CAN", "Power-up"))
    display_queue.put(Message("CAN", "Ready to drive mode active"))
    while True:
        display_queue.put(Message("speed", i))
        time.sleep(1)
        if i == 5:
            display_queue.put(Message("stopped", True))
        print("running")
        i += 1
