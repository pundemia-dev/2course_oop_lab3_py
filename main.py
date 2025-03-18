import customtkinter
from paint import Paint

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("ООП, Лабораторная работа №3.1")
        self.geometry(f"{350}x{510}")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.paint_action = Paint(master=self)
        self.paint_action.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()

