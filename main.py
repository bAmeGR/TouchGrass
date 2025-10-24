import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from time_manage import TimerManager
from notification_manage import show_notification

class TouchGrass:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Touch Grass")
        self.root.geometry("450x400")
        
        self.settings = self.load_settings()
        self.timer_manager = TimerManager(self.on_break_reminder)
        
        self.setup_ui()
        print("Let's Go!")
        
    def load_settings(self):
        default_settings = {
            "work": 45,
            "break_duration": 5,
            "sound_enabled": True,
            "auto_restart": True
        }
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return default_settings
        
    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
    
    def setup_ui(self):
        #Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        #Title
        title_label = ttk.Label(main_frame, text="Touch Grass", 
                               font=('San Francisco', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        #Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        #Work 
        ttk.Label(settings_frame, text="Work (minutes):").grid(row=0, column=0, sticky='w', pady=5)
        self.work_var = tk.StringVar(value=str(self.settings['work']))
        work_combo = ttk.Combobox(settings_frame, textvariable=self.work_var, 
                                 values=["30", "45", "60", "90", "120"], width=10)
        work_combo.grid(row=0, column=1, padx=10, pady=5)
        
        #Break duration
        ttk.Label(settings_frame, text="Break Duration (minutes):").grid(row=1, column=0, sticky='w', pady=5)
        self.break_var = tk.StringVar(value=str(self.settings['break_duration']))
        break_combo = ttk.Combobox(settings_frame, textvariable=self.break_var, 
                                  values=["5", "10", "15", "20"], width=10)
        break_combo.grid(row=1, column=1, padx=10, pady=5)
        
        #Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(button_frame, text="Start Timer", 
                                      command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹Stop Timer", 
                                     command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        #Status 
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="Timer not running")
        self.status_label.pack()
        
        self.time_label = ttk.Label(status_frame, text="", font=('Arial', 24, 'bold'))
        self.time_label.pack(pady=10)
        
        #Options
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.X, pady=10)
        
        self.sound_var = tk.BooleanVar(value=self.settings['sound_enabled'])
        ttk.Checkbutton(options_frame, text=" Enable sound", 
                       variable=self.sound_var).pack(side=tk.LEFT)
        
        self.auto_restart_var = tk.BooleanVar(value=self.settings['auto_restart'])
        ttk.Checkbutton(options_frame, text=" Auto-restart", 
                       variable=self.auto_restart_var).pack(side=tk.LEFT, padx=20)
    

    def start_timer(self):
        try:
            work_minutes = int(self.work_var.get())
            break_minutes = int(self.break_var.get())
            
            self.settings.update({
                'work_interval': work_minutes,
                'break_duration': break_minutes,
                'sound_enabled': self.sound_var.get(),
                'auto_restart': self.auto_restart_var.get()
            })
            self.save_settings()
            
            self.timer_manager.start_timer(work_minutes, break_minutes)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_display()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def stop_timer(self):
        self.timer_manager.stop_timer()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Timer stopped")
        self.time_label.config(text="")
    
    def on_break_reminder(self, break_duration):
        """Called when it's time for a break"""
        show_notification(
            "Break Time",
            f"Take {break_duration} minutes to rest!\nRest your eyes stand up and stretch!",
            self.settings['sound_enabled']
        )
        
        if self.timer_manager.is_running:
            self.root.after(1000, self.update_display)
    
    def update_display(self):
        """Update the countdown display"""
        if self.timer_manager.is_running:
            time_left = self.timer_manager.get_time_left()
            if time_left:
                minutes = time_left // 60
                seconds = time_left % 60
                self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.status_label.config(text="Next break in:")
                self.root.after(1000, self.update_display)
        else:
            self.time_label.config(text="")
            self.status_label.config(text="Timer not running")

if __name__ == "__main__":
    app = TouchGrass()
    app.root.mainloop()