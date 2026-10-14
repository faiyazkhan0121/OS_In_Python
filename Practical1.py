from multiprocessing import Process, Semaphore, Value
import time

def producer(empty, full, data):
    for i in range(5):
        empty.acquire()
        data.value += 1
        print(f"Produced: {data.value}")
        full.release()
        time.sleep(1)

def consumer(empty, full, data):
    for i in range(5):
        full.acquire()
        print(f"Consumed: {data.value}")
        empty.release()
        time.sleep(1)

if __name__ == "__main__":
    empty = Semaphore(1)
    full = Semaphore(0)
    data = Value('i', 0)

    producer_process = Process(target=producer, args=(empty, full, data))
    consumer_process = Process(target=consumer, args=(empty, full, data))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()
    print("Producer and Consumer have completed successfully.")
