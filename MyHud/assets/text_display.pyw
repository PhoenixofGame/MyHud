import colorsys
import tkinter as tk
import win32con
import win32gui
from ConfigManager import ConfigManager
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
# ===========================OVERLAY===========================
UI_Titel = tk.Tk()
UI_Titel.attributes("-topmost", True)
UI_Titel.update()
UI_Titel.attributes("-transparentcolor", "black")  # Transparent background
UI_Titel.overrideredirect(True)# Remove window border


# Make the window click-through
UI_Titel.update()
mainhwnd = win32gui.FindWindow(None, str(UI_Titel.title()))
exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

# fullscreen
screen_width = UI_Titel.winfo_screenwidth()
screen_height = UI_Titel.winfo_screenheight()
UI_Titel.geometry(f"{screen_width}x{screen_height}+0+0")

canvas = tk.Canvas(UI_Titel, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
canvas.pack()

# Title-Objekt erstellen (nur einmal!)
Title = canvas.create_text(
    screen_width // 2,
    50,  # FIXIERT: war (screen_height ** -1) + 50
    text="",
    font=("Comic Sans MS", 15, "italic"),
    fill="white"
)

# Konfiguration laden
current_title = ConfigManager().load_from_config(config_name= "config.json", name_in_config= "CurrentTitle")
title_color = ConfigManager().load_from_config(config_name="config.json", name_in_config="TitleColor")
titel_grose = ConfigManager().load_from_config(config_name="config.json", name_in_config="TitelGrose")

# Normale Farbe
if title_color != "rgb":
    canvas.itemconfig(
        Title,
        text=current_title,
        font=("Comic Sans MS", titel_grose, "italic"),
        fill=title_color
    )
# RGB-Animation
else:
    # Farbpalette erstellen
    titlecolors = []
    for i in range(360):
        h = i / 360.0
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        titlecolors.append('#{0:02X}{1:02X}{2:02X}'.format(
            int(r * 255), int(g * 255), int(b * 255)
        ))
    # Index als Liste für Closure
    index_color = [0]
    def update_color_titel():
        global title_animation_id
        color = titlecolors[index_color[0]]
        canvas.itemconfig(Title, fill=color)
        index_color[0] = (index_color[0] + 1) % len(titlecolors)
        title_animation_id = UI_Titel.after(16, update_color_titel)
    # Text und Font setzen (ohne Farbe, die kommt von der Animation)
    canvas.itemconfig(
        Title,
        text=current_title,
        font=("Comic Sans MS", titel_grose, "italic")
    )
    update_color_titel()

def force_topmost2():
    UI_Titel.attributes("-topmost", True)
    UI_Titel.after(500, force_topmost2)
UI_Titel.after(100, force_topmost2)

UI_Titel.mainloop()
