import threading
import time

class TimerManager:
    def __init__(self, callback):
        self.callback = callback
        self.timer_thread = None
        self.is_running = False
        self.work_interval = 0
        self.break_duration = 0
        self.end_time = None
        
    def start_timer(self, work_minutes, break_minutes):
        if self.is_running:
            return
            
        self.work_interval = work_minutes
        self.break_duration = break_minutes
        self.is_running = True
        self.end_time = time.time() + (work_minutes * 60)
        
        self.timer_thread = threading.Thread(target=self._countdown, daemon=True)
        self.timer_thread.start()
        
    def stop_timer(self):
        self.is_running = False
        if self.timer_thread:
            self.timer_thread.join(timeout=1)
        
    def _countdown(self):
        while self.is_running and time.time() < self.end_time:
            time.sleep(1)
            
        if self.is_running:
            self.callback(self.break_duration)
            
            time.sleep(self.break_duration * 60)
            if self.is_running:
                self.start_timer(self.work_interval, self.break_duration)
    
    def get_time_left(self):
        if self.is_running and self.end_time:
            return max(0, int(self.end_time - time.time()))
        return None