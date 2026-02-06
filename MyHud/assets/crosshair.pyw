import tkinter as tk
import win32gui
import win32con
import colorsys
import os
import sys

from ConfigManager import ConfigManager

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

try:
    dot_color = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="dot_color")
    dot_outline = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="dot_outline")
    dot_size = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="dot_size")
    rectangle_color = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="rectangle_color")
    rectangle_outline = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="rectangle_outline")
    rectangle_size = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="rectangle_size")
    x_color = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="x_color")
    x_size = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="x_size")
    x_gap = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="x_gap")
    x_width = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="x_width")
    plus_color = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="plus_color")
    plus_size = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="plus_size")
    plus_gap = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="plus_gap")
    plus_width = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="plus_width")
    triangle_color = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="triangle_color")
    triangle_size = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="triangle_size")
    triangle_width = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="triangle_width")
    dot_activation = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="dot_activation")
    rectangle_activation = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="rectangle_activation")
    plus_activation = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="plus_activation")
    x_activation = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="x_activation")
    triangle_activation = ConfigManager().load_from_config(config_name="crosshair_config.json", name_in_config="triangle_activation")

except ValueError:
    print("Value Error")
    dot_color = "white"
    dot_outline = "blue"
    dot_size = 2.5
    rectangle_color = "white"
    rectangle_outline = "black"
    rectangle_size = 2.5
    x_color = "blue"
    x_size = 2.5
    x_gap = 2.5
    x_width = 2.0
    plus_color = "white"
    plus_size = 2.5
    plus_gap = 2.5
    plus_width = 2.0
    triangle_color = "white"
    triangle_size = 2.5
    triangle_width = 5.0
    dot_activation = False
    rectangle_activation = False
    plus_activation = False
    x_activation = False
    triangle_activation = False

except FileNotFoundError:
    print("Config Not Found Error")
    dot_color = "white"
    dot_outline = "blue"
    dot_size = 2.5
    rectangle_color = "white"
    rectangle_outline = "black"
    rectangle_size = 2.5
    x_color = "blue"
    x_size = 2.5
    x_gap = 2.5
    x_width = 2.0
    plus_color = "white"
    plus_size = 2.5
    plus_gap = 2.5
    plus_width = 2.0
    triangle_color = "white"
    triangle_size = 2.5
    triangle_width = 5.0
    dot_activation = False
    rectangle_activation = False
    plus_activation = False
    x_activation = False
    triangle_activation = False

    backup_data = {
        "dot_color": "white",
        "dot_outline": "blue",
        "dot_size": 2.5,
        "rectangle_color": "white",
        "rectangle_outline": "black",
        "rectangle_size": 2.5,
        "x_color": "blue",
        "x_size": 2.5,
        "x_gap": 2.5,
        "x_width": 2.0,
        "plus_color": "white",
        "plus_size": 2.5,
        "plus_gap": 2.5,
        "plus_width": 2.0,
        "triangle_color": "white",
        "triangle_size": 2.5,
        "triangle_width": 5.0,
        "dot_activation": False,
        "rectangle_activation": False,
        "plus_activation": False,
        "x_activation": False,
        "triangle_activation": False
    }
    ConfigManager().create_and_save(data= backup_data, config_name= "crosshair_config.json")

toast = tk.Tk()
toast.title("CrosshairOverlay")
toast.attributes("-topmost", True)
toast.update()

toast.attributes("-transparentcolor", "#000001")  # Transparent background
toast.overrideredirect(True)  # Remove window border

# Make the window click-through
toast.update()
mainhwnd = win32gui.FindWindow(None, str(toast.title()))
exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

# fullscreen
screen_width = toast.winfo_screenwidth()
screen_height = toast.winfo_screenheight()
toast.geometry(f"{screen_width}x{screen_height}+0+0")

canvas = tk.Canvas(toast, width=screen_width, height=screen_height, bg="#000001", highlightthickness=0,)
canvas.pack()

