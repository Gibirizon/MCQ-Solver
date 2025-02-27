import customtkinter as ctk

from settings import Colors, Fonts, Geometry


class StartMenu(ctk.CTkFrame):
    def __init__(self, parent, func1, func2):
        super().__init__(master=parent, fg_color="transparent")
        font = ctk.CTkFont(
            family=Fonts.ANSWER,
            size=Fonts.ANSWER_SIZE,
            weight="bold",
            slant="italic",
        )
        StartButton(self, "IT exam", func1, font).pack(
            expand=True, ipadx=5, ipady=20, fill="x"
        )
        StartButton(self, "Help", func2, font).pack(
            expand=True, ipadx=5, ipady=20, fill="x"
        )

        self.place(relx=0.5, rely=0.5, relheight=0.5, relwidth=0.3, anchor="center")


class StartButton(ctk.CTkButton):
    def __init__(self, parent, text, func, font):
        super().__init__(
            master=parent,
            text=text,
            command=func,
            fg_color=Colors.BUTTON,
            hover_color=Colors.BUTTON_HOVER,
            font=font,
            corner_radius=Geometry.CORNER_RADIUS,
        )
