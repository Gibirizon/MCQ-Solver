import customtkinter as ctk


class StartMenu(ctk.CTkFrame):
    def __init__(self, parent, func1):
        super().__init__(master=parent, fg_color="transparent")

        ctk.CTkButton(master=self, text="IT exam", command=func1).pack(
            expand=True, ipadx=5, ipady=20, pady=10, padx=50, fill="x"
        )
        ctk.CTkButton(master=self, text="Help").pack(
            expand=True, ipadx=5, ipady=20, pady=10, padx=50, fill="x"
        )

        self.grid(row=0, column=1, columnspan=3, sticky="nsew", pady=100, padx=50)


class HelpWindow(ctk.CTkToplevel):
    def __init__(self, parent, screen_width, screen_height):
        super().__init__(master=parent)

        self.geometry(f"400x300+{screen_width}+{screen_height}")
        self.title("Help")

        ctk.CTkLabel(self, text="I'm here to help").pack(expand=True)
        ctk.CTkLabel(self, text="This program is used to ...").pack(expand=True)
