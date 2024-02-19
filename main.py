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

    def find_ty_process(self):
        while True:
            try:
                self.mem = Pymem("Ty.exe")
                self.module = process.module_from_name(self.mem.process_handle, "Ty.exe").lpBaseOfDll
                return True
            except:
                print("Ty.exe not found. Retrying in 1 second.")
                time.sleep(1)

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
        if self.find_ty_process():
            self.load_settings()
            self.create_gui()
            if self.keybind:
                keyboard.add_hotkey(self.keybind, self.add_time)
            tk.mainloop()

    def create_gui(self):
        root = tk.Tk()
        root.title("TA Resetter")
        root.geometry("250x100")
        root.resizable(False, False)
        root.attributes('-toolwindow', True)
        root.attributes('-topmost', True)

        button_text = f"\nPress [{self.keybind}]\n to reset" if self.keybind else "\nKeybind not found. Please check your settings file."
        button = tk.Label(root, text=button_text)
        button.pack()

        self.root = root


if __name__ == "__main__":
    modifier = TyTimeModifier()
    modifier.start()
