import customtkinter as ctk
from PIL.Image import Image
from pytesseract import image_to_string

from .basic_widgets import RadioButton, Text, Title
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

    def add_elements(self, image: Image):
        """
        Method to add elements to main content after pasting image.
        We need to let user edit text from the image that was pasted
        as the text will not always be properly processed from the photo.
        This method adds editor box and button to get solution.
        Moreover it create two radio buttons
        to let the user choose to generate response from the text in editor
        or from the image itself.
        """
        self.question_editor = Text(self)
        self.question_editor.place(relx=0, rely=0.6, relheight=0.25, relwidth=1)

        mode_choice = ctk.StringVar(value="text")

        self.add_radiobuttons(mode_choice)
        self.question_editor.insert(
            "end", get_text_from_img(image)
        )  # add text from image to the editor, because if there is image on screenshot text won't be always correct and then user can edit it or choose to generate response by providing image to AI

        SolutionButton(
            self,
            "Generate answer to the question",
            image,
            main_window=self.main_window,
            question_editor=self.question_editor,
            mode=mode_choice,
        )

    def add_radiobuttons(self, mode_choice: ctk.StringVar):
        self.frame_for_radiobuttons = ctk.CTkFrame(self)
        RadioButton(
            self.frame_for_radiobuttons,
            text="Generate repsonse from the text above",
            variable=mode_choice,
            value="text",
        ).pack(side="left", padx=10)
        RadioButton(
            self.frame_for_radiobuttons,
            text="Generate repsonse with image",
            variable=mode_choice,
            value="image",
        ).pack(side="right", padx=10)
        self.frame_for_radiobuttons.place(relx=0, rely=0.87, relheight=0.05, relwidth=1)

    def remove_elements(self):
        self.question_editor.place_forget()
        self.frame_for_radiobuttons.place_forget()


class LeftMenu(ctk.CTkFrame):
    def __init__(self, parent, back_to_main_menu_func, help_func):
        super().__init__(master=parent, fg_color="transparent")
        self.settings = Settings(
            self, back_func=back_to_main_menu_func, help_func=help_func
        )
        self.textbox = Text(self)
        self.textbox.place(relx=0, rely=0, relheight=0.70, relwidth=1)

        self.grid(row=0, column=0, columnspan=2, padx=25, pady=25, sticky="nsew")

    def add_solution(self, solution: str):
        self.textbox.insert("end", solution)


def get_text_from_img(image: Image):
    text = image_to_string(
        image=image,
        lang="pol",
    )
    return text
