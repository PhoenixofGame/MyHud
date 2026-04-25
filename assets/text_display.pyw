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
UI_Titel.attributes("-transparentcolor", "black")  # noqa
UI_Titel.overrideredirect(True)


# Make the window click-through
UI_Titel.update()
mainhwnd = win32gui.FindWindow(None, str(UI_Titel.title())) # noqa
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
title_default_text = ConfigManager().load_from_config(config_name= "config.json", name_in_config= "title_default_text")
title_color = ConfigManager().load_from_config(config_name="config.json", name_in_config="title_color")
title_size = ConfigManager().load_from_config(config_name="config.json", name_in_config="title_size")

# Normale Farbe
if title_color != "rgb":
    canvas.itemconfig(
        Title,
        text=title_default_text,
        font=("Comic Sans MS", title_size, "italic"),
        fill=title_color
    )
# RGB-Animation
else:
    # Farbpalette erstellen
    title_colors = []
    for i in range(360):
        h = i / 360.0
        r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
        title_colors.append('#{0:02X}{1:02X}{2:02X}'.format(
            int(r * 255), int(g * 255), int(b * 255)
        ))
    # Index als Liste für Closure
    index_color = [0]
    def update_color_titel():
        color = title_colors[index_color[0]] # noqa
        canvas.itemconfig(Title, fill=color)
        index_color[0] = (index_color[0] + 1) % len(title_colors)
        title_animation_id = UI_Titel.after(16, update_color_titel) # noqa
    # Text und Font setzen (ohne Farbe, die kommt von der Animation)
    canvas.itemconfig(
        Title,
        text=title_default_text,
        font=("Comic Sans MS", title_size, "italic")
    )
    update_color_titel()

def force_topmost2():
    UI_Titel.attributes("-topmost", True)
    UI_Titel.after(500, force_topmost2) # noqa
UI_Titel.after(100, force_topmost2) # noqa

UI_Titel.mainloop()