class Crosshair:
    def __init__(self):
        # RGB-Farbpalette einmal erstellen
        self.rgb_colors = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            self.rgb_colors.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))

    def create_dot(self, main_color, outline_color, size):
        # Bestimme Anfangsfarben
        initial_fill = "white" if main_color == "rgb" else main_color
        initial_outline = "white" if outline_color == "rgb" else outline_color

        # Erstelle den Dot
        simpel_dot = canvas.create_oval(
            screen_width // 2 - size,
            screen_height // 2 - size,
            screen_width // 2 + size,
            screen_height // 2 + size,
            fill=initial_fill,
            outline=initial_outline
        )

        # Nur wenn RGB benötigt wird, starte Animation
        if main_color == "rgb" or outline_color == "rgb":
            index_dot = 0

            def update_color_dot():
                nonlocal index_dot
                color = self.rgb_colors[index_dot]

                if main_color == "rgb":
                    canvas.itemconfig(simpel_dot, fill=color)
                if outline_color == "rgb":
                    canvas.itemconfig(simpel_dot, outline=color)

                index_dot = (index_dot + 1) % len(self.rgb_colors)
                toast.after(16, update_color_dot)

            update_color_dot()

    def create_rectangle(self, main_color, outline_color, size):
        initial_fill = "white" if main_color == "rgb" else main_color
        initial_outline = "white" if outline_color == "rgb" else outline_color

        simple_rectangle = canvas.create_rectangle(
            screen_width//2 - size,
            screen_height//2 - size,
            screen_width//2 + size,
            screen_height//2 + size,
            fill=initial_fill, outline=initial_outline
        )

        if main_color == "rgb" or outline_color == "rgb":
            index_dot = 0

            def update_color_dot():
                nonlocal index_dot
                color = self.rgb_colors[index_dot]

                if main_color == "rgb":
                    canvas.itemconfig(simple_rectangle, fill=color)
                if outline_color == "rgb":
                    canvas.itemconfig(simple_rectangle, outline=color)

                index_dot = (index_dot + 1) % len(self.rgb_colors)
                toast.after(16, update_color_dot)

            update_color_dot()


    def create_x(self, main_color, size, gap_size, width):
        initial_fill = "white" if main_color == "rgb" else main_color

        combine = size + gap_size
        # X crs
        x_lines = [
            canvas.create_line(screen_width//2 + gap_size, screen_height//2 + gap_size, screen_width//2 + combine, screen_height//2 + combine, fill=initial_fill, width=width), # RECHTS HOCH
            canvas.create_line(screen_width//2 - gap_size, screen_height//2 + gap_size, screen_width//2 - combine, screen_height//2 + combine, fill=initial_fill, width=width), # LINKS HOCH
            canvas.create_line(screen_width//2 + gap_size, screen_height//2 - gap_size, screen_width//2 + combine, screen_height//2 - combine, fill=initial_fill ,width=width), # RECHTS RUNTER
            canvas.create_line(screen_width//2 - gap_size, screen_height//2 - gap_size, screen_width//2 - combine, screen_height//2 - combine, fill=initial_fill ,width=width) # LINKS RUNTER
        ]

        if main_color == "rgb":
            index_dot = 0

            def update_color():
                nonlocal index_dot
                color = self.rgb_colors[index_dot]

                # Alle Linien auf einmal updaten
                for line in x_lines:
                    canvas.itemconfig(line, fill=color)

                index_dot = (index_dot + 1) % len(self.rgb_colors)
                toast.after(16, update_color)

            update_color()

    def create_plus(self, main_color, size, gap_size, width):
        initial_fill = "white" if main_color == "rgb" else main_color

        combine = size + gap_size

        #plus
        plus_lines = [
            canvas.create_line(screen_width//2 - gap_size, screen_height//2, screen_width//2 - combine, screen_height//2, fill=initial_fill, width=width), # links
            canvas.create_line(screen_width//2, screen_height//2 - gap_size, screen_width//2, screen_height//2 - combine, fill=initial_fill, width=width), # runter
            canvas.create_line(screen_width//2 + gap_size, screen_height//2, screen_width//2 + combine, screen_height//2, fill=initial_fill, width=width), # rechts
            canvas.create_line(screen_width//2, screen_height//2 + gap_size, screen_width//2, screen_height//2 + combine, fill=initial_fill, width=width) # hoch
        ]

        if main_color == "rgb":
            index_dot = 0

            def update_color():
                nonlocal index_dot
                color = self.rgb_colors[index_dot]

                # Alle Linien auf einmal updaten
                for line in plus_lines:
                    canvas.itemconfig(line, fill=color)

                index_dot = (index_dot + 1) % len(self.rgb_colors)
                toast.after(16, update_color)

            update_color()

    def create_drei(self, main_color, size, width):
        initial_fill = "white" if main_color == "rgb" else main_color

        #drei_eck
        simple_triangle = canvas.create_line(
                            screen_width//2 + size, screen_height//2 + size, #linke ecke
                            screen_width//2 - size, screen_height//2 + size, # rechte ecke
                            screen_width//2, screen_height//2, #spitze
                            screen_width//2 + size, screen_height//2 + size, # linke ecke
                            width=width, fill=initial_fill
        )

        if main_color == "rgb":
            index_dot = 0

            def update_color_dot():
                nonlocal index_dot
                color = self.rgb_colors[index_dot]

                canvas.itemconfig(simple_triangle, fill=color)

                index_dot = (index_dot + 1) % len(self.rgb_colors)
                toast.after(16, update_color_dot)

            update_color_dot()


if dot_activation == True:
    Crosshair().create_dot(main_color=dot_color, outline_color=dot_outline, size=dot_size)

if rectangle_activation == True:
    Crosshair().create_rectangle(main_color=rectangle_color, outline_color=rectangle_outline, size=rectangle_size)

if x_activation == True:
    Crosshair().create_x(main_color=x_color, size=x_size, gap_size=x_gap, width=x_width)

if plus_activation == True:
    Crosshair().create_plus(main_color=plus_color, size=plus_size, gap_size=plus_gap, width=plus_width)

if triangle_activation == True:
    Crosshair().create_drei(main_color=triangle_color, size=triangle_size, width=triangle_width)


def force_topmost():
    toast.attributes("-topmost", True)
    toast.after(500, force_topmost)
toast.after(100, force_topmost)

toast.mainloop()    