import asyncio

import customtkinter as ctk
import openai
from exam_widgets import (
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
from start_menu import StartMenu
from sydney import SydneyClient


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
        self.minsize(GEOMETRY[0], GEOMETRY[1])

        self.columnconfigure((0, 1, 2, 3, 4), weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="b")
        self.start_menu = StartMenu(self, self.exam_layout)

        self.mainloop()

    def exam_layout(self):
        self.start_menu.grid_forget()

        # main_content widgets
        self.main_content = MainContent(self)
        self.title = Title(self.main_content, "red")
        self.image_import = ImageImport(self.main_content, self)

        # left menu widgets
        self.left_menu = LeftMenu(self)
        self.settings = Settings(self.left_menu, self.help, self.back_to_main_menu)
        self.text = Text(self.left_menu)

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
                self.settings,
                text="Paste next question",
                func=self.reset_elements,
            )
            # i need to add other widgets !!!!!!!!!!!!!!!!!!!!!!!!!

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
        self.image_import.image_output.delete("all")

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

    def get_solution(self):
        # zmiana obrazku na text
        self.text = image_to_string(image=self.image, lang="pol")
        print(self.text)

        # komunikacja z Bing AI
        async def chatbot() -> None:
            async with SydneyClient(style="balanced") as sydney:
                async for response in sydney.ask_stream(
                    self.text
                ):  # compose_stream będę używał, jak będę dodawał informacje do Textboxa, żeby znaleźć odpowiedź użyję ask_stream
                    print(response, end="", flush=True)

        # wywołanie funkcji
        asyncio.run(chatbot())

    # button settings functions
    def help(self):
        print("help")

    def back_to_main_menu(self):
        print("back to main menu")

    def reset_elements(self):
        print("reseting elements")


if __name__ == "__main__":
    App()

# with a button, write solutions take text from image, then communicate with chatgpt

# add widgets after paste image

# change all widgets, wchich i'm working with to have immediately access to them
# what i mean is just calling them from main.py, not from exam_widgets
