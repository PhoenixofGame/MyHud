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
    COLOR_DEFAULT = ConfigManager().load_from_config("config.json", "COLOR_DEFAULT")
    COLOR_PRESSED = ConfigManager().load_from_config("config.json", "COLOR_PRESSED")
    X_LOCATION = ConfigManager().load_from_config("config.json", "X_LOCATION")
    Y_LOCATION = ConfigManager().load_from_config("config.json", "Y_LOCATION")
    TEXT_FONT = ConfigManager().load_from_config("config.json", "TEXT_FONT")
    TEXT_SIZE = ConfigManager().load_from_config("config.json", "TEXT_SIZE")
    OUTLINE_COLOR = ConfigManager().load_from_config("config.json", "OUTLINE_COLOR")
    TEXT_COLOR = ConfigManager().load_from_config("config.json", "TEXT_COLOR")
except FileNotFoundError:
    print("Config File Not Found")
    COLOR_DEFAULT = "white"
    COLOR_PRESSED = "red"
    X_LOCATION = 1920 - 180
    Y_LOCATION = 10
    TEXT_FONT = "Comic Sans MS"
    TEXT_SIZE = 20
    OUTLINE_COLOR = "black"
    TEXT_COLOR = "black"

main = tk.Tk()
main.attributes("-topmost", True)
main.attributes("-transparentcolor", "#000001")
main.configure(background="#000001")
main.overrideredirect(True)

# Make the window click-through
main.update()
mainhwnd = win32gui.FindWindow(None, str(main.title()))
exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

# fullscreen
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
main.geometry(f"{screen_width}x{screen_height}+0+0")

canvas = tk.Canvas(main, width=170, height=170, bg="#000001", highlightthickness=0)
canvas.place(x=X_LOCATION, y=Y_LOCATION)


class Keys:
    def __init__(self, hotkey, location):
        x = location[0]
        y = location[1]
        width = location[2]
        height = location[3]

        center_x = (x + width) / 2
        center_y = (y + height) / 2

        self.button = canvas.create_rectangle(x, y, width, height, fill=COLOR_DEFAULT, outline=OUTLINE_COLOR)
        self.text = canvas.create_text(center_x, center_y, text=hotkey.upper(), font=(TEXT_FONT, TEXT_SIZE), fill=TEXT_COLOR)

        self.hotkey = hotkey.lower()
        self.is_mouse = hotkey.lower() in ["lmb", "rmb", "mmb"]

        if self.is_mouse:
            # Mouse Listener
            def on_click(x, y, button, pressed):
                button_map = {
                    "lmb": mouse.Button.left,
                    "rmb": mouse.Button.right,
                    "mmb": mouse.Button.middle
                }

                if self.hotkey in button_map and button == button_map[self.hotkey]:
                    if pressed:
                        canvas.itemconfig(self.button, fill=COLOR_PRESSED)
                    else:
                        canvas.itemconfig(self.button, fill=COLOR_DEFAULT)

            listener = mouse.Listener(on_click=on_click)
            listener.start()
        else:
            # Keyboard Listener
            def on_press(key):
                try:
                    if hasattr(key, 'char') and key.char and key.char.lower() == self.hotkey:
                        canvas.itemconfig(self.button, fill=COLOR_PRESSED)

                    elif key == keyboard.Key.space and self.hotkey == "space":
                        canvas.itemconfig(self.button, fill=COLOR_PRESSED)
                except AttributeError:
                    pass

            def on_release(key):
                try:
                    if hasattr(key, 'char') and key.char and key.char.lower() == self.hotkey:
                        canvas.itemconfig(self.button, fill=COLOR_DEFAULT)
                    elif key == keyboard.Key.space and self.hotkey == "space":
                        canvas.itemconfig(self.button, fill=COLOR_DEFAULT)
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
    main.after(500, force_topmost)


main.after(100, force_topmost)

main.mainloop()