import tkinter as tk
import os
import sys
import win32con
import win32gui
from AnimatedGif import AnimatedGIF
from ConfigManager import ConfigManager

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# ===========================OVERLAY===========================
UI_Gif = tk.Tk()
UI_Gif.attributes("-topmost", True)
UI_Gif.attributes("-transparentcolor", "black")  # Transparent background
UI_Gif.overrideredirect(True)# Remove window border


# Make the window click-through
UI_Gif.update()
mainhwnd = win32gui.FindWindow(None, str(UI_Gif.title()))
exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

# fullscreen
screen_width = UI_Gif.winfo_screenwidth()
screen_height = UI_Gif.winfo_screenheight()
UI_Gif.geometry(f"{screen_width}x{screen_height}+0+0")

canvas = tk.Canvas(UI_Gif, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
canvas.pack()

GIFFileName = ConfigManager().load_from_config(config_name= "config.json", name_in_config="GIFFileName")
GIFXLOCATION = ConfigManager().load_from_config(config_name= "config.json", name_in_config="GIFXLOCATION")
GIFYLOCATION = ConfigManager().load_from_config(config_name= "config.json", name_in_config="GIFYLOCATION")
GIFwidth = ConfigManager().load_from_config(config_name= "config.json", name_in_config="GIFwidth")
GIFheight = ConfigManager().load_from_config(config_name= "config.json", name_in_config="GIFheight")

gif_file_name = "Your_Gifs/" + GIFFileName

animated_gif = AnimatedGIF(canvas, gif_file_name, GIFXLOCATION, GIFYLOCATION, width= GIFwidth, height= GIFheight)
animated_gif.start()

def force_topmost2():
    UI_Gif.attributes("-topmost", True)
    UI_Gif.after(500, force_topmost2)
UI_Gif.after(100, force_topmost2)

UI_Gif.mainloop()

