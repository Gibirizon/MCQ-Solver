from enum import Enum
from pathlib import Path
from typing import cast

import customtkinter as ctk
from odf import teletype
from odf.draw import Frame
from odf.draw import Image as odfImage
from odf.opendocument import load
from odf.text import P
from PIL.Image import Image

from src.anki.connect_anki import Anki
from src.components.basic_widgets import CommonLabel, OptionMenu

from ...settings import Colors
from ...windows.user_information import InformationWindow
from .export_files import ExtendFile, NewFile
from .tabview_utils import SettingsButtons


class Settings(ctk.CTkTabview):
    def __init__(self, parent, back_func, help_func):
        super().__init__(
            master=parent,
            fg_color=Colors.SETTINGS_BG,
            segmented_button_fg_color=Colors.SETTINGS_SEGMENTED_BG,
            segmented_button_selected_color=Colors.SETTINGS_SELECTED_BUTTON,
            segmented_button_unselected_color=Colors.SETTINGS_SEGMENTED_BG,
            segmented_button_selected_hover_color=Colors.BUTTON_HOVER,
            segmented_button_unselected_hover_color=Colors.BUTTON_HOVER,
        )
        self.left_menu = parent
        # help window not visible at creation
        self.help_window = None

        # tabs
        self.add("Navigate")
        self.add("Help")

        # buttons for going back to main menu and getting help instructions
        SettingsButtons(
            self.tab("Navigate"),
            "Back to main menu",
            back_func,
        ).pack(expand=True)
        SettingsButtons(
            self.tab("Help"),
            "Help",
            help_func,
        ).pack(expand=True)

        # data
        self.file_path_string = ctk.StringVar()
        self.dir_path_string = ctk.StringVar()
        self.file_name_string = ctk.StringVar()

        # chosing export option
        self.export_option_string = ctk.StringVar(value=ExportOptions.ANKI.value)

        # anki deck option
        self.anki_deck_string = ctk.StringVar()

        self.place(rely=0.75, relx=0, relheight=0.25, relwidth=1)

    def create_button(self, tab: str, text: str, func):
        return SettingsButtons(self.tab(tab), text, func)

    def add_section_for_export(self, image: Image):
        # save image to later export it
        self.image = image

        # create new tab to export answer to a markdown/odt file
        self.add("Export")

        self.export_frame = ctk.CTkFrame(self.tab("Export"))
        self.export_frame.place(
            relx=0.5, rely=0.5, relheight=0.7, relwidth=0.5, anchor="center"
        )

        CommonLabel(self.export_frame, "Select export method:").pack(
            pady=5, expand=True
        )
        export_values = [option.value for option in ExportOptions]
        self.option_menu = OptionMenu(
            self.export_frame, self.export_option_string, export_values
        )

        SettingsButtons(
            self.export_frame,
            "Submit choice",
            self.choose_export_option,
        ).pack(expand=True)

    def choose_export_option(self):
        self.remove_options_layout()
        if self.export_option_string.get() == ExportOptions.NEW.value:
            self.new_file_layout()
        elif self.export_option_string.get() == ExportOptions.EXTEND.value:
            self.extend_file_layout()
        elif self.export_option_string.get() == ExportOptions.ANKI.value:
            self.anki_layout()

    def remove_options_layout(self):
        cast(SettingsButtons, self.option_menu).pack_forget()
        for child in self.export_frame.winfo_children():
            child.destroy()
        # cast(SettingsButtons, self.export_frame).place_forget()

    def anki_layout(self):
        self.anki_connection = Anki()
        CommonLabel(self.export_frame, "Select deck:").pack(pady=5, expand=True)
        decks = self.anki_connection.get_decks()
        self.anki_decks = OptionMenu(self.export_frame, self.anki_deck_string, decks)

        SettingsButtons(
            self.export_frame,
            "Add new note",
            self.add_new_anki_note,
        ).pack(expand=True)

    def new_file_layout(self):
        NewFile(
            self.tab(
                "Export",
            ),
            self.dir_path_string,
            self.file_name_string,
            self.export_solution,
        )

    def extend_file_layout(self):
        ExtendFile(
            self.tab("Export"),
            self.file_path_string,
            self.export_solution,
        )

    def add_new_anki_note(self):
        answer_text = self.left_menu.textbox.get("0.0", "end")
        status = self.anki_connection.add_note(
            self.anki_deck_string.get(), self.image, answer_text
        )
        # add information for user that note was created or not - TODO

    def export_solution(self, path):
        # have to first save img in script files, than take it from there
        dir_name = Path(__file__).parent
        full_image_path = dir_name / "temp_image.png"
        cast(Image, self.image).save(full_image_path)
        write_text = self.left_menu.textbox.get("0.0", "end")

        # adding image
        textdoc = load(path)
        p_img = P()
        textdoc.text.addElement(p_img)  # pyright: ignore
        photoframe = Frame(
            width=f"{cast(Image, self.image).size[0] / 2}pt",
            height=f"{cast(Image, self.image).size[1] / 2}pt",
            anchortype="paragraph",
        )
        href = textdoc.addPicture(full_image_path)
        photoframe.addElement(odfImage(href=href))
        p_img.addElement(photoframe)
        # adding text
        paragraph = P()
        teletype.addTextToElement(
            paragraph,
            write_text,
        )
        textdoc.text.addElement(paragraph)  # pyright: ignore
        # saving file
        textdoc.save(path)

        # remove img
        full_image_path.unlink(missing_ok=True)

        # message of success
        InformationWindow(self.left_menu.master, "Successfully saved file")


class ExportOptions(Enum):
    NEW = "Create new file"
    EXTEND = "Extend previously created file"
    ANKI = "Export to Anki deck"
