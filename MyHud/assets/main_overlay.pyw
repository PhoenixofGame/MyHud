import random
import tkinter as tk
import colorsys
import time
import sys
import os
import psutil
import win32con
import win32gui
import win32process
from ConfigManager import ConfigManager
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))


UI = tk.Tk()
UI.attributes("-topmost", True)
UI.attributes("-transparentcolor", "black")  # Transparent background
UI.overrideredirect(True)# Remove window border


# Make the window click-through
UI.update()
mainhwnd = win32gui.FindWindow(None, str(UI.title()))
exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

# fullscreen
screen_width = UI.winfo_screenwidth()
screen_height = UI.winfo_screenheight()
UI.geometry(f"{screen_width}x{screen_height}+0+0")

canvas = tk.Canvas(UI, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
canvas.pack()

###############################################################################################################
######################################      Config Laden       ################################################
###############################################################################################################
try:
    main_overlay_motv_color = ConfigManager().load_from_config(config_name="config.json", name_in_config="main_overlay_motv_color")
    main_overlay_motv_size = ConfigManager().load_from_config(config_name="config.json", name_in_config="main_overlay_motv_size")
    main_overlay_clock_color = ConfigManager().load_from_config(config_name="config.json", name_in_config="main_overlay_clock_color")
    main_overlay_clock_size = ConfigManager().load_from_config(config_name="config.json", name_in_config="main_overlay_clock_size")
    main_overlay_spotify_color = ConfigManager().load_from_config(config_name="config.json", name_in_config="main_overlay_spotify_color")
    main_overlay_spotify_size = ConfigManager().load_from_config(config_name="config.json", name_in_config="main_overlay_spotify_size")

except ValueError:
    print("Value Error")
    main_overlay_motv_color = "rgb"
    main_overlay_motv_size = 15
    main_overlay_clock_color = "white"
    main_overlay_clock_size = 15
    main_overlay_spotify_color = "white"
    main_overlay_spotify_size = 15

###############################################################################################################
######################################   Motivation anzeige    ################################################
###############################################################################################################
# Konstanter Abstand zwischen den Elementen
SPACING = -5
start_y = 10


try:
    config_path = os.path.join('Your_Motivation_Text/motivation.txt')
    with open(config_path, 'r', encoding='utf-8') as f:
        motivation = [
            line.strip()
            for line in f
            if line.strip()
        ]

except FileNotFoundError:
    motivation = ["stay motivated", "CoFfEEee", "I wanna Sleep", "RAU ON TOP"]


def update_spruch():
    try:
        Motvspruch = random.choice(motivation)
    except IndexError:
        Motvspruch = ""
    canvas.itemconfig(mot_id, text=Motvspruch)
    UI.after(300000, update_spruch)


txcolor = []
for i in range(360):
    h = i / 360.0
    r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
    txcolor.append('#{0:02X}{1:02X}{2:02X}'.format(
        int(r*255), int(g*255), int(b*255)
    ))
index = 0
def update_color():
    global index
    TextColor = txcolor[index]
    canvas.itemconfig(mot_id, fill=TextColor)
    index = (index + 1) % len(txcolor)
    UI.after(16, update_color)


mot_y = start_y
mot_id = canvas.create_text(
    screen_width - 10,
    mot_y,
    text="",
    anchor="ne",
    fill="#00ff9d",
    font=("Comic Sans MS", main_overlay_motv_size, "bold italic")
)
update_spruch()

if main_overlay_motv_color == "rgb":
    update_color()
else:
    canvas.itemconfig(mot_id, fill=main_overlay_motv_color)


###############################################################################################################
######################################   Uhr anzeige    #######################################################
###############################################################################################################
def update_clock():
    aktuelle_zeit = time.strftime("%H:%M:%S")
    canvas.itemconfig(uhr_id, text=aktuelle_zeit)
    UI.after(1000, update_clock)

def update_color2():
    global index
    TextColor = txcolor[index]
    canvas.itemconfig(uhr_id, fill=TextColor)
    index = (index + 1) % len(txcolor)
    UI.after(16, update_color2)

mot_bbox = canvas.bbox(mot_id)
mot_height = mot_bbox[3] - mot_bbox[1] if mot_bbox else main_overlay_motv_size

uhr_y = mot_y + mot_height + SPACING
uhr_id = canvas.create_text(
    screen_width - 10,
    uhr_y,
    text="--:--:--",
    font=("Comic Sans MS", main_overlay_clock_size, "italic"),
    fill="white",
    anchor="ne"
)
update_clock()

if main_overlay_clock_color == "rgb":
    update_color2()
else:
    canvas.itemconfig(uhr_id, fill=main_overlay_clock_color)
###############################################################################################################
######################################   Spotify anzeige    ###################################################
###############################################################################################################
def get_spotify_song():
    spotify_pids = [p.pid for p in psutil.process_iter(['name']) if p.info['name'] == 'Spotify.exe']
    if not spotify_pids:
        return ""

    def enum_windows_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            if pid in spotify_pids:
                title = win32gui.GetWindowText(hwnd)
                if title.strip():
                    results.append(title)

    results = []
    win32gui.EnumWindows(enum_windows_callback, results)

    return results[0] if results else ""

def update_spotify_text():
    song = get_spotify_song()
    if song == "Spotify Free" or song == "Spotify Premium":
        canvas.itemconfig(spotify_id, text="")
    else:
        canvas.itemconfig(spotify_id, text=song)

    UI.after(2000, update_spotify_text)

def update_color3():
    global index
    TextColor = txcolor[index]
    canvas.itemconfig(spotify_id, fill=TextColor)
    index = (index + 1) % len(txcolor)
    UI.after(16, update_color3)

uhr_bbox = canvas.bbox(uhr_id)
uhr_height = uhr_bbox[3] - uhr_bbox[1] if uhr_bbox else main_overlay_clock_size

spotify_y = uhr_y + uhr_height + SPACING
spotify_id = canvas.create_text(
    screen_width - 10,
    spotify_y,
    text="",
    font=("Comic Sans MS", main_overlay_spotify_size, "italic"),
    fill="white",
    anchor="ne"
)
update_spotify_text()

if main_overlay_spotify_color == "rgb":
    update_color3()
else:
    canvas.itemconfig(spotify_id, fill=main_overlay_spotify_color)

# ende
def force_topmost2():
    UI.attributes("-topmost", True)
    UI.after(500, force_topmost2)
UI.after(100, force_topmost2)



UI.mainloop()
