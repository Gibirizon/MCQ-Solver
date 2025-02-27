import customtkinter as ctk

from settings import Colors, Fonts


class Title(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            text="IT exam auto solutions",
            font=ctk.CTkFont(
                family=Fonts.TITLE,
                size=Fonts.TITLE_SIZE,
                slant="italic",
                weight="bold",
            ),
        )

        self.place(rely=0, relx=0, relheight=0.15, relwidth=1)


class Text(ctk.CTkTextbox):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            wrap="word",
            fg_color=Colors.TEXTBOX,
            font=ctk.CTkFont(family=Fonts.NORMAL, size=Fonts.NORMAL_SIZE),
            border_color=Colors.BORDER_TEXTBOX,
            border_width=2,
            border_spacing=10,
            corner_radius=15,
        )

        self.place(relx=0, rely=0, relheight=0.65, relwidth=1)


class CommonLabel(ctk.CTkLabel):
    def __init__(self, parent, text):
        super().__init__(
            master=parent,
            text=text,
            font=ctk.CTkFont(family=Fonts.NORMAL, size=Fonts.NORMAL_SIZE),
        )
