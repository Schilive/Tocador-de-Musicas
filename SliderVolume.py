from tkinter import *


class SliderVolume(Frame):
    def __init__(self, parent, x=0, y=0, length_line=130, func=None, color="gray", **options):
        Frame.__init__(self, parent, **options)

        self.min_button = x  # Smallest x-position the slider may be and its starting position
        self.y = y  # The slider's y-position
        self.length = length_line  # The length of the slider's line
        self.func = func  # Fuction called when the slider's value changes
        self.color = color  # The color of the scaler's button

        # Draws the slider's line
        self.canvas = Canvas(parent, highlightthickness=0, borderwidth=0, height=self.winfo_reqheight(),
                             width=self.length)
        self.canvas.create_line(0, 0, self.length, 0, width=10)

        # The button, which is the slider itself
        self.button = Button(parent, text="", bg=self.color, activebackground=self.color, relief=SOLID, bd=0.2)
        self.max_button = self.length + self.min_button - self.button.winfo_reqwidth()  # Biggest x-position the
        # slider may be
        self.button.bind("<B1-Motion>", self.button_pressed)
        self.button.bind("<ButtonRelease-1>", self.button_released)

        # Places the widgets
        self.canvas.place(x=self.min_button, y=self.y + 12)
        self.button.place(x=self.min_button, y=self.y)

    def button_pressed(self, event):
        """Called when the button is both pressed and moved. Moves slider where the mouse is going to"""

        position = max(self.button.winfo_x() + event.x, self.min_button)  # Button's position to be
        position = min(position, self.max_button)
        self.button.place(x=position)

        if self.func is not None:
            self.func(self.get())

    def button_released(self, event):
        """Called when the button is released. Calls the function given as an argument"""

        if self.func is not None:
            self.func(self.get())

    def get(self):
        """The slider's value in percentage (0%–100%), which is (0–1)"""

        current_position = self.button.winfo_x()
        percentage_position = (current_position - self.min_button) / (self.max_button - self.min_button)
        return percentage_position

    def set(self, value_percentage):
        """Sets the slider's value in percentage"""

        position = value_percentage * (self.max_button - self.min_button) + self.min_button
        position = max(position, self.min_button)
        position = min(position, self.max_button)
        self.button.place(x=position)

