from os.path import dirname
from typing import cast

import customtkinter as ctk
from odf import teletype
from odf.draw import Frame
from odf.draw import Image as odfImage
from odf.opendocument import load
from odf.text import P
from PIL.Image import Image

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

        self.place(rely=0.65, relx=0, relheight=0.35, relwidth=1)

    def create_button(self, tab: str, text: str, func):
        SettingsButtons(self.tab(tab), text, func).pack(expand=True)

    def add_section_for_export(self, image: Image):
        self.add("Export")
        self.new_file_button = SettingsButtons(
            self.tab("Export"),
            "Create new file (required to add content to this file later)",
            self.new_file_layout,
        )
        self.new_file_button.pack(expand=True)
        self.extend_file_button = SettingsButtons(
            self.tab("Export"),
            "Extend previously created file",
            self.extend_file_layout,
        )
        self.extend_file_button.pack(expand=True)
        # save image to later export it
        self.image = image

    def remove_button_in_export(self):
        cast(SettingsButtons, self.new_file_button).pack_forget()
        cast(SettingsButtons, self.extend_file_button).pack_forget()

    def new_file_layout(self):
        self.remove_button_in_export()
        NewFile(
            self.tab(
                "Export",
            ),
            self.dir_path_string,
            self.file_name_string,
            self.export_solution,
        )

    def extend_file_layout(self):
        self.remove_button_in_export()
        ExtendFile(
            self.tab("Export"),
            self.file_path_string,
            self.export_solution,
        )

    def export_solution(self, path):
        # have to first save img in script files, than take it from there
        dir_name = dirname(__file__)
        full_image_path = f"{dir_name}/exam_img.png"
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

        # message of success
        InformationWindow(self.left_menu.master)
