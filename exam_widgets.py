import customtkinter as ctk


class MainContent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.title = Title(self, "red")
        self.image_import = ImageImport(self, parent)
        self.answer = Answer(self)

        self.grid(row=0, column=2, columnspan=3, padx=10, pady=10, sticky="nsew")


class Title(ctk.CTkLabel):
    def __init__(self, parent, fg_color):
        super().__init__(
            master=parent, fg_color=fg_color, text="IT exam auto solutions"
        )

        self.place(rely=0, relx=0, relheight=0.2, relwidth=1)


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, main_window):
        super().__init__(master=parent)
        # widgets
        self.button_import = ctk.CTkButton(self, text="Import image")

        self.label_paste = ctk.CTkLabel(
            self, text="or just paste an image from clipboard (press Ctrl-V)"
        )
        self.button_import.place(relx=0.5, rely=0.45, anchor="center")
        self.label_paste.place(relx=0.5, rely=0.55, anchor="center")
        # binding
        self.bind("<Motion>", lambda _: self.focus_set())
        self.bind("<Leave>", lambda _: main_window.focus_set())

        self.place(rely=0.25, relx=0, relheight=0.6, relwidth=1)


class ImageOutput(ctk.CTkCanvas):
    def __init__(self, parent, resize_image_func):
        super().__init__(
            master=parent,
            # relief="ridge",
            # background=color,
            highlightthickness=0,
        )

        self.pack(expand=True, fill="both")
        self.bind("<Configure>", resize_image_func)


class Answer(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            fg_color="red",
            text="Answer to your question is ...",
        )

        self.place(rely=0.9, relx=0, relheight=0.1, relwidth=1)


class LeftMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.textbox = Text(self)
        self.settings = Settings(self)

        self.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


class Settings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="yellow")

        ctk.CTkButton(self, text="Back to main menu").pack(expand=True)
        ctk.CTkButton(self, text="Help").pack(expand=True)

        self.place(rely=0.7, relx=0, relheight=0.25, relwidth=1)


class Text(ctk.CTkTextbox):
    def __init__(self, parent):
        super().__init__(master=parent, wrap="word", fg_color="blue")

        self.place(relx=0, rely=0, relheight=0.65, relwidth=1)
