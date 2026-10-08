import random
import tkinter as tk
import colorsys
import time
import os
import psutil
import win32con
import win32gui
import win32process

try:
    from assets.Config_Manager import ConfigManager
except ImportError:
    from Config_Manager import ConfigManager

cm = ConfigManager()



class Main_Overlay:
    def __init__(self, config_file: str, master):
        self.running = False
        self.config_file = config_file


        self.main = tk.Toplevel(master)
        self.main.attributes("-topmost", True)
        self.main.attributes("-transparentcolor", "black")  # noqa
        self.main.overrideredirect(True)

        self.main.update()
        mainhwnd = win32gui.FindWindow(None, str(self.main.title())) # noqa
        exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
        exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()
        self.main.geometry(f"{screen_width}x{screen_height}+0+0")

        canvas = tk.Canvas(self.main, width=screen_width, height=screen_height, bg="black", highlightthickness=0)
        canvas.pack()

        main_overlay_motivation_color = cm.load_from_config(config_name="config.json", name_in_config="main_overlay_motivation_color", default= "rgb")
        main_overlay_motivation_size = cm.load_from_config(config_name="config.json", name_in_config="main_overlay_motivation_size", default= 15)
        main_overlay_clock_color = cm.load_from_config(config_name="config.json", name_in_config="main_overlay_clock_color", default= "white")
        main_overlay_clock_size = cm.load_from_config(config_name="config.json", name_in_config="main_overlay_clock_size", default= 15)
        main_overlay_spotify_color = cm.load_from_config(config_name="config.json", name_in_config="main_overlay_spotify_color", default= "white")
        main_overlay_spotify_size = cm.load_from_config(config_name="config.json", name_in_config="main_overlay_spotify_size", default= 15)

        try:
            config_path = os.path.join('Your_Motivation_Text/motivation.txt')
            with open(config_path, 'r', encoding='utf-8') as f:
                motivation = [
                    line.strip()
                    for line in f
                    if line.strip()
                ]

        except FileNotFoundError:
            motivation = ["stay motivated", "CoFfEEee", "I wanna Sleep"]

        SPACING = -5

        def update_spruch():
            try:
                motivations_spruch = random.choice(motivation)
            except IndexError:
                motivations_spruch = ""
            canvas.itemconfig(mot_id, text=motivations_spruch)
            self.main.after(300000, update_spruch) # noqa


        txcolor = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            txcolor.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r*255), int(g*255), int(b*255)
            ))

        self.index = 0
        def update_color():
            TextColor = txcolor[self.index]
            canvas.itemconfig(mot_id, fill=TextColor)
            self.index = (self.index + 1) % len(txcolor)
            self.main.after(16, update_color) # noqa


        mot_y = 10
        mot_id = canvas.create_text(
            screen_width - 10,
            mot_y,
            text="",
            anchor="ne",
            fill="#00ff9d",
            font=("Comic Sans MS", main_overlay_motivation_size, "bold italic")
        )
        update_spruch()

        if main_overlay_motivation_color == "rgb":
            update_color()
        else:
            canvas.itemconfig(mot_id, fill=main_overlay_motivation_color)

        #Uhr
        def update_clock():
            aktuelle_zeit = time.strftime("%H:%M:%S")
            canvas.itemconfig(uhr_id, text=aktuelle_zeit)
            self.main.after(1000, update_clock) # noqa

        def update_color2():
            TextColor = txcolor[self.index]
            canvas.itemconfig(uhr_id, fill=TextColor)
            self.index = (self.index + 1) % len(txcolor)
            self.main.after(16, update_color2) # noqa

        mot_bbox = canvas.bbox(mot_id)
        mot_height = mot_bbox[3] - mot_bbox[1] if mot_bbox else main_overlay_motivation_size

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

        # spotify
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
            self.main.after(2000, update_spotify_text) # noqa

        def update_color3():
            TextColor = txcolor[self.index]
            canvas.itemconfig(spotify_id, fill=TextColor)
            self.index = (self.index + 1) % len(txcolor)
            self.main.after(16, update_color3) # noqa

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
            self.main.attributes("-topmost", True)
            self.main.after(500, force_topmost2) # noqa
        self.main.after(100, force_topmost2) # noqa

    def start_main_overlay(self):
        self.running = True

        def force_topmost2():
            self.main.attributes("-topmost", True)
            self.main.after(500, force_topmost2) # noqa
        self.main.after(100, force_topmost2) # noqa

    def destroy_main(self):
        self.main.destroy()

    def stop_main_overlay(self):
        self.running = False
        self.main.after(0, self.destroy_main) # noqa

