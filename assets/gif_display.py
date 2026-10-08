import tkinter as tk
import os
import win32con
import win32gui
import json

from PIL import Image, ImageTk

from pynput import keyboard

try:
    from assets.Config_Manager import ConfigManager
except ImportError:
    from Config_Manager import ConfigManager

cm = ConfigManager()


def key_to_str(key):
    if isinstance(key, keyboard.Key):
        return key.name
    if isinstance(key, keyboard.KeyCode) and key.char:
        return key.char.lower()
    return None

class AnimatedGIF:
    def __init__(self, canvas, gif_path, x, y, width=None, height=None, anchor="center", name=None):
        self.name = name
        self.canvas = canvas
        self.x = x
        self.y = y
        self.anchor = anchor
        self.width = width
        self.height = height

        self.running = False
        self.after_id = None
        self.current_frame = 0
        self.is_animated = False

        self.pil_image = Image.open(gif_path)
        self.frames = []
        self.photo_images = []

        try:
            self.pil_image.seek(1)
            self.is_animated = True
            self.pil_image.seek(0)
        except EOFError:
            self.is_animated = False

        if self.is_animated:
            try:
                while True:
                    frame = self.pil_image.copy().convert("RGBA")
                    if self.width and self.height:
                        frame = frame.resize((self.width, self.height), Image.Resampling.LANCZOS)
                    self.frames.append(frame)
                    self.pil_image.seek(len(self.frames))
            except EOFError:
                pass

            if not self.frames:
                raise ValueError("Keine Frames im GIF gefunden")

            self.pil_image.seek(0)
            self.delay = self.pil_image.info.get("duration", 100)
        else:
            frame = self.pil_image.convert("RGBA")
            if self.width and self.height:
                frame = frame.resize((self.width, self.height), Image.Resampling.LANCZOS)
            self.frames.append(frame)
            self.delay = 0

        first_photo = ImageTk.PhotoImage(
            self.frames[0],
            master=self.canvas.master
        )
        self.photo_images.append(first_photo)
        self.current_photo = first_photo

        self.image_id = self.canvas.create_image(
            self.x,
            self.y,
            image=self.current_photo,
            anchor=self.anchor
        )

        if self.is_animated:
            self.start()

    def animate(self):
        if not self.running or not self.is_animated:
            return

        frame_index = self.current_frame % len(self.frames)

        while len(self.photo_images) <= frame_index:
            photo = ImageTk.PhotoImage(
                self.frames[len(self.photo_images)],
                master=self.canvas.master
            )
            self.photo_images.append(photo)

        self.current_photo = self.photo_images[frame_index]
        self.canvas.itemconfigure(self.image_id, image=self.current_photo)

        self.current_frame = (self.current_frame + 1) % len(self.frames)

        self.after_id = self.canvas.after(self.delay, self.animate)

    def start(self):
        if not self.running and self.is_animated:
            self.running = True
            self.animate()

    def stop(self):
        self.running = False
        if self.after_id:
            self.canvas.after_cancel(self.after_id)
            self.after_id = None

    def hide(self):
        self.canvas.itemconfigure(self.image_id, state="hidden")

    def show(self):
        self.canvas.itemconfigure(self.image_id, state="normal")

    def destroy(self):
        self.stop()
        self.canvas.delete(self.image_id)

    def resize(self, width, height):
        """
        Bild-Größe zur Laufzeit ändern
        """
        self.width = width
        self.height = height

        self.frames.clear()
        self.photo_images.clear()
        self.current_frame = 0

        if self.is_animated:
            self.pil_image.seek(0)

            try:
                while True:
                    frame = self.pil_image.copy().convert("RGBA")
                    frame = frame.resize(
                        (self.width, self.height),
                        Image.Resampling.LANCZOS
                    )
                    self.frames.append(frame)
                    self.pil_image.seek(len(self.frames))
            except EOFError:
                pass
        else:
            self.pil_image.seek(0)
            frame = self.pil_image.convert("RGBA")
            frame = frame.resize(
                (self.width, self.height),
                Image.Resampling.LANCZOS
            )
            self.frames.append(frame)

        first_photo = ImageTk.PhotoImage(
            self.frames[0],
            master=self.canvas.master
        )
        self.photo_images.append(first_photo)
        self.current_photo = first_photo
        self.canvas.itemconfigure(self.image_id, image=self.current_photo)

