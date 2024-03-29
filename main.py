import tkinter as tk
import time
import keyboard
import json
from pymem import Pymem, process

class TyTimeModifier:
    def __init__(self):
        self.mem = None
        self.module = None
        self.keybind = None
        self.root = None

    def find_ty_process(self):
        try:
            self.mem = Pymem("Ty.exe")
            self.module = process.module_from_name(self.mem.process_handle, "Ty.exe").lpBaseOfDll
            return True
        except:
            print("Ty.exe not found.")
            return False

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.keybind = settings.get('keybind', '').upper()
                if self.keybind:
                    print("Loaded keybind:", self.keybind)
                else:
                    print("No keybind found in settings file.")
        except FileNotFoundError:
            print("Settings file not found.")
        except Exception as e:
            print("An unexpected error occurred while loading settings:", e)

    def add_time(self):
        if self.mem and self.module:
            try:
                time_offset = 0x28CB6C
                self.mem.write_float(self.module + time_offset, 69420.0)
                print("Time added!")
            except Exception as e:
                print("An error occurred while adding time:", e)
        else:
            print("Ty process not found. Make sure Ty.exe is running.")

    def start(self):
        self.load_settings()
        self.create_gui()  # Create GUI window first
        self.check_ty_process()  # Start checking for Ty process

    def check_ty_process(self):
        if self.find_ty_process():
            if self.keybind:
                keyboard.add_hotkey(self.keybind, self.add_time)
        if self.root:
            self.root.after(1000, self.check_ty_process)  # Retry after 1 second

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("TA Resetter")
        self.root.geometry("250x100")
        self.root.resizable(False, False)
        self.root.attributes('-toolwindow', True)
        self.root.attributes('-topmost', True)

        button_text = f"\nPress [{self.keybind}]\n to reset" if self.keybind else "\nKeybind not found. Please check your settings file."
        button = tk.Label(self.root, text=button_text)
        button.pack()


if __name__ == "__main__":
    modifier = TyTimeModifier()
    modifier.start()
    tk.mainloop()
