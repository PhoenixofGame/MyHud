import colorsys
import tkinter as tk
import win32con
import win32gui

try:
    from assets.Config_Manager import ConfigManager
except ImportError:
    from Config_Manager import ConfigManager

cm = ConfigManager()

class Title_UI:
    def __init__(self, config_file: str, master):
        self.running = False
        self.config_file = config_file


        self.main = tk.Toplevel(master)
        self.main.attributes("-topmost", True)
        self.main.update()
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

        Title = canvas.create_text(
            screen_width // 2,
            50,
            text="",
            font=("Sitka", 15),
            fill="white"
        )

        title_default_text = cm.load_from_config(config_name= self.config_file, name_in_config= "title_default_text", default="Title")
        title_color = cm.load_from_config(config_name= self.config_file, name_in_config="title_color", default="white")
        title_size = cm.load_from_config(config_name= self.config_file, name_in_config="title_size", default=25)

        if title_color != "rgb":
            canvas.itemconfig(
                Title,
                text=title_default_text,
                font=("Sitka", title_size),
                fill=title_color
            )
        else:
            title_colors = []
            for i in range(360):
                h = i / 360.0
                r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
                title_colors.append('#{0:02X}{1:02X}{2:02X}'.format(
                    int(r * 255), int(g * 255), int(b * 255)
                ))
            index_color = [0]
            def update_color_titel():
                color = title_colors[index_color[0]] # noqa
                canvas.itemconfig(Title, fill=color)
                index_color[0] = (index_color[0] + 1) % len(title_colors)
                title_animation_id = self.main.after(16, update_color_titel) # noqa
            canvas.itemconfig(
                Title,
                text=title_default_text,
                font=("Sitka", title_size)
            )
            update_color_titel()

    def start_title(self):
        self.running = True

        def force_topmost2():
            self.main.attributes("-topmost", True)
            self.main.after(500, force_topmost2) # noqa
        self.main.after(100, force_topmost2) # noqa

    def destroy_main(self):
        self.main.destroy()

    def stop_title(self):
        self.running = False
        self.main.after(0, self.destroy_main) # noqa
