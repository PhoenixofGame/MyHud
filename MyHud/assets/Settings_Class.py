import customtkinter
import json



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
        settings_win.wm_attributes("-alpha", 0.85)

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
                1000,
                lambda: self.save_button.configure(
                    text="Save Settings",
                    fg_color=self.secondary_color
                )
            )
            settings_win.after(1000, settings_win.destroy)

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



    def add_entry(self, entry_name, placeholder, value_type=str):
        if not self.frame:
            return None

        entry = customtkinter.CTkEntry(
            self.frame,
            fg_color="#ffffff",
            text_color="#000000",
            placeholder_text=str(placeholder)
        )
        entry.pack(fill="x", pady=8)

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

