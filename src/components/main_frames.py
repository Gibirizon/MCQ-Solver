import customtkinter as ctk

from .basic_widgets import Text, Title
from .image import ImageImport
from .solution import SolutionButton
from .tabview.tabview_settings import Settings


class MainContent(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color="transparent")
        self.main_window = parent

        Title(self)
        self.image_import = ImageImport(
            self,
            self.main_window,
        )

        self.grid(row=0, column=2, columnspan=3, padx=25, pady=25, sticky="nsew")

    def create_answer_button(self, image):
        SolutionButton(
            self, "Get an answer to your question", image, main_window=self.main_window
        )


class LeftMenu(ctk.CTkFrame):
    def __init__(self, parent, back_to_main_menu_func, help_func):
        super().__init__(master=parent, fg_color="transparent")
        self.settings = Settings(
            self, back_func=back_to_main_menu_func, help_func=help_func
        )
        self.textbox = Text(self)

        self.grid(row=0, column=0, columnspan=2, padx=25, pady=25, sticky="nsew")

    def add_solution(self, solution: str):
        self.textbox.insert("end", solution)
