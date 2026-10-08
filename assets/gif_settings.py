import json
import customtkinter as ctk
import os
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


class GifSetting:
    def __init__(self, name, font, config_file):
        self.name = name
        self.font = font
        self.config_file = config_file
        self.restart_func = None

        self.root = None
        self.entries = []

        self.aktive_buttons = {}
        self.hold_containers = {}
        self.entry_widgets = {}
        self.save_buttons = {}

    def create_new(self, master, restart_func):
        self.restart_func = restart_func
        self.aktive_buttons = {}
        self.hold_containers = {}
        self.entry_widgets = {}
        self.save_buttons = {}

        self.root = ctk.CTkFrame(master, corner_radius=20, width=1230)
        self.root.pack(pady=10, fill="x", padx=30)

        title = ctk.CTkLabel(self.root, text=f"⚙️ {self.name} Settings",
                             font=(self.font, 30, "bold"))
        title.pack(pady=20)

        self.build_hotkey_row()

        body = ctk.CTkFrame(self.root, fg_color="transparent")
        body.pack(fill="x", padx=10, pady=10)

        container_b = ctk.CTkFrame(body, fg_color="transparent", width=250)
        container_b.pack(side="left", fill="y", padx=5, pady=5)

        scroll_frame = ctk.CTkScrollableFrame(container_b, fg_color="grey", width=230, height=300)
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.scroll_frame_a = ctk.CTkFrame(body, fg_color="transparent")
        self.scroll_frame_a.pack(side="right", expand=True, fill="both", padx=5, pady=5)

        bild_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
        bild_dateien = [f for f in os.listdir("Your_Gifs") if f.lower().endswith(bild_extensions)]

        for datei in bild_dateien:
            btn = ctk.CTkButton(scroll_frame, text=datei,
                                command=lambda d=datei: self.toggle_button(d),
                                anchor="w", fg_color="red", hover_color="#450000")
            btn.pack(fill="x", pady=2, padx=5)
            self.aktive_buttons[datei] = {"button": btn, "aktiv": False}

        self.load_active_gifs()

    def destroy(self, master):
        if self.root is not None:
            self.root.destroy()
            self.root = None
            master.update()
            if hasattr(master, '_parent_canvas'):
                master._parent_canvas.configure(scrollregion=master._parent_canvas.bbox("all"))  # noqa

    def load_active_gifs(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)

            for gif_name, config in settings_data.items():
                if config.get("enabled", False) and gif_name in self.aktive_buttons:
                    # restart=False: beim Öffnen des Menüs kein Overlay-Neustart
                    self.toggle_button(gif_name, restart=False)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def load_gif_config(self, gif_name):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)

            if gif_name in settings_data:
                return settings_data[gif_name]
            else:
                return {
                    "x": 0,
                    "y": 0,
                    "width": 200,
                    "height": 200,
                    "enabled": False
                }
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "x": 0,
                "y": 0,
                "width": 200,
                "height": 200,
                "enabled": False
            }

    def _restart(self):
        if self.restart_func is not None and self.root is not None:
            self.root.after(0, self.restart_func)

    def toggle_button(self, dateiname, restart=True):
        button_info = self.aktive_buttons[dateiname]
        button = button_info["button"]

        if button_info["aktiv"]:
            button.configure(fg_color="red", hover_color="#450000")

            if dateiname in self.hold_containers:
                self.hold_containers[dateiname].destroy()
                del self.hold_containers[dateiname]

            if dateiname in self.entry_widgets:
                del self.entry_widgets[dateiname]

            if dateiname in self.save_buttons:
                del self.save_buttons[dateiname]

            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    settings_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                settings_data = {}

            if dateiname in settings_data:
                settings_data[dateiname]["enabled"] = False
                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(settings_data, f, indent=4, ensure_ascii=False)

            button_info["aktiv"] = False

            if restart:
                self._restart()
        else:
            button.configure(fg_color="green", hover_color="#006300")
            current_config = self.load_gif_config(dateiname)

            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    settings_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                settings_data = {}

            settings_data[dateiname] = {
                "x": current_config["x"],
                "y": current_config["y"],
                "width": current_config["width"],
                "height": current_config["height"],
                "enabled": True
            }

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(settings_data, f, indent=4, ensure_ascii=False)

            hold_container = ctk.CTkFrame(
                self.scroll_frame_a,
                fg_color="grey",
                corner_radius=5,
                height=60
            )
            hold_container.pack(pady=5, padx=10, fill="x")

            title = ctk.CTkLabel(
                hold_container,
                text=f"⚙️ {dateiname} Settings",
                font=("Comic Sans MS", 30, "bold"),
                text_color="white"
            )
            title.pack(pady=20)

            main_frame = ctk.CTkFrame(hold_container, fg_color="transparent")
            main_frame.pack(pady=10, fill="x", padx=30)

            self.entry_widgets[dateiname] = {}

            # X Position
            container = ctk.CTkFrame(main_frame, fg_color="transparent")
            container.pack(pady=8, fill="x")

            label = ctk.CTkLabel(
                container,
                text="X Position:",
                font=("Comic Sans MS", 20, "bold"),
            )
            label.pack(side="left")

            gif_x = ctk.CTkEntry(
                container,
                fg_color="#ffffff",
                text_color="#000000",
                placeholder_text=str(current_config["x"])
            )
            gif_x.insert(0, str(current_config["x"]))
            gif_x.pack(side="right", fill="x", expand=True, padx=(10, 0))
            self.entry_widgets[dateiname]["x"] = gif_x

            # Y Position
            container1 = ctk.CTkFrame(main_frame, fg_color="transparent")
            container1.pack(pady=8, fill="x")

            label1 = ctk.CTkLabel(
                container1,
                text="Y Position:",
                font=("Comic Sans MS", 20, "bold"),
            )
            label1.pack(side="left")

            gif_y = ctk.CTkEntry(
                container1,
                fg_color="#ffffff",
                text_color="#000000",
                placeholder_text=str(current_config["y"])
            )
            gif_y.insert(0, str(current_config["y"]))
            gif_y.pack(side="right", fill="x", expand=True, padx=(10, 0))
            self.entry_widgets[dateiname]["y"] = gif_y

            # Width
            container2 = ctk.CTkFrame(main_frame, fg_color="transparent")
            container2.pack(pady=8, fill="x")

            label2 = ctk.CTkLabel(
                container2,
                text="Width:",
                font=("Comic Sans MS", 20, "bold"),
            )
            label2.pack(side="left")

            gif_size_x = ctk.CTkEntry(
                container2,
                fg_color="#ffffff",
                text_color="#000000",
                placeholder_text=str(current_config["width"])
            )
            gif_size_x.insert(0, str(current_config["width"]))
            gif_size_x.pack(side="right", fill="x", expand=True, padx=(10, 0))
            self.entry_widgets[dateiname]["width"] = gif_size_x

            # Height
            container3 = ctk.CTkFrame(main_frame, fg_color="transparent")
            container3.pack(pady=8, fill="x")

            label3 = ctk.CTkLabel(
                container3,
                text="Height:",
                font=("Comic Sans MS", 20, "bold"),
            )
            label3.pack(side="left")

            gif_size_y = ctk.CTkEntry(
                container3,
                fg_color="#ffffff",
                text_color="#000000",
                placeholder_text=str(current_config["height"])
            )
            gif_size_y.insert(0, str(current_config["height"]))
            gif_size_y.pack(side="right", fill="x", expand=True, padx=(10, 0))
            self.entry_widgets[dateiname]["height"] = gif_size_y

            def save_settings(gif_name=dateiname):
                try:
                    with open(self.config_file, "r", encoding="utf-8") as e:
                        settings_data_2 = json.load(e)
                except (FileNotFoundError, json.JSONDecodeError):
                    settings_data_2 = {}

                settings_data_2[gif_name] = {
                    "x": int(self.entry_widgets[gif_name]["x"].get() or 0),
                    "y": int(self.entry_widgets[gif_name]["y"].get() or 0),
                    "width": int(self.entry_widgets[gif_name]["width"].get() or 200),
                    "height": int(self.entry_widgets[gif_name]["height"].get() or 200),
                    "enabled": True
                }

                with open(self.config_file, "w", encoding="utf-8") as t:
                    json.dump(settings_data_2, t, indent=4, ensure_ascii=False)

                self._restart()

                self.save_buttons[gif_name].configure(text="✅ Saved!", fg_color="#00cc66")

                def reset_button():
                    btn = self.save_buttons.get(gif_name)
                    if btn is not None:
                        try:
                            btn.configure(text="Save Settings", fg_color="white")
                        except Exception:
                            pass

                self.root.after(300, reset_button)  # noqa

            save_button = ctk.CTkButton(
                main_frame,
                text="Save Settings",
                font=("Comic Sans MS", 25, "bold"),
                fg_color="white",
                hover_color="white",
                text_color="black",
                command=save_settings
            )
            save_button.pack(pady=20)

            self.save_buttons[dateiname] = save_button

            self.hold_containers[dateiname] = hold_container

            button_info["aktiv"] = True

            if restart:
                self._restart()

    def get_enabled_gifs(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)

            enabled_gifs = {}
            for gif_name, config in settings_data.items():
                if config.get("enabled", False):
                    enabled_gifs[gif_name] = config

            return enabled_gifs
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def build_hotkey_row(self):
        current = str(cm.load_from_config("assets/config.json", "gif_drag_hotkey", default="f8"))
        row = ctk.CTkFrame(self.root, fg_color="transparent")
        row.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(row, text="Drag Hotkey (halten):", font=(self.font, 20, "bold")).pack(side="left")

        self.hotkey_button = ctk.CTkButton(row, text=current.upper(), width=150, command=self.capture_hotkey)
        self.hotkey_button.pack(side="right")

    def capture_hotkey(self):
        self.hotkey_button.configure(text="Taste drücken...")

        def on_press(key):
            name = key_to_str(key)
            if name is None:
                return None
            try:
                self.root.after(0, lambda: self.apply_hotkey(name))
            except Exception:
                pass
            return False

        keyboard.Listener(on_press=on_press).start()

    def apply_hotkey(self, name):
        if name == "esc":
            name = str(cm.load_from_config("assets/config.json", "gif_drag_hotkey", default="f8"))
        else:
            cm.save_to_config("assets/config.json", "gif_drag_hotkey", name)
            self._restart()
        self.hotkey_button.configure(text=name.upper())

    def update_position(self, name, x, y):
        if self.root is None or name not in self.entry_widgets:
            return
        try:
            for key, val in (("x", x), ("y", y)):
                entry = self.entry_widgets[name][key]
                entry.delete(0, "end")
                entry.insert(0, str(val))
        except Exception:
            pass