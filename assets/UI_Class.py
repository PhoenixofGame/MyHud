import customtkinter

class UiClass:
    def __init__(self, name, font):
        self.name = name
        self.label = name + "_label"
        self.frame = name + "_frame"
        self.controls = name + "_controls"
        self.main_button = name + "_main_button"
        self.save_button = name + "_save_button"
        self.font = font

    def create_module(self, master, command_main, command_second, label_text, button = False, button_text = ""):
        self.frame = customtkinter.CTkFrame(master, corner_radius=20)
        self.frame.pack(fill="x", padx=40, pady=10)

        self.label = customtkinter.CTkLabel(
            self.frame, text=label_text, font=(self.font, 42, "bold"))
        self.label.pack(side="left", padx=30, pady=10)

        self.controls = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        self.controls.pack(side="right", padx=20)

        if command_main is not None:
            if not button:
                self.main_button = customtkinter.CTkSwitch(
                    self.controls,
                    text="",
                    corner_radius=50,
                    command=command_main,
                    switch_width=90,  # Breite des Switches
                    switch_height=40,  # Höhe des Switches
                    fg_color="red",  # Farbe wenn AUS
                    progress_color="green",  # Farbe wenn AN
                    border_width=3
                )
                self.main_button.pack(side="left", padx=10)
            if button:
                self.main_button = customtkinter.CTkButton(
                self.controls, text=button_text, width=40, height=45,
                font=(self.font, 30), corner_radius=10, command=command_main
            )
                self.main_button.pack(side="left", padx=10)

        if command_second is not None:
            self.save_button = customtkinter.CTkButton(
                self.controls, text="⚙️", width=40, height=45,
                font=(self.font, 30), corner_radius=10, command=command_second
            )
            self.save_button.pack(side="left", padx=10)

    def update_label(self, new_text):
        if self.label:
            self.label.configure(text=new_text)





