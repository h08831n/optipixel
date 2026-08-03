import os
import multiprocessing

def get_optimal_worker_count() -> int:
    try:
        cpu_count = multiprocessing.cpu_count()
        # Leave 1 core free for OS/UI responsiveness
        return max(1, cpu_count - 1)
    except Exception:
        return 2