class GifOverlay:
    def __init__(self, config_file: str, master, on_drop=None):
        self.config_file = config_file
        self.on_drop = on_drop
        self.hotkey_listener = None
        self.drag_active = False
        self.animated_gifs = []

        self.running = False

        self.UI_Gif = tk.Toplevel(master)
        self.UI_Gif.attributes("-topmost", True)
        self.UI_Gif.attributes("-transparentcolor", "black") # noqa
        self.UI_Gif.overrideredirect(True)

        # Make the window click-through
        self.UI_Gif.update()
        mainhwnd = win32gui.FindWindow(None, str(self.UI_Gif.title())) # noqa
        exStyle = win32gui.GetWindowLong(mainhwnd, win32con.GWL_EXSTYLE) # noqa
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
            self.UI_Gif.after(500, force_topmost2) # noqa

        self.UI_Gif.after(100, force_topmost2) # noqa

        self.start_hotkey_listener()

    def load_and_create_gifs(self):
        for gif in self.animated_gifs:
            try:
                gif.stop()
            except Exception as e:
                print(f"Error: {e}")

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
                                self.canvas, gif_file_name,
                                config.get("x", 0), config.get("y", 0),
                                width=config.get("width", 200), height=config.get("height", 200),
                                name=gif_name
                            )
                            animated_gif.start()
                            self.enable_drag(animated_gif)
                            self.animated_gifs.append(animated_gif)
                        except Exception as e:
                            print(f"Error: {e}")

        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def reload_gifs(self):
        self.load_and_create_gifs()

    def start_gif(self):
        self.running = True

        def force_topmost2():
            self.UI_Gif.attributes("-topmost", True)
            self.UI_Gif.after(500, force_topmost2)  # noqa

        self.UI_Gif.after(100, force_topmost2)  # noqa

    def destroy_main(self):
        self.UI_Gif.destroy()

    def stop_gif(self):
        self.running = False
        if self.hotkey_listener:
            self.hotkey_listener.stop()
        for g in self.animated_gifs:
            g.stop()
        self.UI_Gif.after(0, self.destroy_main)  # noqa

    def set_click_through(self, enabled):
        try:
            hwnd = win32gui.GetParent(self.UI_Gif.winfo_id())
            ex = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if enabled:
                ex |= win32con.WS_EX_TRANSPARENT
            else:
                ex &= ~win32con.WS_EX_TRANSPARENT
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex)
        except Exception as e:
            print(f"click-through Fehler: {e}")

    def enable_drag(self, gif):
        offset = {}

        def press(e):
            offset["x"], offset["y"] = e.x - gif.x, e.y - gif.y

        def move(e):
            gif.x, gif.y = e.x - offset["x"], e.y - offset["y"]
            self.canvas.coords(gif.image_id, gif.x, gif.y)

        def release(e):
            self.save_position(gif)

        self.canvas.tag_bind(gif.image_id, "<ButtonPress-1>", press)
        self.canvas.tag_bind(gif.image_id, "<B1-Motion>", move)
        self.canvas.tag_bind(gif.image_id, "<ButtonRelease-1>", release)

    def save_position(self, gif):
        x, y = int(gif.x), int(gif.y)
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if gif.name in data:
                data[gif.name]["x"] = x
                data[gif.name]["y"] = y
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        if self.on_drop:
            self.on_drop(gif.name, x, y)

    def start_hotkey_listener(self):
        hotkey = str(cm.load_from_config("assets/config.json", "gif_drag_hotkey", default="f8")).lower()

        def set_drag(active):
            try:
                self.UI_Gif.after(0, lambda: self.set_click_through(not active))
            except Exception:
                pass

        def on_press(key):
            if key_to_str(key) == hotkey and not self.drag_active:
                self.drag_active = True
                set_drag(True)

        def on_release(key):
            if key_to_str(key) == hotkey and self.drag_active:
                self.drag_active = False
                set_drag(False)

        self.hotkey_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.hotkey_listener.daemon = True
        self.hotkey_listener.start()