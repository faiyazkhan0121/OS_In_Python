import random


class Process:

    def __init__(self, pid, burst_time, arrival_time=0, priority=0):
        self.pid = pid
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority

        self.start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None


def fcfs_scheduler(processes):
    return sorted(processes, key=lambda p: p.arrival_time)


def sjf_scheduler(processes):
    return sorted(processes, key=lambda p: p.burst_time)


def priority_scheduler(processes):
    return sorted(processes, key=lambda p: p.priority)


def simulate_non_preemptive(processes):
    current_time = 0
    gantt_chart = []

    for process in processes:
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        process.start_time = current_time
        process.completion_time = current_time + process.burst_time
        process.waiting_time = process.start_time - process.arrival_time
        process.turnaround_time = (
            process.completion_time - process.arrival_time
        )

        gantt_chart.append(
            (process.pid, process.start_time, process.completion_time)
        )

        current_time = process.completion_time

    return gantt_chart


if __name__ == "__main__":
    processes = [
        Process(
            i,
            burst_time=random.uniform(1, 4),
            arrival_time=random.uniform(0, 5),
            priority=random.randint(1, 5)
        )
        for i in range(5)
    ]

    print("Processes:")

    for p in processes:
        print(
            f"P{p.pid}: "
            f"arrival={p.arrival_time:.2f}, "
            f"burst={p.burst_time:.2f}, "
            f"priority={p.priority}"
        )

    scheduled = fcfs_scheduler(processes)
    gantt_chart = simulate_non_preemptive(scheduled)

    print("\nGantt Chart:")

    for pid, start, end in gantt_chart:
        print(f"| P{pid} ({start:.1f}-{end:.1f}) ", end="")

    print("|")

    print("\nProcess Details:")

    total_wt = 0
    total_tat = 0

    for p in scheduled:
        total_wt += p.waiting_time
        total_tat += p.turnaround_time

        print(
            f"P{p.pid}: "
            f"WT={p.waiting_time:.2f}, "
            f"TAT={p.turnaround_time:.2f}"
        )

    print(
        f"\nAverage Waiting Time: "
        f"{total_wt / len(processes):.2f}"
    )

    print(
        f"Average Turnaround Time: "
        f"{total_tat / len(processes):.2f}"
    )