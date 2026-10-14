import random
import threading
import time

shared_data = 0
read_count = 0

read_count_lock = threading.Lock()
resource_lock = threading.Lock()
write_request = threading.Lock()


def reader(id):
    global read_count

    while True:
        write_request.acquire()
        write_request.release()

        with read_count_lock:
            read_count += 1
            if read_count == 1:
                resource_lock.acquire()

        print(f"Reader {id} reads shared_data = {shared_data}")
        time.sleep(random.uniform(0.1, 0.5))

        with read_count_lock:
            read_count -= 1
            if read_count == 0:
                resource_lock.release()

        time.sleep(random.uniform(0.1, 0.5))


def writer(id):
    global shared_data

    while True:
        write_request.acquire()
        resource_lock.acquire()

        shared_data += 1
        print(f"Writer {id} updates shared_data to {shared_data}")
        time.sleep(random.uniform(0.2, 0.6))

        resource_lock.release()
        write_request.release()

        time.sleep(random.uniform(0.5, 1.0))


if __name__ == "__main__":
    readers = [
        threading.Thread(target=reader, args=(i,))
        for i in range(3)
    ]

    writers = [
        threading.Thread(target=writer, args=(i,))
        for i in range(2)
    ]

    for t in readers + writers:
        t.daemon = True
        t.start()

    time.sleep(10)
    print("Simulation finished.")