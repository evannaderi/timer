import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import time
import os
import pync

class Timer:
    def __init__(self, master, duration, name, alternate_duration=None):
        self.master = master
        self.initial_duration = duration
        self.duration = duration
        self.time_left = duration
        self.name = name
        self.is_running = False
        self.alternate_duration = alternate_duration
        self.is_alternate = False
        self.sound_on = True
        self.auto_repeat = False

        self.frame = tk.Frame(master)
        self.frame.pack(pady=5)

        self.label = tk.Label(self.frame, text=self.format_time(self.time_left), font=("Arial", 24))
        self.label.pack(side=tk.LEFT, padx=5)

        self.start_stop_button = tk.Button(self.frame, text="Start", command=self.start_stop)
        self.start_stop_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side=tk.LEFT)

        self.change_time_button = tk.Button(self.frame, text="Change Time", command=self.change_time)
        self.change_time_button.pack(side=tk.LEFT)

        self.sound_var = tk.BooleanVar(value=True)
        self.sound_check = tk.Checkbutton(self.frame, text="Sound", variable=self.sound_var, command=self.toggle_sound)
        self.sound_check.pack(side=tk.LEFT)

        self.repeat_var = tk.BooleanVar(value=False)
        self.repeat_check = tk.Checkbutton(self.frame, text="Auto-repeat", variable=self.repeat_var, command=self.toggle_repeat)
        self.repeat_check.pack(side=tk.LEFT)

        self.delete_button = tk.Button(self.frame, text="Delete", command=self.delete)
        self.delete_button.pack(side=tk.LEFT)

    def start_stop(self):
        if self.is_running:
            self.is_running = False
            self.start_stop_button.config(text="Start")
        else:
            self.is_running = True
            self.start_stop_button.config(text="Stop")
            self.countdown()

    def countdown(self):
        if self.is_running:
            if self.time_left <= 0:
                self.label.config(text="Time's up!")
                self.notify()
                self.switch_duration()
            else:
                self.label.config(text=self.format_time(self.time_left))
                self.time_left -= 1
                self.master.after(1000, self.countdown)

    def notify(self):
        pync.notify(f"{self.name}: Time's up!", title="Timer Notification")
        if self.sound_on:
            os.system('afplay /System/Library/Sounds/Glass.aiff')

    def switch_duration(self):
        if self.alternate_duration:
            self.is_alternate = not self.is_alternate
            self.time_left = self.alternate_duration if self.is_alternate else self.duration
        else:
            self.time_left = self.duration
        
        if self.auto_repeat:
            self.is_running = True
            self.countdown()
        else:
            self.is_running = False
            self.start_stop_button.config(text="Start")
        
        self.label.config(text=self.format_time(self.time_left))

    def reset_timer(self):
        self.time_left = self.duration
        self.is_running = False
        self.is_alternate = False
        self.start_stop_button.config(text="Start")
        self.label.config(text=self.format_time(self.time_left))

    def change_time(self):
        new_duration = simpledialog.askinteger("Change Time", f"Enter new duration for {self.name} in seconds:", 
                                               parent=self.master, minvalue=1, initialvalue=self.duration)
        if new_duration:
            self.duration = new_duration
            if self.alternate_duration:
                new_alternate = simpledialog.askinteger("Change Alternate Time", 
                                                        f"Enter new alternate duration for {self.name} in seconds:", 
                                                        parent=self.master, minvalue=1, initialvalue=self.alternate_duration)
                if new_alternate:
                    self.alternate_duration = new_alternate
            self.reset_timer()

    def toggle_sound(self):
        self.sound_on = self.sound_var.get()

    def toggle_repeat(self):
        self.auto_repeat = self.repeat_var.get()

    def delete(self):
        self.frame.destroy()

    @staticmethod
    def format_time(seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        if hours > 0:
            return f"{hours:02d}:{mins:02d}:{secs:02d}"
        else:
            return f"{mins:02d}:{secs:02d}"

class TimerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Multi-Timer App")
        self.master.geometry("600x600")

        self.timers = []

        self.add_timer_frame = tk.Frame(master)
        self.add_timer_frame.pack(pady=10)

        self.add_custom_timer_button = tk.Button(self.add_timer_frame, text="Add Custom Timer", command=self.add_custom_timer)
        self.add_custom_timer_button.pack(side=tk.LEFT, padx=5)

        self.add_eye_timer_button = tk.Button(self.add_timer_frame, text="Add Eye Care Timer", command=self.add_eye_timer)
        self.add_eye_timer_button.pack(side=tk.LEFT, padx=5)

        self.add_pomodoro_timer_button = tk.Button(self.add_timer_frame, text="Add Pomodoro Timer", command=self.add_pomodoro_timer)
        self.add_pomodoro_timer_button.pack(side=tk.LEFT, padx=5)

    def add_custom_timer(self):
        name = simpledialog.askstring("New Timer", "Enter a name for this timer:", parent=self.master)
        if name is None or name.strip() == "":
            name = f"Timer {len(self.timers) + 1}"
        
        duration = simpledialog.askinteger("New Timer", "Enter primary duration in seconds:", parent=self.master, minvalue=1)
        if duration is not None:
            has_alternate = messagebox.askyesno("Alternate Duration", "Do you want to add an alternate duration?")
            if has_alternate:
                alternate_duration = simpledialog.askinteger("New Timer", "Enter alternate duration in seconds:", 
                                                             parent=self.master, minvalue=1)
                if alternate_duration is not None:
                    new_timer = Timer(self.master, duration, name, alternate_duration=alternate_duration)
                    self.timers.append(new_timer)
            else:
                new_timer = Timer(self.master, duration, name)
                self.timers.append(new_timer)

    def add_eye_timer(self):
        new_timer = Timer(self.master, 20 * 60, "Eye Care Timer", alternate_duration=20)
        self.timers.append(new_timer)

    def add_pomodoro_timer(self):
        new_timer = Timer(self.master, 25 * 60, "Pomodoro Timer", alternate_duration=5 * 60)
        self.timers.append(new_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
