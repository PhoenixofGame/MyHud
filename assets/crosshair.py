import tkinter as tk
import win32gui
import win32con
import colorsys
import ctypes

try:
    from assets.Config_Manager import ConfigManager
except ImportError:
    from Config_Manager import ConfigManager

class Crosshair:
    def __init__(self, config_file: str, master):

        self.config_file = config_file
        self.running = None

        ctypes.windll.shcore.SetProcessDpiAwareness(2)

        self.main = tk.Toplevel(master)
        self.main.title("CrosshairOverlay")
        self.main.attributes("-topmost", True)
        self.main.update()

        self.main.attributes("-transparentcolor", "#000001")
        self.main.overrideredirect(True)

        self.main.update()
        mainhwnd = win32gui.FindWindow(None, str(self.main.title()))
        exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE)
        exStyle |= win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(mainhwnd, win32con.GWL_EXSTYLE, exStyle)

        self.screen_width = self.main.winfo_screenwidth()
        self.screen_height = self.main.winfo_screenheight()
        self.main.geometry(f"{self.screen_width}x{self.screen_height}+0+0")

        self.canvas = tk.Canvas(self.main, width=self.screen_width, height=self.screen_height, bg="#000001", highlightthickness=0)
        self.canvas.pack()

        self.rgb_colors = []
        for i in range(360):
            h = i / 360.0
            r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
            self.rgb_colors.append('#{0:02X}{1:02X}{2:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            ))

    def start_crosshair(self):
        dot_activation= self.load_from_config(name_in_config="dot_activation", default=False)
        rectangle_activation = self.load_from_config(name_in_config="rectangle_activation", default=False)
        plus_activation = self.load_from_config(name_in_config="plus_activation", default=True)
        x_activation = self.load_from_config(name_in_config="x_activation", default=False)
        triangle_activation = self.load_from_config(name_in_config="triangle_activation", default=False)

        if dot_activation:
            self.create_dot()

        if rectangle_activation:
            self.create_rectangle()

        if x_activation:
            self.create_x()

        if plus_activation:
            self.create_plus()

        if triangle_activation:
            self.create_drei()

        self.running = True

        def force_topmost():
            if not self.running:
                return
            self.main.attributes("-topmost", True)
            self.main.after(500, force_topmost)

        self.main.after(100, force_topmost)

    def destroy_main(self):
        self.main.destroy()

    def stop_crosshair(self):
        self.running = False
        self.main.after(0, self.destroy_main)

    def load_from_config(self, name_in_config, default):
        return ConfigManager().load_from_config(config_name=self.config_file, name_in_config=name_in_config, default=default)


    def update_color_single(self, local_index, input_form, main_color, outline_color):
        color = self.rgb_colors[local_index]

        if main_color == "rgb":
            self.canvas.itemconfig(input_form, fill=color)
        if outline_color == "rgb":
            self.canvas.itemconfig(input_form, outline=color)

        local_index = (local_index + 1) % len(self.rgb_colors)
        self.main.after(16, self.update_color_single, local_index, input_form, main_color, outline_color)

    def create_dot(self):
        main_color = self.load_from_config(name_in_config="dot_color", default="white")
        size = self.load_from_config(name_in_config="dot_size", default=2.5)

        initial_fill = "white" if main_color == "rgb" else main_color

        size = int(round(size))

        cx = self.screen_width // 2
        cy = self.screen_height // 2

        d = size * 2
        img = tk.PhotoImage(master=self.canvas, width=d, height=d)
        r = size - 0.5
        pixels = [(x, y) for y in range(d) for x in range(d)
                  if (x - r) ** 2 + (y - r) ** 2 <= size ** 2]

        def paint(color):
            for x, y in pixels:
                img.put(color, to=(x, y))

        paint(initial_fill)
        simpel_dot = self.canvas.create_image(cx, cy, image=img, anchor="center")

        self.canvas.tag_raise(simpel_dot)

        self.canvas.dot_img = img

        if main_color == "rgb":
            index_dot = 0

            def update_color_dot():
                nonlocal index_dot
                paint(self.rgb_colors[index_dot])
                index_dot = (index_dot + 1) % len(self.rgb_colors)
                self.main.after(16, update_color_dot)  # noqa

            update_color_dot()

    def create_rectangle(self):
        main_color = self.load_from_config(name_in_config="rectangle_color", default="white")
        outline_color = self.load_from_config(name_in_config="rectangle_outline", default="black")
        size = self.load_from_config(name_in_config="rectangle_size", default=2.5)

        initial_fill = "white" if main_color == "rgb" else main_color
        initial_outline = "white" if outline_color == "rgb" else outline_color

        simple_rectangle = self.canvas.create_rectangle(
            self.screen_width//2 - size,
            self.screen_height//2 - size,
            self.screen_width//2 + size,
            self.screen_height//2 + size,
            fill=initial_fill, outline=initial_outline
        )

        if main_color == "rgb" or outline_color == "rgb":
            start_index = 0
            self.update_color_single(local_index=start_index, input_form=simple_rectangle, main_color=main_color, outline_color=outline_color)

    def create_x(self):
        main_color = self.load_from_config(name_in_config="x_color", default="blue")
        size = self.load_from_config(name_in_config="x_size", default=2.5)
        gap_size = self.load_from_config(name_in_config="x_gap", default=2.5)
        width = self.load_from_config(name_in_config="x_width", default=2.0)

        initial_fill = "white" if main_color == "rgb" else main_color

        combine = size + gap_size
        x_lines = [
            self.canvas.create_line(self.screen_width//2 + gap_size, self.screen_height//2 + gap_size, self.screen_width//2 + combine, self.screen_height//2 + combine, fill=initial_fill, width=width), # RECHTS HOCH
            self.canvas.create_line(self.screen_width//2 - gap_size, self.screen_height//2 + gap_size, self.screen_width//2 - combine, self.screen_height//2 + combine, fill=initial_fill, width=width), # LINKS HOCH
            self.canvas.create_line(self.screen_width//2 + gap_size, self.screen_height//2 - gap_size, self.screen_width//2 + combine, self.screen_height//2 - combine, fill=initial_fill ,width=width), # RECHTS RUNTER
            self.canvas.create_line(self.screen_width//2 - gap_size, self.screen_height//2 - gap_size, self.screen_width//2 - combine, self.screen_height//2 - combine, fill=initial_fill ,width=width) # LINKS RUNTER
        ]

        if main_color == "rgb":
            index_dot = 0
            def update_color():
                nonlocal index_dot
                color = self.rgb_colors[index_dot]
                for line in x_lines:
                    self.canvas.itemconfig(line, fill=color)

                index_dot = (index_dot + 1) % len(self.rgb_colors)
                self.main.after(16, update_color,)

            update_color()

    def create_plus(self):
        main_color = self.load_from_config(name_in_config="plus_color", default="white")
        size = self.load_from_config(name_in_config="plus_size", default=2.5)
        gap_size = self.load_from_config(name_in_config="plus_gap", default=2.5)
        width = self.load_from_config(name_in_config="plus_width", default=2.0)

        initial_fill = "white" if main_color == "rgb" else main_color

        combine = size + gap_size

        plus_lines = [
            self.canvas.create_line(self.screen_width//2 - gap_size, self.screen_height//2, self.screen_width//2 - combine, self.screen_height//2, fill=initial_fill, width=width), # links
            self.canvas.create_line(self.screen_width//2, self.screen_height//2 - gap_size, self.screen_width//2, self.screen_height//2 - combine, fill=initial_fill, width=width), # runter
            self.canvas.create_line(self.screen_width//2 + gap_size, self.screen_height//2, self.screen_width//2 + combine, self.screen_height//2, fill=initial_fill, width=width), # rechts
            self.canvas.create_line(self.screen_width//2, self.screen_height//2 + gap_size, self.screen_width//2, self.screen_height//2 + combine, fill=initial_fill, width=width) # hoch
        ]

        if main_color == "rgb":
            index_dot = 0

            def update_color():
                nonlocal index_dot
                color = self.rgb_colors[index_dot]

                for line in plus_lines:
                    self.canvas.itemconfig(line, fill=color)

                index_dot = (index_dot + 1) % len(self.rgb_colors)
                self.main.after(16, update_color,)

            update_color()

    def create_drei(self):
        main_color = self.load_from_config(name_in_config="triangle_color", default="white")
        size = self.load_from_config(name_in_config="triangle_size", default=2.5)
        width = self.load_from_config(name_in_config="triangle_width", default=5.0)

        initial_fill = "white" if main_color == "rgb" else main_color

        simple_triangle = self.canvas.create_line(
                            self.screen_width//2 + size, self.screen_height//2 + size, #linke ecke
                            self.screen_width//2 - size, self.screen_height//2 + size, # rechte ecke
                            self.screen_width//2, self.screen_height//2, #spitze
                            self.screen_width//2 + size, self.screen_height//2 + size, # linke ecke
                            width=width, fill=initial_fill
        )

        if main_color == "rgb":
            index_dot = 0

            def update_color_dot():
                nonlocal index_dot
                color = self.rgb_colors[index_dot]

                self.canvas.itemconfig(simple_triangle, fill=color)

                index_dot = (index_dot + 1) % len(self.rgb_colors)
                self.main.after(16, update_color_dot,)