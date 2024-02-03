import customtkinter as ctk


class StartMenu(ctk.CTkFrame):
    def __init__(self, parent, func1):
        super().__init__(master=parent)

        ctk.CTkButton(master=self, text="IT exam", command=func1).pack(
            expand=True, ipadx=5, ipady=20, pady=10, padx=50, fill="x"
        )
        ctk.CTkButton(master=self, text="Settings").pack(
            expand=True, ipadx=5, ipady=20, pady=10, padx=50, fill="x"
        )
        ctk.CTkButton(master=self, text="Help").pack(
            expand=True, ipadx=5, ipady=20, pady=10, padx=50, fill="x"
        )

        self.grid(row=0, column=1, columnspan=3, sticky="nsew", pady=100, padx=50)
