import customtkinter

class UiClass:
    def __init__(self, name, main_color, secondary_color, text_color):
        self.name = name
        self.label = name + "_label"
        self.frame = name + "_frame"
        self.controls = name + "_controls"
        self.main_button = name + "_main_button"
        self.save_button = name + "_save_button"
        self.main_color = main_color
        self.secondary_color = secondary_color
        self.text_color = text_color

    def create_module(self, master, command_main, command_second, hover_color, label_text):
        self.frame = customtkinter.CTkFrame(master, corner_radius=20, fg_color=self.main_color)
        self.frame.pack(fill="x", padx=40, pady=10)

        self.label = customtkinter.CTkLabel(
            self.frame, text=label_text, font=("Comic Sans MS", 42, "bold"), text_color=self.text_color)
        self.label.pack(side="left", padx=30, pady=10)

        self.controls = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        self.controls.pack(side="right", padx=20)

        if command_main is not None:
            self.main_button = customtkinter.CTkSwitch(
                self.controls,
                text="",
                corner_radius=50,
                command=command_main,
                switch_width=90,  # Breite des Switches
                switch_height=40,  # Höhe des Switches
                fg_color="red",  # Farbe wenn AUS
                progress_color="green",  # Farbe wenn AN
                button_color="#cfcccc",  # Farbe des Schiebereglers
                button_hover_color="#cfcccc",
                border_width=3,
                border_color="#cfcccc",
                text_color=self.text_color
            )
            self.main_button.pack(side="left", padx=10)

        if command_second is not None:
            self.save_button = customtkinter.CTkButton(
                self.controls, text="⚙️", width=40, height=45,
                fg_color="#1b1b1b", hover_color= hover_color, text_color=self.text_color,
                font=("Comic Sans MS", 30), corner_radius=10, command=command_second
            )
            self.save_button.pack(side="left", padx=10)

    def update_label(self, new_text):
        if self.label:
            self.label.configure(text=new_text)





