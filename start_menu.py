import customtkinter as ctk
import emoji
from exam_widgets import MainButtons, Text
from settings import *
from tabview_settings import CommonLabel


class StartMenu(ctk.CTkFrame):
    def __init__(self, parent, func1, func2):
        super().__init__(master=parent, fg_color="transparent")
        font = ctk.CTkFont(
            family=ANSWER_FONT, size=ANSWER_FONT_SIZE, weight="bold", slant="italic"
        )
        MainButtons(self, "IT exam", func1, font).pack(
            expand=True, ipadx=5, ipady=20, fill="x"
        )
        MainButtons(self, "Help", func2, font).pack(
            expand=True, ipadx=5, ipady=20, fill="x"
        )

        self.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.3, anchor="center")


class HelpWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(master=parent)
        width = HELP_GEOMETRY[0]
        height = HELP_GEOMETRY[1]
        half_width = int((self.winfo_screenwidth() / 2) - (width / 2))
        half_height = int((self.winfo_screenheight() / 2) - (height / 2))

        self.geometry(f"{width}x{height}+{half_width}+{half_height}")
        self.minsize(width, height)
        self.title("Help")

        self.help_title = CommonLabel(self, "How does this program work?")
        self.help_title.configure(
            font=ctk.CTkFont(family=TTITLE_FONT, size=ANSWER_FONT_SIZE)
        )
        self.help_title.pack(pady=5)

        self.help_text = Text(self)
        self.help_text.insert("end", HELP_TEXT)
        self.help_text.insert("end", emoji.emojize("Good luck! 	:grinning_face:"))

        self.help_text.configure(state="disabled")
        self.help_text.pack(expand=True, fill="both", padx=8, pady=5)
