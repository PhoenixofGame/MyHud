import tkinter as tk
import win32con
import win32gui
from pynput import keyboard, mouse
import os
import sys
from ConfigManager import ConfigManager

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# VARIABLEN
try:
    key_text_color = ConfigManager().load_from_config("config.json", "key_text_color")
    key_color_pressed = ConfigManager().load_from_config("config.json", "key_color_pressed")
    key_x_location = ConfigManager().load_from_config("config.json", "key_x_location")
    key_y_location = ConfigManager().load_from_config("config.json", "key_y_location")
    key_text_font = ConfigManager().load_from_config("config.json", "key_text_font")
    key_text_size = ConfigManager().load_from_config("config.json", "key_text_size")
    key_outline_color = ConfigManager().load_from_config("config.json", "key_outline_color")
    key_default_color = ConfigManager().load_from_config("config.json", "key_default_color")
except FileNotFoundError:
    print("Config File Not Found")
    key_default_color = "white"
    key_color_pressed = "red"
    key_x_location = 1920 - 180
    key_y_location = 10
    key_text_font = "Comic Sans MS"
    key_text_size = 20
    key_outline_color = "black"
    key_text_color = "black"

main = tk.Tk()
main.attributes("-topmost", True)
main.attributes("-transparentcolor", "#000001") # noqa
main.configure(background="#000001")
main.overrideredirect(True)

# Make the window click-through
main.update()
mainhwnd = win32gui.FindWindow(None, str(main.title())) # noqa
exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

# fullscreen
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
main.geometry(f"{screen_width}x{screen_height}+0+0")

canvas = tk.Canvas(main, width=170, height=170, bg="#000001", highlightthickness=0)
canvas.place(x=key_x_location, y=key_y_location)


class Keys:
    def __init__(self, hotkey, location):
        x = location[0]
        y = location[1]
        width = location[2]
        height = location[3]

        center_x = (x + width) / 2
        center_y = (y + height) / 2

        self.button = canvas.create_rectangle(x, y, width, height, fill=key_default_color, outline=key_outline_color)
        self.text = canvas.create_text(center_x, center_y, text=hotkey.upper(), font=(key_text_font, key_text_size), fill=key_text_color)

        self.hotkey = hotkey.lower()
        self.is_mouse = hotkey.lower() in ["lmb", "rmb", "mmb"]

        if self.is_mouse:
            # Mouse Listener
            def on_click(button, pressed):
                button_map = {
                    "lmb": mouse.Button.left,
                    "rmb": mouse.Button.right,
                    "mmb": mouse.Button.middle
                }

                if self.hotkey in button_map and button == button_map[self.hotkey]:
                    if pressed:
                        canvas.itemconfig(self.button, fill=key_color_pressed)
                    else:
                        canvas.itemconfig(self.button, fill=key_default_color)

            listener = mouse.Listener(on_click=on_click) # noqa
            listener.start()
        else:
            # Keyboard Listener
            def on_press(key):
                try:
                    if hasattr(key, 'char') and key.char and key.char.lower() == self.hotkey:
                        canvas.itemconfig(self.button, fill=key_color_pressed)

                    elif key == keyboard.Key.space and self.hotkey == "space":
                        canvas.itemconfig(self.button, fill=key_color_pressed)
                except AttributeError:
                    pass

            def on_release(key):
                try:
                    if hasattr(key, 'char') and key.char and key.char.lower() == self.hotkey:
                        canvas.itemconfig(self.button, fill=key_default_color)
                    elif key == keyboard.Key.space and self.hotkey == "space":
                        canvas.itemconfig(self.button, fill=key_default_color)
                except AttributeError:
                    pass

            listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            listener.start()


Keys("w", (60, 0, 110, 50))
Keys("s", (60, 60, 110, 110))
Keys("d", (120, 60, 170, 110))
Keys("a", (0, 60, 50, 110))
Keys("lmb", (0, 0, 50, 50))
Keys("rmb", (120, 0, 170, 50))
Keys("space", (0, 120, 170, 170))


def force_topmost():
    main.attributes("-topmost", True)
    main.after(500, force_topmost) # noqa
main.after(100, force_topmost) # noqa

main.mainloop()