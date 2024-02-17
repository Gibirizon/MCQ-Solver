import customtkinter as ctk
from settings import *
from tabview_settings import CommonLabel, SettingsButtons


class MainContent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")

        # self.title = Title(self, "red")
        # self.image_import = ImageImport(self, parent)
        # self.answer = Answer(self)

        self.grid(row=0, column=2, columnspan=3, padx=25, pady=25, sticky="nsew")


class Title(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            text="IT exam auto solutions",
            font=ctk.CTkFont(
                family=TTITLE_FONT, size=TTITLE_FONT_SIZE, slant="italic", weight="bold"
            ),
        )

        self.place(rely=0, relx=0, relheight=0.15, relwidth=1)


class ImageImport(ctk.CTkFrame):
    def __init__(self, parent, main_window, image_func):
        super().__init__(master=parent, fg_color=IMAGE_FRAME_COLOR)

        self.image_func = image_func

        # widgets
        self.button_import = SettingsButtons(self, "Import image", self.open_dialog)

        self.label_paste = CommonLabel(
            self, "or just paste an image from clipboard (press Ctrl-V)"
        )
        self.button_import.place(relx=0.5, rely=0.4, anchor="center")
        self.label_paste.place(relx=0.5, rely=0.6, anchor="center")
        # binding
        self.bind("<Motion>", lambda _: self.focus_set())
        self.bind("<Leave>", lambda _: main_window.focus_set())

        self.place(rely=0.2, relx=0, relheight=0.65, relwidth=1)

    def open_dialog(self):
        path = ctk.filedialog.askopenfilename(
            filetypes=(
                ("image files", "*.jpg"),
                ("image files", "*.png"),
            ),
            title="Choose image",
            initialdir="/home",
        )
        if path:
            self.focus_set()
            self.image_func(path=path)


class ImageOutput(ctk.CTkCanvas):
    def __init__(self, parent, resize_image_func):
        super().__init__(
            master=parent,
            background=IMAGE_FRAME_COLOR,
            highlightthickness=0,
        )

        self.pack(expand=True, fill="both")
        self.bind("<Configure>", resize_image_func)


class Answer(ctk.CTkLabel):
    def __init__(self, parent, font, correct_answer_variable):
        super().__init__(
            master=parent,
            text=f"Correct answer is {correct_answer_variable}",
            fg_color=ANSWER_BACKGROUND_COLOR,
            text_color=ANSWER_TEXT_COLOR,
            corner_radius=CORNER_RADIUS,
            font=font,
        )

        self.place(rely=0.88, relx=0, relheight=0.1, relwidth=1)


class LeftMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")

        # self.textbox = Text(self)
        # self.settings = Settings(self)

        self.grid(row=0, column=0, columnspan=2, padx=25, pady=25, sticky="nsew")


class MainButtons(ctk.CTkButton):
    def __init__(self, parent, text, func, font):
        super().__init__(
            master=parent,
            text=text,
            command=func,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            font=font,
            corner_radius=CORNER_RADIUS,
        )


class Text(ctk.CTkTextbox):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            wrap="word",
            fg_color=TEXTBOX_COLOR,
            font=ctk.CTkFont(family=NORMAL_FONT, size=NORMAL_FONT_SIZE),
            border_color=BORDER_TEXTBOX_COLOR,
            border_width=2,
            border_spacing=10,
            corner_radius=15,
        )

        self.place(relx=0, rely=0, relheight=0.65, relwidth=1)
