import tkinter as tk
import win32con
import win32gui
from pynput import keyboard, mouse

try:
    from assets.Config_Manager import ConfigManager
except ImportError:
    from Config_Manager import ConfigManager

cm = ConfigManager()


class Keys:
    def __init__(self, hotkey, location, canvas, key_text_color, key_color_pressed, key_text_font, key_text_size, key_outline_color, key_default_color):
        x = location[0]
        y = location[1]
        width = location[2]
        height = location[3]

        center_x = (x + width) / 2
        center_y = (y + height) / 2

        self.listener = None

        self.button = canvas.create_rectangle(x, y, width, height, fill=key_default_color, outline=key_outline_color)
        self.text = canvas.create_text(center_x, center_y, text=hotkey.upper(), font=(key_text_font, key_text_size), fill=key_text_color)

        self.hotkey = hotkey.lower()
        self.is_mouse = hotkey.lower() in ["lmb", "rmb", "mmb"]

        if self.is_mouse:
            # Mouse Listener
            def on_click(_x, _y, button, pressed):
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

            self.listener = mouse.Listener(on_click=on_click)  # noqa
            self.listener.daemon = True
            self.listener.start()

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

            self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            self.listener.daemon = True
            self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()

class Key_Overlay:
    def __init__(self, config_file: str, master):
        self.running = False
        self.config_file = config_file

        self.button = None
        self.text = None
        self.hotkey = None
        self.is_mouse = None

        self.keys = []

        self.main = tk.Toplevel(master)

        key_x_location = cm.load_from_config("config.json", "key_x_location", default= 1920 - 180)
        key_y_location = cm.load_from_config("config.json", "key_y_location", default= 10)

        self.key_text_color = cm.load_from_config("config.json", "key_text_color", default= "white")
        self.key_color_pressed = cm.load_from_config("config.json", "key_color_pressed", default= "red")
        self.key_text_font = cm.load_from_config("config.json", "key_text_font", default= "Sitka")
        self.key_text_size = cm.load_from_config("config.json", "key_text_size", default= 15)
        self.key_outline_color = cm.load_from_config("config.json", "key_outline_color", default= "black")
        self.key_default_color = cm.load_from_config("config.json", "key_default_color", default= "black")

        self.main.attributes("-topmost", True)
        self.main.attributes("-transparentcolor", "#000001") # noqa
        self.main.configure(background="#000001")
        self.main.overrideredirect(True)

        self.main.update()
        mainhwnd = win32gui.FindWindow(None, str(self.main.title())) # noqa
        exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
        exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()
        self.main.geometry(f"{screen_width}x{screen_height}+0+0")

        self.canvas = tk.Canvas(self.main, width=170, height=170, bg="#000001", highlightthickness=0)
        self.canvas.place(x=key_x_location, y=key_y_location)

    def start_key_overlay(self):
        self.running = True

        self.keys.append(Keys("w", (60, 0, 110, 50), canvas=self.canvas, key_text_color=self.key_text_color, key_color_pressed=self.key_color_pressed, key_text_font=self.key_text_font, key_text_size=self.key_text_size, key_outline_color=self.key_outline_color, key_default_color=self.key_default_color))
        self.keys.append(Keys("s", (60, 60, 110, 110), canvas=self.canvas, key_text_color=self.key_text_color, key_color_pressed=self.key_color_pressed, key_text_font=self.key_text_font, key_text_size=self.key_text_size, key_outline_color=self.key_outline_color, key_default_color=self.key_default_color))
        self.keys.append(Keys("d", (120, 60, 170, 110), canvas=self.canvas, key_text_color=self.key_text_color, key_color_pressed=self.key_color_pressed, key_text_font=self.key_text_font, key_text_size=self.key_text_size, key_outline_color=self.key_outline_color, key_default_color=self.key_default_color))
        self.keys.append(Keys("a", (0, 60, 50, 110), canvas=self.canvas, key_text_color=self.key_text_color, key_color_pressed=self.key_color_pressed, key_text_font=self.key_text_font, key_text_size=self.key_text_size, key_outline_color=self.key_outline_color, key_default_color=self.key_default_color))
        self.keys.append(Keys("lmb", (0, 0, 50, 50), canvas=self.canvas, key_text_color=self.key_text_color, key_color_pressed=self.key_color_pressed, key_text_font=self.key_text_font, key_text_size=self.key_text_size, key_outline_color=self.key_outline_color, key_default_color=self.key_default_color))
        self.keys.append(Keys("rmb", (120, 0, 170, 50), canvas=self.canvas, key_text_color=self.key_text_color, key_color_pressed=self.key_color_pressed, key_text_font=self.key_text_font, key_text_size=self.key_text_size, key_outline_color=self.key_outline_color, key_default_color=self.key_default_color))
        self.keys.append(Keys("space", (0, 120, 170, 170), canvas=self.canvas, key_text_color=self.key_text_color, key_color_pressed=self.key_color_pressed, key_text_font=self.key_text_font, key_text_size=self.key_text_size, key_outline_color=self.key_outline_color, key_default_color=self.key_default_color))

        def force_topmost():
            self.main.attributes("-topmost", True)
            self.main.after(500, force_topmost) # noqa
        self.main.after(100, force_topmost) # noqa

    def destroy_main(self):
        self.main.destroy()

    def stop_key_overlay(self):
        self.running = False
        for k in getattr(self, "keys", []):
            k.stop()
        self.main.after(0, self.destroy_main)
