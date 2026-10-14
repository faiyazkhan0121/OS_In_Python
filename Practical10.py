import random
from collections import deque


class Process:

    def __init__(self, pid, burst_time, arrival_time=0):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.remaining_time = burst_time
        self.completion_time = None
        self.waiting_time = 0
        self.turnaround_time = 0
        self.last_execution_time = arrival_time


def round_robin(processes, time_quantum):
    time = 0
    ready_queue = deque()
    gantt_chart = []

    processes.sort(key=lambda p: p.arrival_time)
    processes_left = processes.copy()

    while processes_left or ready_queue:
        for p in processes_left[:]:
            if p.arrival_time <= time:
                ready_queue.append(p)
                processes_left.remove(p)

        if not ready_queue:
            time += 0.1
            continue

        current = ready_queue.popleft()
        start_time = time
        exec_time = min(current.remaining_time, time_quantum)
        
        time += exec_time
        current.remaining_time -= exec_time

        gantt_chart.append((current.pid, start_time, time))

        current.waiting_time += start_time - current.last_execution_time
        current.last_execution_time = time

        if current.remaining_time > 0:
            ready_queue.append(current)
        else:
            current.completion_time = time
            current.turnaround_time = (
                current.completion_time - current.arrival_time
            )

    return gantt_chart, processes


if __name__ == "__main__":
    num_processes = 5
    time_quantum = 1.0

    processes = [
        Process(
            i,
            burst_time=random.uniform(1, 5),
            arrival_time=random.uniform(0, 3)
        )
        for i in range(num_processes)
    ]

    print("Processes:")

    for p in processes:
        print(
            f"P{p.pid}: "
            f"arrival={p.arrival_time:.2f}, "
            f"burst={p.burst_time:.2f}"
        )

    gantt_chart, finished_processes = round_robin(
        processes,
        time_quantum
    )

    print("\nGantt Chart:")

    for pid, start, end in gantt_chart:
        print(
            f"| P{pid} ({start:.1f}-{end:.1f}) ",
            end=""
        )

    print("|")

    total_wt = 0
    total_tat = 0

    print("\nProcess Details:")

    for p in finished_processes:
        total_wt += p.waiting_time
        total_tat += p.turnaround_time

        print(
            f"P{p.pid}: "
            f"WT={p.waiting_time:.2f}, "
            f"TAT={p.turnaround_time:.2f}"
        )

    print(
        f"\nAverage Waiting Time: "
        f"{total_wt / num_processes:.2f}"
    )

    print(
        f"Average Turnaround Time: "
        f"{total_tat / num_processes:.2f}"
    )