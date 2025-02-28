import customtkinter as ctk

from ..components.basic_widgets import CommonLabel
from ..settings import Fonts, Geometry


class InformationWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(master=parent)
        width = Geometry.SUCCEESS_SAVE[0]
        height = Geometry.SUCCEESS_SAVE[1]
        half_width = int((self.winfo_screenwidth() / 2) - (width / 2))
        half_height = int((self.winfo_screenheight() / 2) - (height / 2))

        self.geometry(f"{width}x{height}+{half_width}+{half_height}")
        self.minsize(width, height)
        self.title("Success")

        self.success_label = CommonLabel(self, "Successfully saved file")
        self.success_label.configure(
            font=ctk.CTkFont(
                family=Fonts.ANSWER,
                size=Fonts.ANSWER_SIZE,
                weight="bold",
            )
        )
        self.success_label.pack(expand=True, fill="both")
