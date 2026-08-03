from PySide6.QtCore import QThreadPool
from app.utils.system_utils import get_optimal_worker_count

class WorkerPoolManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WorkerPoolManager, cls).__new__(cls)
            cls._instance.pool = QThreadPool()
            cls._instance.set_max_threads(0)  # Auto
        return cls._instance

    def set_max_threads(self, thread_count: int):
        if thread_count <= 0:
            thread_count = get_optimal_worker_count()
        self.pool.setMaxThreadCount(thread_count)

    def start_worker(self, worker):
        self.pool.start(worker)

    def active_thread_count(self) -> int:
        return self.pool.activeThreadCount()

    def clear(self):
        self.pool.clear()
