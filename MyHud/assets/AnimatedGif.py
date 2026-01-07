from PIL import Image, ImageTk


class AnimatedGIF:
    def __init__(
        self,
        canvas,
        gif_path,
        x,
        y,
        width=None,
        height=None,
        anchor="center",

    ):
        """
        canvas : Tkinter Canvas
        gif_path : Pfad zur GIF-Datei
        x, y : Position auf dem Canvas
        width, height : gewünschte GIF-Größe (optional)
        anchor : Canvas-Anker (default: center)
        """

        self.canvas = canvas
        self.x = x
        self.y = y
        self.anchor = anchor
        self.width = width
        self.height = height

        self.running = False
        self.after_id = None
        self.current_frame = 0

        # GIF laden
        self.pil_image = Image.open(gif_path)
        self.frames = []
        self.photo_images = []

        # Alle Frames laden
        try:
            while True:
                frame = self.pil_image.copy().convert("RGBA")

                # Größe ändern, falls angegeben
                if self.width and self.height:
                    frame = frame.resize(
                        (self.width, self.height),
                        Image.Resampling.LANCZOS
                    )

                self.frames.append(frame)
                self.pil_image.seek(len(self.frames))
        except EOFError:
            pass

        if not self.frames:
            raise ValueError("Keine Frames im GIF gefunden")

        # Delay aus GIF lesen
        self.pil_image.seek(0)
        self.delay = self.pil_image.info.get("duration", 100)

        # Ersten Frame erzeugen
        first_photo = ImageTk.PhotoImage(
            self.frames[0],
            master=self.canvas.master
        )
        self.photo_images.append(first_photo)
        self.current_photo = first_photo

        # Canvas-Image erstellen
        self.image_id = self.canvas.create_image(
            self.x,
            self.y,
            image=self.current_photo,
            anchor=self.anchor
        )

        # Starten
        self.start()

    # -------------------------------------------------
    # Animation
    # -------------------------------------------------
    def animate(self):
        if not self.running:
            return

        frame_index = self.current_frame % len(self.frames)

        # PhotoImage nur einmal erzeugen
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

    # -------------------------------------------------
    # Steuerung
    # -------------------------------------------------
    def start(self):
        if not self.running:
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

    # -------------------------------------------------
    # Größe zur Laufzeit ändern
    # -------------------------------------------------
    def resize(self, width, height):
        """
        GIF-Größe zur Laufzeit ändern
        """
        self.width = width
        self.height = height

        self.frames.clear()
        self.photo_images.clear()
        self.current_frame = 0

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

        # Ersten Frame neu setzen
        first_photo = ImageTk.PhotoImage(
            self.frames[0],
            master=self.canvas.master
        )
        self.photo_images.append(first_photo)
        self.current_photo = first_photo
        self.canvas.itemconfigure(self.image_id, image=self.current_photo)