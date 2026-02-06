import customtkinter
import json
from tkinter import colorchooser





class SettingsMenu:
    def __init__(self, name, main_color, secondary_color, config_file):
        self.name = name
        self.main_color = main_color
        self.secondary_color = secondary_color
        self.config_file = config_file

        self.entries = []
        self.frame = None
        self.save_button = None


    def create_new(self, master):
        settings_win = customtkinter.CTkToplevel(master)
        settings_win.title(f"{self.name} Settings ⚙️")
        settings_win.minsize(600, 100)
        settings_win.resizable(False, False)
        settings_win.configure(fg_color=self.main_color)
        settings_win.grab_set()
        settings_win.wm_attributes("-alpha", 0.95)

        title = customtkinter.CTkLabel(
            settings_win,
            text=f"⚙️ {self.name} Settings",
            font=("Comic Sans MS", 30, "bold"),
            text_color=self.secondary_color
        )
        title.pack(pady=20)

        self.frame = customtkinter.CTkFrame(settings_win, fg_color="transparent")
        self.frame.pack(pady=10, fill="x", padx=30)

        def save_settings():
            # bestehende JSON laden
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    settings_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                settings_data = {}

            # Entries speichern (typisiert)
            for entry in self.entries:
                raw_value = entry["widget"].get().strip()
                if not raw_value:
                    continue

                try:
                    value = entry["type"](raw_value)
                except ValueError:
                    print(f"Ungültiger Wert für {entry['label']}: {raw_value}")
                    continue

                settings_data[entry["label"]] = value

            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(settings_data, f, indent=4, ensure_ascii=False)


            self.save_button.configure(text="✅ Saved!", fg_color="#00cc66")
            settings_win.after(
                300,
                lambda: self.save_button.configure(
                    text="Save Settings",
                    fg_color=self.secondary_color
                )
            )
            settings_win.after(400, settings_win.destroy)

        self.save_button = customtkinter.CTkButton(
            settings_win,
            text="Save Settings",
            font=("Comic Sans MS", 25, "bold"),
            fg_color=self.secondary_color,
            hover_color=self.secondary_color,
            text_color="black",
            command=save_settings
        )
        self.save_button.pack(pady=20)

    def add_color_picker(self, text, default_color, save_variable, show_rgb = True):
        if not self.frame:
            return None

        # Standardfarbe für den Button
        current_color = default_color

        # Prüfe ob default_color RGB ist (beginnt mit "rgb(")
        if default_color == "rgb":
            is_rgb = True
        else:
            is_rgb = False

        def choose_color():
            nonlocal current_color
            # askcolor gibt ein Tuple zurück: ((r,g,b), "#hexcode")
            color = colorchooser.askcolor(title="Choose color")
            if color[1]:  # Wenn eine Farbe gewählt wurde (nicht abgebrochen)
                current_color = color[1]
                button.configure(fg_color=current_color)

        # Container Frame für Button und Label
        container = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        container.pack(pady=8, fill="x")

        label = customtkinter.CTkLabel(
            container,
            text=text,
            font=("Comic Sans MS", 20, "bold"),
        )
        label.pack(side="left")

        if show_rgb:
            rgb_switch = customtkinter.CTkSwitch(
                container,
                text="Toggle RGB",
                switch_width=40,
                switch_height=20,
                font=("Comic Sans MS", 20, "bold"),
            )
            rgb_switch.pack(side="right", padx=(10, 10))

        button = customtkinter.CTkButton(
            container,
            text="",
            width=40,
            height=40,
            command=choose_color,
            fg_color=current_color if not is_rgb else "red",  # Fallback für RGB
            border_width=2,
            border_color="white",
            hover_color=current_color if not is_rgb else "red",
        )
        button.pack(side="right", padx=(10, 10))

        # Switch auf "on" setzen wenn default RGB ist
        if show_rgb:
            if is_rgb:
                rgb_switch.select()

        class ColorPickerWrapper:
            def __init__(self, initial_color):
                self.color = initial_color

            def get(self):
                if show_rgb and rgb_switch.get():
                    return "rgb"
                return current_color

            def set(self, color):
                nonlocal current_color
                current_color = color
                button.configure(fg_color=color)

        wrapper = ColorPickerWrapper(current_color)

        self.entries.append({
            "label": save_variable,
            "widget": wrapper,
            "type": str
        })

        return button

    def add_entry(self, entry_name,text, placeholder, value_type=str):
        if not self.frame:
            return None

        # Container Frame für Button und Label
        container = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        container.pack(pady=8, fill="x")

        label = customtkinter.CTkLabel(
            container,
            text=text,
            font=("Comic Sans MS", 20, "bold"),
        )
        label.pack(side="left")

        entry = customtkinter.CTkEntry(
            container,
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text=str(placeholder)
        )
        entry.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.entries.append({
            "label": entry_name,
            "widget": entry,
            "type": value_type
        })

        return entry

    def get_entry_value(self, entry_name):
        for entry in self.entries:
            if entry["label"] == entry_name:
                raw_value = entry["widget"].get().strip()
                try:
                    return entry["type"](raw_value)
                except ValueError:
                    return None
        return None

