import random
import threading
import time

BUFFER_SIZE = 5
buffer = []

mutex = threading.Lock()
empty_slots = threading.Semaphore(BUFFER_SIZE)
full_slots = threading.Semaphore(0)


def producer(id, items_to_produce):
    for item in range(items_to_produce):
        empty_slots.acquire()
        mutex.acquire()
        buffer.append(item)
        print(f"Producer {id} produced {item} | Buffer: {buffer}")
        mutex.release()
        full_slots.release()
        time.sleep(random.uniform(0.1, 0.5))


def consumer(id, items_to_consume):
    for _ in range(items_to_consume):
        full_slots.acquire()
        mutex.acquire()
        item = buffer.pop(0)
        print(f"Consumer {id} consumed {item} | Buffer: {buffer}")
        mutex.release()
        empty_slots.release()
        time.sleep(random.uniform(0.1, 0.5))


if __name__ == "__main__":
    num_items = 10

    prod_thread = threading.Thread(
        target=producer,
        args=(1, num_items)
    )

    cons_thread = threading.Thread(
        target=consumer,
        args=(1, num_items)
    )

    prod_thread.start()
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()

    print("All items produced and consumed.")