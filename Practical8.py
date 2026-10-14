import random
import threading
import time
from queue import Queue


class Process:

    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time


fcfs_queue = Queue()
cpu_lock = threading.Semaphore(1)


def process_execution(process):
    fcfs_queue.put(process)
    print(
        f"Process {process.pid} arrives with burst time "
        f"{process.burst_time:.2f}"
    )

    while True:
        if fcfs_queue.queue[0] == process:
            cpu_lock.acquire()
            print(f"Process {process.pid} starts execution")
            time.sleep(process.burst_time)
            print(f"Process {process.pid} finishes execution")
            fcfs_queue.get()
            cpu_lock.release()
            break
        else:
            time.sleep(0.01)


if __name__ == "__main__":
    processes = [
        Process(i, random.uniform(0.5, 1.5))
        for i in range(5)
    ]

    threads = [
        threading.Thread(
            target=process_execution,
            args=(p,)
        )
        for p in processes
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("FCFS scheduling simulation completed.")