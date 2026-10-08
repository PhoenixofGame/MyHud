import colorsys
import tkinter as tk
from pynput import keyboard
import win32con
import win32gui

try:
    from assets.Config_Manager import ConfigManager
except ImportError:
    from Config_Manager import ConfigManager

cm = ConfigManager()

class Counter:
    def __init__(self, config_file: str, master):
        self.running = False
        self.config_file = config_file
        self.listener = None

        self.main = tk.Toplevel(master)
        self.main.attributes("-topmost", True)
        self.main.update()
        self.main.attributes("-transparentcolor", "black")  # noqa
        self.main.overrideredirect(True)

        self.main.update()
        mainhwnd = win32gui.FindWindow(None, str(self.main.title()))   # noqa
        exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)         # noqa
        exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

        self.screen_width = self.main.winfo_screenwidth()
        self.screen_height = self.main.winfo_screenheight()
        self.main.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        self.canvas  = tk.Canvas(self.main, width=self.screen_width, height=self.screen_height, bg="black", highlightthickness=0)
        self.canvas.pack()

        counter_x_location = cm.load_from_config(config_name=self.config_file, name_in_config="counter_x_location", default=500)
        counter_y_location = cm.load_from_config(config_name=self.config_file, name_in_config="counter_y_location", default=100)
        counter_font = cm.load_from_config(config_name=self.config_file, name_in_config="counter_font", default="Comic Sans MS")
        counter_size = cm.load_from_config(config_name=self.config_file, name_in_config="counter_size", default=50)
        self.counter_color = cm.load_from_config(config_name=self.config_file, name_in_config="counter_color", default="#690f96")
        self.counter_text = cm.load_from_config(config_name=self.config_file, name_in_config="counter_text", default="Default Counter")
        self.counter_start_value = cm.load_from_config(config_name=self.config_file, name_in_config="counter_default_value", default=0)
        self.counter_hotkey_positive = cm.load_from_config(config_name=self.config_file, name_in_config="counter_hotkey_positive", default="r")
        self.counter_hotkey_negative = cm.load_from_config(config_name=self.config_file, name_in_config="counter_hotkey_negative", default="t")

        self.counter = self.canvas.create_text(
            counter_x_location,
            counter_y_location,
            text=f"{self.counter_text} {self.counter_start_value}",
            font=(counter_font, counter_size),
            fill="white"
        )

        if self.counter_color != "rgb":
            self.canvas.itemconfig(
                self.counter,
                fill=self.counter_color
            )

        else:
            title_colors = []
            for i in range(360):
                h = i / 360.0
                r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
                title_colors.append('#{0:02X}{1:02X}{2:02X}'.format(
                    int(r * 255), int(g * 255), int(b * 255)
                ))
            index_color = [0]

            def update_color_titel():
                color = title_colors[index_color[0]]  # noqa
                self.canvas.itemconfig(self.counter, fill=color)
                index_color[0] = (index_color[0] + 1) % len(title_colors)
                title_animation_id = self.main.after(16, update_color_titel)  # noqa

            update_color_titel()

    def add_counter(self):
        counter_default_value = cm.load_from_config(config_name=self.config_file, name_in_config="counter_default_value", default=0)
        counter_current_value = counter_default_value + 1
        self.canvas.itemconfig(self.counter, text= f"{self.counter_text} {counter_current_value}")
        self.canvas.update()
        cm.save_to_config(config_name= self.config_file, what_to_save="counter_default_value", status=counter_current_value)

    def sub_counter(self):
        counter_default_value = cm.load_from_config(config_name=self.config_file, name_in_config="counter_default_value", default=0)
        counter_current_value = counter_default_value - 1
        self.canvas.itemconfig(self.counter, text= f"{self.counter_text} {counter_current_value}")
        self.canvas.update()
        cm.save_to_config(config_name= self.config_file, what_to_save="counter_default_value", status=counter_current_value)

    def start_counter(self):
        self.running = True

        self.counter_hotkey_positive = self.counter_hotkey_positive.lower()
        self.counter_hotkey_negative = self.counter_hotkey_negative.lower()

        def on_release(key):
            try:
                if hasattr(key, 'char') and key.char and key.char.lower() == self.counter_hotkey_positive:
                    self.add_counter()
                if hasattr(key, 'char') and key.char and key.char.lower() == self.counter_hotkey_negative:
                    self.sub_counter()
            except AttributeError:
                pass


        self.listener = keyboard.Listener(on_release=on_release)
        self.listener.start()

        def force_topmost2():
            self.main.attributes("-topmost", True)
            self.main.after(500, force_topmost2) # noqa
        self.main.after(100, force_topmost2) # noqa

    def destroy_main(self):
        self.main.destroy()

    def stop_counter(self):
        self.running = False
        self.listener.stop()
        self.main.after(0, self.destroy_main) # noqa