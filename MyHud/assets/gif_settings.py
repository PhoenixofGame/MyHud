import json
import customtkinter as ctk
import os
from assets.Settings_Class import SettingsMenu


class GifSetting:
    def __init__(self, master, name, config_file):
        self.name = name
        self.config_file = config_file

        self.test = ctk.CTkToplevel(master)
        self.test.attributes("-topmost", True)
        self.test.geometry("700x500")
        self.test.title("Gif Settings")
        self.test.configure(fg_color="black")
        self.test.wm_attributes("-alpha", 0.95)
        self.test.resizable(False, False)

        # Dictionary um Button-Zustände und Labels zu speichern
        self.aktive_buttons = {}
        self.hold_containers = {}
        self.entry_widgets = {}  # Speichert alle Entry-Widgets
        self.save_buttons = {}  # NEU: Speichert alle Save-Buttons separat

        container_titel = ctk.CTkLabel(self.test, fg_color="transparent", height=50, text="Gif Settings",
                                       font=("Comic Sans MS", 40, "bold"))
        container_titel.pack(side="top", fill="x", padx=5, pady=(5, 0))

        self.container_a = ctk.CTkFrame(self.test, fg_color="transparent")
        self.container_a.pack(side="right", expand="true", fill="both", padx=(0, 5), pady=5)

        # Scrollbarer Frame für die gelben Labels
        self.scroll_frame_a = ctk.CTkScrollableFrame(self.container_a, fg_color="transparent")
        self.scroll_frame_a.pack(fill="both", expand=True, padx=5, pady=5)

        container_b = ctk.CTkFrame(self.test, fg_color="transparent", width=200)
        container_b.pack(side="left", fill="y", padx=5, pady=5)

        scroll_frame = ctk.CTkScrollableFrame(container_b, fg_color="grey")
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Bildformate
        bild_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')

        # Dateien aus Ordner laden
        bild_dateien = [
            f for f in os.listdir("assets/Your_Gifs")
            if f.lower().endswith(bild_extensions)
        ]

        # Button für jede Bilddatei erstellen
        for datei in bild_dateien:
            btn = ctk.CTkButton(
                scroll_frame,
                text=datei,
                command=lambda d=datei: self.toggle_button(d),
                anchor="w",
                fg_color="red",
            )
            btn.pack(fill="x", pady=2, padx=5)

            # Button im Dictionary speichern
            self.aktive_buttons[datei] = {"button": btn, "aktiv": False}

        # NEUE FUNKTION: Nach dem Erstellen aller Buttons, aktivierte GIFs laden
        self.load_active_gifs()

    def load_active_gifs(self):
        """Lädt alle aktivierten GIFs und setzt deren Buttons auf aktiv"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)

            for gif_name, config in settings_data.items():
                if config.get("enabled", False) and gif_name in self.aktive_buttons:
                    # Button automatisch aktivieren
                    self.toggle_button(gif_name)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def load_gif_config(self, gif_name):
        """Lädt die Konfiguration für ein bestimmtes GIF"""
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                settings_data = json.load(f)

            if gif_name in settings_data:
                return settings_data[gif_name]
            else:
                # Standard-Werte zurückgeben
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

    def toggle_button(self, dateiname):
        button_info = self.aktive_buttons[dateiname]
        button = button_info["button"]

        # Zustand umschalten
        if button_info["aktiv"]:
            # Deaktivieren
            button.configure(fg_color="red")

            if dateiname in self.hold_containers:
                self.hold_containers[dateiname].destroy()
                del self.hold_containers[dateiname]

            if dateiname in self.entry_widgets:
                del self.entry_widgets[dateiname]

            if dateiname in self.save_buttons:
                del self.save_buttons[dateiname]

            # WICHTIG: GIF in Config deaktivieren
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
        else:
            # Aktivieren
            button.configure(fg_color="green")

            # Config laden
            current_config = self.load_gif_config(dateiname)

            # NEU: Direkt beim Aktivieren in Config speichern
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
                "enabled": True  # Sofort auf enabled setzen
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

            self.frame = ctk.CTkFrame(hold_container, fg_color="transparent")
            self.frame.pack(pady=10, fill="x", padx=30)

            # Entry-Widgets erstellen und in Dictionary speichern
            self.entry_widgets[dateiname] = {}

            # X Position
            container = ctk.CTkFrame(self.frame, fg_color="transparent")
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
            container1 = ctk.CTkFrame(self.frame, fg_color="transparent")
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
            container2 = ctk.CTkFrame(self.frame, fg_color="transparent")
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
            container3 = ctk.CTkFrame(self.frame, fg_color="transparent")
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
                # bestehende JSON laden
                try:
                    with open(self.config_file, "r", encoding="utf-8") as f:
                        settings_data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    settings_data = {}

                # Werte aus Entry-Widgets speichern
                settings_data[gif_name] = {
                    "x": int(self.entry_widgets[gif_name]["x"].get() or 0),
                    "y": int(self.entry_widgets[gif_name]["y"].get() or 0),
                    "width": int(self.entry_widgets[gif_name]["width"].get() or 200),
                    "height": int(self.entry_widgets[gif_name]["height"].get() or 200),
                    "enabled": True
                }

                with open(self.config_file, "w", encoding="utf-8") as f:
                    json.dump(settings_data, f, indent=4, ensure_ascii=False)

                # Den RICHTIGEN Button updaten
                self.save_buttons[gif_name].configure(text="✅ Saved!", fg_color="#00cc66")
                self.test.after(
                    300,
                    lambda: self.save_buttons[gif_name].configure(
                        text="Save Settings",
                        fg_color="white"
                    )
                )

            save_button = ctk.CTkButton(
                self.frame,
                text="Save Settings",
                font=("Comic Sans MS", 25, "bold"),
                fg_color="white",
                hover_color="white",
                text_color="black",
                command=save_settings
            )
            save_button.pack(pady=20)

            # Save-Button im Dictionary speichern
            self.save_buttons[dateiname] = save_button

            # Container speichern
            self.hold_containers[dateiname] = hold_container

            button_info["aktiv"] = True

    def get_enabled_gifs(self):
        """Gibt eine Liste aller aktivierten GIFs mit ihren Einstellungen zurück"""
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

    def start(self):
        self.test.mainloop()