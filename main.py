import asyncio
from os.path import dirname, exists
from shlex import quote
from time import sleep

import customtkinter as ctk
from exam_widgets import (
    Answer,
    ImageImport,
    ImageOutput,
    LeftMenu,
    MainButtons,
    MainContent,
    Text,
    Title,
)
from odf import draw, teletype
from odf.draw import Frame, Image
from odf.opendocument import OpenDocumentText, load
from odf.text import P
from PIL import Image, ImageGrab, ImageTk
from pytesseract import image_to_string
from settings import *
from start_menu import HelpWindow, StartMenu
from sydney import SydneyClient
from tabview_settings import (
    ExtendFile,
    FileName,
    NewFilePath,
    Settings,
    SettingsButtons,
    SuccessSave,
)


class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("MayaBD")
        width = GEOMETRY[0]
        height = GEOMETRY[1]
        half_width = int((self.winfo_screenwidth() / 2) - (width / 2))
        half_height = int((self.winfo_screenheight() / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{half_width}+{half_height}")
        self.minsize(width, height)

        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="b")

        # data
        self.file_path_string = ctk.StringVar()
        self.dir_path_string = ctk.StringVar()
        self.file_name_string = ctk.StringVar()
        self.correct_answer = ctk.StringVar(value="...")

        # fonts
        self.primary_font = ctk.CTkFont(family=NORMAL_FONT, size=NORMAL_FONT_SIZE)
        self.answer_and_main_button_font = ctk.CTkFont(
            family=ANSWER_FONT, size=ANSWER_FONT_SIZE, weight="bold"
        )

        # start widgets
        self.start_menu = StartMenu(self, self.exam_layout, self.help)
        self.help_window = None

        self.mainloop()

    def exam_layout(self):
        self.start_menu.place_forget()

        # main_content widgets
        self.main_content = MainContent(self)
        self.main_title = Title(self.main_content)
        self.image_import = ImageImport(self.main_content, self, self.paste_image)

        # left menu widgets
        self.left_menu = LeftMenu(self)
        self.settings = Settings(
            self.left_menu,
            self.back_to_main_menu,
            self.help,
        )

        self.textbox = Text(self.left_menu)

        # bind to paste screenshot
        self.bind("<Control-KeyPress-v>", self.paste_image)

    def paste_image(self, _=None, path=None):
        if self.focus_get() == self.image_import:
            # working on image
            self.image = Image.open(path) if path else ImageGrab.grabclipboard()
            self.image_ratio = self.image.size[0] / self.image.size[1]
            self.image_tk = ImageTk.PhotoImage(image=self.image)

            # working on layout
            self.image_import.button_import.place_forget()
            self.image_import.label_paste.place_forget()

            self.image_import.image_output = ImageOutput(
                self.image_import, self.resize_image
            )
            self.write_solutions = MainButtons(
                self.main_content,
                "Get a solution to your question",
                self.get_solution,
                self.answer_and_main_button_font,
            )
            self.write_solutions.place(rely=0.9, relx=0, relheight=0.1, relwidth=1)
            SettingsButtons(
                self.settings.tab("Navigate"),
                text="Paste next question",
                func=self.reset_elements,
            ).pack(expand=True)

    def resize_image(self, event):
        self.canvas_ratio = event.width / event.height
        self.canvas_width = event.width
        self.canvas_height = event.height
        # checking is image ratio bigger than canvas ratio (which means i need to adjust width, image height will automatically be smaller than canvas height) or smaller than canvas ratio
        if self.image_ratio > self.canvas_ratio:
            self.image_width = event.width
            self.image_height = self.image_width / self.image_ratio
        else:
            self.image_height = event.height
            self.image_width = self.image_height * self.image_ratio
        self.place_image()

    def place_image(self):
        # resizing image
        resized_image = self.image.resize(
            (int(self.image_width), int(self.image_height))
        )
        self.image_tk = ImageTk.PhotoImage(image=resized_image)

        # placing image
        self.image_import.image_output.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk
        )

    # Bing AI
    async def chatbot(self, prompt):
        async with SydneyClient(style="balanced") as sydney:
            response = await sydney.compose(prompt)
            index = response.find("Odpowiedź:") + 11
            self.correct_answer.set(value=response[index])
            self.textbox.insert("end", response)

    def get_solution(self):
        # change image to text
        self.text = image_to_string(
            image=self.image,
            lang="pol",
        )

        # communication with Sydney - Bing (correct question)
        prompt = f'{PROMPT_EXPLANATION}"{self.text}"'
        asyncio.run(self.chatbot(prompt))

        # changing/adding widgets
        self.settings.add("Export")
        self.settings.new_file_button = SettingsButtons(
            self.settings.tab("Export"),
            "Create new file (required to add content to this file later)",
            self.new_file_layout,
        )
        self.settings.extend_file_button = SettingsButtons(
            self.settings.tab("Export"),
            "Extend previously created file",
            self.extend_file_layout,
        )
        self.settings.new_file_button.pack(expand=True)
        self.settings.extend_file_button.pack(expand=True)

        self.write_solutions.place_forget()

        self.answer = Answer(
            self.main_content,
            self.answer_and_main_button_font,
            self.correct_answer.get(),
        )

    # button settings functions
    def help(self):
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = HelpWindow(
                self
            )  # create window if its None or destroyed
        else:
            self.help_window.attributes("-topmost", True)

    def back_to_main_menu(self):
        self.main_content.grid_forget()
        self.left_menu.grid_forget()
        self.start_menu = StartMenu(self, self.exam_layout, self.help)

    def reset_elements(self):
        self.main_content.grid_forget()
        self.left_menu.grid_forget()

        # main_content widgets
        self.main_content = MainContent(self)
        self.main_title = Title(self.main_content)
        self.image_import = ImageImport(self.main_content, self, self.paste_image)

        # left menu widgets
        self.left_menu = LeftMenu(self)
        self.settings = Settings(self.left_menu, self.back_to_main_menu, self.help)
        self.textbox = Text(self.left_menu)

    def new_file_layout(self):
        self.settings.new_file_button.pack_forget()
        self.settings.extend_file_button.pack_forget()
        self.settings.new_file_frame = ctk.CTkFrame(
            self.settings.tab("Export"), fg_color="transparent"
        )
        self.settings.new_file_frame.place(
            relx=0.01, rely=0.01, relheight=0.75, relwidth=1
        )
        NewFilePath(self.settings.new_file_frame, self.dir_path_string)
        FileName(self.settings.new_file_frame, self.file_name_string, self.primary_font)
        SettingsButtons(
            self.settings.tab("Export"),
            "Create new file",
            lambda: self.create_new_file(
                self.dir_path_string.get(), self.file_name_string.get()
            ),
        ).place(relx=0.5, rely=0.87, anchor="center")

    def extend_file_layout(self):
        self.settings.new_file_button.pack_forget()
        self.settings.extend_file_button.pack_forget()
        ExtendFile(
            self.settings.tab("Export"),
            self.file_path_string,
            self.export_solution,
        )

    def create_new_file(self, path, file_name):
        full_path = f"{path}/{file_name}"
        if file_name[-4:] != ".odt":
            self.file_name_string.set("Invalid file extension")
            return
        elif exists(full_path):
            self.file_name_string.set("The file already exists")
            return
        textdoc = OpenDocumentText()
        textdoc.save(full_path)
        self.export_solution(full_path)

    def export_solution(self, path):

        # have to first save img in script files, than take it from there
        dir_name = dirname(__file__)
        full_image_path = f"{dir_name}/exam_img.png"
        self.image.save(full_image_path)
        write_text = self.textbox.get("0.0", "end")

        # adding image
        textdoc = load(path)
        p_img = P()
        textdoc.text.addElement(p_img)
        photoframe = Frame(
            width=f"{self.image.size[0]/2}pt",
            height=f"{self.image.size[1]/2}pt",
            anchortype="paragraph",
        )
        href = textdoc.addPicture(full_image_path)
        photoframe.addElement(draw.Image(href=href))
        p_img.addElement(photoframe)
        # adding text
        paragraph = P()
        teletype.addTextToElement(paragraph, write_text)
        textdoc.text.addElement(paragraph)
        # saving file
        textdoc.save(path)

        # communicate of success
        SuccessSave(self, self.answer_and_main_button_font)


if __name__ == "__main__":
    App()
