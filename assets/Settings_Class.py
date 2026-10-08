import customtkinter
import threading
from tkinter import colorchooser

try:
    from assets.Config_Manager import ConfigManager
except ImportError:
    from Config_Manager import ConfigManager


class SettingsMenu:
    def __init__(self, name, font, config_file):
        self.name = name
        self.config_file = config_file
        self.font = font

        self.settings_win = None

        self.entries = []
        self.frame = None
        self.save_button = None


    def create_new(self, master, restart_func):
        self.settings_win = customtkinter.CTkFrame(master, corner_radius=20, width=1230)
        self.settings_win.pack(pady=10, fill="x", padx=30)

        title = customtkinter.CTkLabel(
            self.settings_win,
            text=f"⚙️ {self.name} Settings",
            font=(self.font, 30, "bold"),
        )
        title.pack(pady=20)

        self.frame = customtkinter.CTkFrame(self.settings_win, fg_color="transparent")
        self.frame.pack(pady=10, fill="x", padx=30)

        def save_settings():

            for entry in self.entries:
                raw_value = entry["widget"].get().strip()
                if not raw_value:
                    continue

                try:
                    value = entry["type"](raw_value)
                except ValueError:
                    print(f"Ungültiger Wert für {entry['label']}: {raw_value}")
                    continue

                ConfigManager().save_to_config(self.config_file, entry["label"], value)

            if restart_func is not None:
                threading.Thread(target=restart_func, daemon=True).start()

            self.save_button.configure(text="✅ Saved!", fg_color="#00cc66")
            self.settings_win.after(
                300,
                lambda: self.save_button.configure(
                    text="Save Settings",
                )
            ) # noqa

            self.settings_win.after(
                300,
                lambda: self.save_button.configure(
                    text="Save Settings",
                )
            ) # noqa


        self.save_button = customtkinter.CTkButton(
            self.settings_win,
            text="Save Settings",
            font=(self.font, 25, "bold"),
            command=save_settings
        )
        self.save_button.pack(pady=20)

    def add_color_picker(self, text, default_color, save_variable, show_rgb = True):
        if not self.frame:
            return None

        current_color = default_color
        if default_color == "rgb":
            is_rgb = True
        else:
            is_rgb = False

        def choose_color():
            nonlocal current_color
            color = colorchooser.askcolor(title="Choose color")
            if color[1]:
                current_color = color[1]
                button.configure(fg_color=current_color)

        container = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        container.pack(pady=8, fill="x")

        label = customtkinter.CTkLabel(
            container,
            text=text,
            font=(self.font, 20, "bold"),
        )
        label.pack(side="left")

        if show_rgb:
            rgb_switch = customtkinter.CTkSwitch(
                container,
                text="Toggle RGB",
                switch_width=40,
                switch_height=20,
                font=(self.font, 20, "bold"),
            )
            rgb_switch.pack(side="right", padx=(10, 10))

        button = customtkinter.CTkButton(
            container,
            text="",
            width=40,
            height=40,
            command=choose_color,
            fg_color=current_color if not is_rgb else "red",
            border_width=2,
            hover_color=current_color if not is_rgb else "red",
        )
        button.pack(side="right", padx=(10, 10))

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

        container = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        container.pack(pady=8, fill="x")

        label = customtkinter.CTkLabel(
            container,
            text=text,
            font=(self.font, 20, "bold"),
        )
        label.pack(side="left", padx=(0, 10))

        entry = customtkinter.CTkEntry(
            container,
            placeholder_text=str(placeholder),
            width=450
        )
        entry.pack(side="right")

        self.entries.append({
            "label": entry_name,
            "widget": entry,
            "type": value_type
        })

        return entry

    def add_switch(self, switch_text, save_stuff, saved_status):
        if not self.frame:
            return None

        container = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        container.pack(pady=8, fill="x")

        label = customtkinter.CTkLabel(
            container,
            text=switch_text,
            font=(self.font, 20, "bold"),
        )
        label.pack(side="left", padx=(0, 10))

        switch = customtkinter.CTkSwitch(
            container,
            text="",
            corner_radius=50,
            switch_width=90,  # Breite des Switches
            switch_height=40,  # Höhe des Switches
            fg_color="red",  # Farbe wenn AUS
            progress_color="green",  # Farbe wenn AN
            border_width=3,
        )
        switch.pack(side="right", padx=(10, 0))

        if saved_status == "True":
            switch.select()

        class switch_toggle:
            def __init__(self, switch_in):
                self.switch_in = switch_in

            def get(self):
                if self.switch_in.get() == 1:
                    return "True"
                else:
                    return "False"

        switch_out = switch_toggle(switch)

        self.entries.append({
            "label": save_stuff,
            "widget": switch_out,
            "type": str
        })

        return switch

    def add_dropdown(self, dropdown_name, text, options, saved_value=None):
        if not self.frame:
            return None

        container = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        container.pack(pady=8, fill="x")

        label = customtkinter.CTkLabel(
            container,
            text=text,
            font=(self.font, 20, "bold"),
        )
        label.pack(side="left", padx=(0, 10))

        dropdown = customtkinter.CTkOptionMenu(
            container,
            values=options,
            font=(self.font, 18, "bold"),
            text_color="#000000",
            dropdown_text_color="#000000",
            dropdown_hover_color="#dddddd",
            width=450,
        )
        dropdown.pack(side="right")

        if saved_value and saved_value in options:
            dropdown.set(saved_value)
        elif options:
            dropdown.set(options[0])

        self.entries.append({
            "label": dropdown_name,
            "widget": dropdown,
            "type": str
        })

        return dropdown

    def get_entry_value(self, entry_name):
        for entry in self.entries:
            if entry["label"] == entry_name:
                raw_value = entry["widget"].get().strip()
                try:
                    return entry["type"](raw_value)
                except ValueError:
                    return None
        return None

    def destroy(self, master):
        def do_destroy():
            for entry in self.entries:
                widget = entry["widget"]
                if isinstance(widget, customtkinter.CTkOptionMenu):
                    try:
                        widget._close_dropdown_menu()
                    except Exception:
                        pass
            self.settings_win.destroy()
            master.update()
            if hasattr(master, '_parent_canvas'):
                master._parent_canvas.configure(scrollregion=master._parent_canvas.bbox("all"))  # noqa

        do_destroy()


