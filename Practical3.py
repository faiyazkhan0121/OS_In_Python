import threading
import time


def worker(thread_id, sleep_time):
    print(f"[Thread-{thread_id}] Starting work...")
    time.sleep(sleep_time)
    print(
        f"[Thread-{thread_id}] "
        f"Work completed after {sleep_time} second(s)."
    )


def thread_lifecycle_demo():
    print("=== Thread Lifecycle Demo ===\n")
    threads = []

    for i in range(5):
        t = threading.Thread(
            target=worker,
            args=(i, i + 1),
            name=f"Worker-{i}"
        )
        threads.append(t)
        print(
            f"[Main] {t.name} created, "
            f"Alive? {t.is_alive()}"
        )

    print()

    for t in threads:
        t.start()
        print(
            f"[Main] {t.name} started, "
            f"Alive? {t.is_alive()}"
        )

    print()

    for t in threads:
        t.join()
        print(
            f"[Main] {t.name} finished, "
            f"Alive? {t.is_alive()}"
        )

    print("\nAll threads have completed their work.")


if __name__ == "__main__":
    thread_lifecycle_demo()