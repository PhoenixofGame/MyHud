import tkinter as tk
import os
import sys
import win32con
import win32gui
from AnimatedGif import AnimatedGIF
import json


class GifOverlay:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.animated_gifs = []

        os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

        # ===========================OVERLAY===========================
        self.UI_Gif = tk.Tk()
        self.UI_Gif.attributes("-topmost", True)
        self.UI_Gif.attributes("-transparentcolor", "black")
        self.UI_Gif.overrideredirect(True)

        # Make the window click-through
        self.UI_Gif.update()
        mainhwnd = win32gui.FindWindow(None, str(self.UI_Gif.title()))
        exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
        exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

        # fullscreen
        screen_width = self.UI_Gif.winfo_screenwidth()
        screen_height = self.UI_Gif.winfo_screenheight()
        self.UI_Gif.geometry(f"{screen_width}x{screen_height}+0+0")

        self.canvas = tk.Canvas(
            self.UI_Gif,
            width=screen_width,
            height=screen_height,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack()

        self.load_and_create_gifs()

        def force_topmost2():
            self.UI_Gif.attributes("-topmost", True)
            self.UI_Gif.after(500, force_topmost2)

        self.UI_Gif.after(100, force_topmost2)

    def load_and_create_gifs(self):
        """Lädt alle aktivierten GIFs aus der Config und erstellt sie"""
        # Alte GIFs stoppen
        for gif in self.animated_gifs:
            try:
                gif.stop()
            except:
                pass
        self.animated_gifs.clear()

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)

            for gif_name, config in settings_data.items():
                if config.get("enabled", False):
                    gif_file_name = f"Your_Gifs/{gif_name}"

                    if os.path.exists(gif_file_name):
                        try:
                            animated_gif = AnimatedGIF(
                                self.canvas,
                                gif_file_name,
                                config.get("x", 0),
                                config.get("y", 0),
                                width=config.get("width", 200),
                                height=config.get("height", 200)
                            )
                            animated_gif.start()
                            self.animated_gifs.append(animated_gif)
                        except Exception as e:
                            pass

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def reload_gifs(self):
        """Lädt die GIFs neu (für externe Aufrufe)"""
        self.load_and_create_gifs()

    def start(self):
        self.UI_Gif.mainloop()


# Verwendung
if __name__ == "__main__":
    overlay = GifOverlay("gif_config.json")
    overlay.start()