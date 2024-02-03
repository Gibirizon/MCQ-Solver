import customtkinter as ctk
from exam_widgets import ImageOutput, LeftMenu, MainContent
from PIL import Image, ImageGrab, ImageTk
from settings import *
from start_menu import StartMenu


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
        # creating all of widgets
        self.start_menu.grid_forget()
        self.main_content = MainContent(self)
        self.left_menu = LeftMenu(self)
        self.bind("<Control-KeyPress-v>", self.paste_image)

    def paste_image(self, *args):
        if self.focus_get() == self.main_content.image_import:
            # working on image
            self.image = ImageGrab.grabclipboard()
            self.image_ratio = self.image.size[0] / self.image.size[1]
            self.image_tk = ImageTk.PhotoImage(image=self.image)

            # working on layout
            frame = self.main_content.image_import
            frame.button_import.place_forget()
            frame.label_paste.place_forget()
            frame.image_output = ImageOutput(frame, self.resize_image)

            # i need to add other widgets !!!!!!!!!!!!!!!!!!!!!!!!!

    def resize_image(self, event):
        self.canvas_ratio = event.width / event.height

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
        
        print("placing image")
        pass


if __name__ == "__main__":
    App()
