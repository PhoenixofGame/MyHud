import colorsys
import tkinter as tk
from pynput import keyboard
import win32con
import win32gui
from ConfigManager import ConfigManager
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
# ===========================OVERLAY===========================
corn = tk.Tk()
corn.attributes("-topmost", True)
corn.update()
corn.attributes("-transparentcolor", "black")  # Transparent background
corn.overrideredirect(True)# Remove window border


# Make the window click-through
corn.update()
mainhwnd = win32gui.FindWindow(None, str(corn.title()))
exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

# fullscreen
screen_width = corn.winfo_screenwidth()
screen_height = corn.winfo_screenheight()
corn.geometry(f"{screen_width}x{screen_height}+0+0")

canvas = tk.Canvas(corn, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
canvas.pack()

# Konfiguration laden
counter_text = ConfigManager().load_from_config(config_name= "config.json", name_in_config= "counter_text")
counter_font = ConfigManager().load_from_config(config_name= "config.json", name_in_config= "counter_font")
counter_size = ConfigManager().load_from_config(config_name= "config.json", name_in_config= "counter_size")
counter_color = ConfigManager().load_from_config(config_name="config.json", name_in_config="counter_color")
counter_start_value = ConfigManager().load_from_config(config_name="config.json", name_in_config="counter_default_value")
counter_hotkey_positive = ConfigManager().load_from_config(config_name="config.json", name_in_config="counter_hotkey_positive")
counter_hotkey_negative = ConfigManager().load_from_config(config_name="config.json", name_in_config="counter_hotkey_negative")
counter_x_location = ConfigManager().load_from_config(config_name="config.json", name_in_config="counter_x_location")
counter_y_location = ConfigManager().load_from_config(config_name="config.json", name_in_config="counter_y_location")


counter = canvas.create_text(
    counter_x_location,
    counter_y_location,
    text=f"{counter_text} {counter_start_value}",
    font=(counter_font, counter_size),
    fill="white"
)

if counter_color != "rgb":
    canvas.itemconfig(
        counter,
        fill=counter_color
    )

else:
    titlecolors = []
    for i in range(360):
        h = i / 360.0
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        titlecolors.append('#{0:02X}{1:02X}{2:02X}'.format(
            int(r * 255), int(g * 255), int(b * 255)
        ))
    index_color = [0]
    def update_color_titel():
        global title_animation_id
        color = titlecolors[index_color[0]]
        canvas.itemconfig(counter, fill=color)
        index_color[0] = (index_color[0] + 1) % len(titlecolors)
        title_animation_id = corn.after(16, update_color_titel)
    update_color_titel()


def add_counter():
    counter_default_value = ConfigManager().load_from_config(config_name="config.json", name_in_config="counter_default_value")
    counter_current_value = counter_default_value + 1
    canvas.itemconfig(counter, text= f"{counter_text} {counter_current_value}")
    canvas.update()
    ConfigManager().save_to_config(config_name= "config.json", what_to_save="counter_default_value", status=counter_current_value)

def sub_counter():
    counter_default_value = ConfigManager().load_from_config(config_name="config.json", name_in_config="counter_default_value")
    counter_current_value = counter_default_value - 1
    canvas.itemconfig(counter, text= f"{counter_text} {counter_current_value}")
    canvas.update()
    ConfigManager().save_to_config(config_name= "config.json", what_to_save="counter_default_value", status=counter_current_value)

counter_hotkey_positive = counter_hotkey_positive.lower()
counter_hotkey_negative = counter_hotkey_negative.lower()

def on_release(key):
    try:
        if hasattr(key, 'char') and key.char and key.char.lower() == counter_hotkey_positive:
            add_counter()
        if hasattr(key, 'char') and key.char and key.char.lower() == counter_hotkey_negative:
            sub_counter()
    except AttributeError:
        pass


listener = keyboard.Listener(on_release=on_release)
listener.start()

def force_topmost2():
    corn.attributes("-topmost", True)
    corn.after(500, force_topmost2)
corn.after(100, force_topmost2)

corn.mainloop()