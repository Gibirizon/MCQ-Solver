import asyncio

import customtkinter as ctk
import openai
from exam_widgets import (
    Answer,
    GetSolutionButton,
    ImageImport,
    ImageOutput,
    LeftMenu,
    MainContent,
    Settings,
    SettingsButtons,
    Text,
    Title,
)
from PIL import Image, ImageGrab, ImageTk
from pytesseract import get_languages, image_to_string
from settings import *
from start_menu import HelpWindow, StartMenu
from sydney import SydneyClient


class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("MayaBD")
        width = GEOMETRY[0]
        height = GEOMETRY[1]
        self.half_width = int((self.winfo_screenwidth() / 2) - (width / 2))
        self.half_height = int((self.winfo_screenheight() / 2) - (height / 2))
        self.geometry(f"{width}x{height}+{self.half_width}+{self.half_height}")
        self.minsize(GEOMETRY[0], GEOMETRY[1])

        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="b")
        self.start_menu = StartMenu(self, self.exam_layout)
        self.help_window = None

        self.mainloop()

    def exam_layout(self):
        self.start_menu.grid_forget()

        # main_content widgets
        self.main_content = MainContent(self)
        self.title = Title(self.main_content, "red")
        self.image_import = ImageImport(self.main_content, self)

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

    def paste_image(self, *args):
        if self.focus_get() == self.image_import:
            # working on image
            self.image = ImageGrab.grabclipboard()
            self.image_ratio = self.image.size[0] / self.image.size[1]
            self.image_tk = ImageTk.PhotoImage(image=self.image)

            # working on layout
            self.image_import.button_import.place_forget()
            self.image_import.label_paste.place_forget()

            self.image_import.image_output = ImageOutput(
                self.image_import, self.resize_image
            )
            self.write_solutions = GetSolutionButton(
                self.main_content,
                text="Get a solution to your question",
                func=self.get_solution,
            )
            self.settings.paste_next_question = SettingsButtons(
                self.settings.tab("Navigate"),
                text="Paste next question",
                func=self.reset_elements,
            )

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
        print(f"resizing image {event} {self.image_width} {self.image_height}")
        self.place_image()

    def place_image(self):
        # deleting all other images on canvas
        # self.image_import.image_output.delete("all")

        # resizing image
        resized_image = self.image.resize(
            (int(self.image_width), int(self.image_height))
        )
        self.image_tk = ImageTk.PhotoImage(image=resized_image)

        # placing image
        self.image_import.image_output.create_image(
            self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk
        )
        print("placing image")

    # komunikacja z Bing AI
    async def chatbot(self, text):
        async with SydneyClient(style="balanced") as sydney:
            response = await sydney.ask(
                text
            )  # compose_stream będę używał, jak będę dodawał informacje do Textboxa, żeby znaleźć odpowiedź użyję ask_stream
            print(response)
            self.textbox.insert("end", response)

    def get_solution(self):
        # zmiana obrazku na text
        self.text = image_to_string(image=self.image, lang="pol")
        print(self.text)

        # wywołanie funkcji komunikacji z Bing
        asyncio.run(self.chatbot(self.text))

        # changing/adding widgets
        self.settings.add("Export")
        self.settings.export_solution = SettingsButtons(
            self.settings.tab("Export"), "Save", self.export_solution
        )

        self.write_solutions.place_forget()

        self.answer = Answer(self.main_content)

    # button settings functions
    def help(self):
        if self.help_window is None or not self.help_window.winfo_exists():
            print("printing help")
            self.help_window = HelpWindow(
                self, self.half_width, self.half_height
            )  # create window if its None or destroyed
        else:
            self.help_window.focus()  # if window exists focus it

    def back_to_main_menu(self):
        print("going back to main menu")
        self.main_content.grid_forget()
        self.left_menu.grid_forget()
        self.start_menu = StartMenu(self, self.exam_layout)

    def reset_elements(self):
        print("reseting elements")
        self.main_content.grid_forget()
        self.left_menu.grid_forget()

        # main_content widgets
        self.main_content = MainContent(self)
        self.title = Title(self.main_content, "red")
        self.image_import = ImageImport(self.main_content, self)

        # left menu widgets
        self.left_menu = LeftMenu(self)
        self.settings = Settings(self.left_menu, self.help, self.back_to_main_menu)
        self.textbox = Text(self.left_menu)

    def export_solution(self):
        print("exporting solution")


if __name__ == "__main__":
    App()
