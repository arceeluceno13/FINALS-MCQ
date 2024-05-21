import os
import sys
from tkinter import Tk, Button, Label, Entry, PhotoImage, Frame, Text
from tkinter.filedialog import askopenfilename
from login_gui import LoginGUI
from exam_gui import ExamGUI
from file_handler import FileHandler
from user_input import UserInputGUI


class MainApp:
    def __init__(self):
        self.bg_color = "#292929"  # Black
        self.fg_color = "#fdd000"  # Yellow
        self.button_color = "#fdd000"
        self.login_gui = LoginGUI(self.bg_color, self.fg_color, self.button_color, self.center_window, self.create_gui)
        self.exam_gui = ExamGUI(self.bg_color, self.fg_color, self.button_color, self.center_window, self.is_cell_bold)
        self.file_handler = FileHandler()
        self.user_input_gui = UserInputGUI(self.bg_color, self.fg_color, self.exam_gui, self.button_color)

    def center_window(self, window, width=500, height=400):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        center_x = int((screen_width - width) / 2)
        center_y = int((screen_height - height) / 2)
        window.geometry(f"{width}x{height}+{center_x}+{center_y}")

    def create_gui(self):
        root = Tk()
        root.title("Teacher's Tool: MCQ Randomizer")
        root.geometry("1000x700")
        root.configure(bg=self.bg_color)

        self.center_window(root, 1000, 700)

        file_path = [None]

        def select_file():
            file_path[0] = askopenfilename(filetypes=[("Excel files", "*.xlsx")])

        def upload_file(event=None):
            time_limit = time_limit_entry.get()
            if not time_limit:
                error_label.config(text="Time limit is required.")
                return

            # Check if the time limit is a number
            if not time_limit.isdigit():
                error_label.config(text="Time limit must be a number.")
                return

            time_limit = int(time_limit)
            if time_limit < 0:
                error_label.config(text="Time limit cannot be negative.")
                return

            if not file_path[0]:
                error_label.config(text="No file selected.")
                return

            ws = self.file_handler.read_excel(file_path[0])
            if ws:
                root.destroy()
                # If time limit is 0, pass None instead
                self.user_input_gui.create(ws, None if time_limit == 0 else time_limit)

        frame = Frame(root, bg=self.bg_color)
        frame.pack()

        instructions = Text(frame, bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 12), wrap="word", height=9,
                            width=60, borderwidth=0)
        instructions.insert("1.0", "GOOD DAY, TEACHER!\n", "title")
        instructions.insert("2.0", "EXCEL FILE MUST BE IN THIS FORMAT\n\n", "title")
        instructions.insert("3.0", "1. All Questions Must be in Column A.\n", "normal")
        instructions.insert("4.0", "2. All Choices from A to D must be in column B to E.\n", "normal")
        instructions.insert("5.0", "NOTE: The entire question and its choices must be on row 1.\n", "bold")
        instructions.insert("6.0", "3. Cells with correct answers must be in BOLD Letters.\n", "normal")
        # instructions.insert("6.0", "Here's an example layout:\n", "normal")

        # Configure the "bold" tag to use a bold font
        instructions.tag_configure("bold", font=("Helvetica", 12, "bold"), justify="center")
        instructions.tag_configure("title", font=("Helvetica", 18, "bold"), justify="center")
        instructions.tag_configure("normal", font=("Helvetica", 12,), justify="center")

        instructions.config(state="disabled")
        instructions.pack(pady=(30, 0))

        example_label = Label(frame, text="KINDLY FOLLOW THIS EXAMPLE LAYOUT:",
                              fg=self.fg_color,
                              bg=self.bg_color,
                              font=("Helvetica", 12, "bold"))
        example_label.pack(pady=10)

        # Define the
        # source_path function
        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)

        # Use the resource_path function to get the path of the image
        guide_image = PhotoImage(file=resource_path("img\\guide.PNG"))
        image_label = Label(frame, image=guide_image, bg=self.bg_color)
        image_label.image = guide_image
        image_label.pack(pady=(0, 30))

        Label(frame, text="Time Limit (in minutes):",
              bg=self.bg_color,
              fg=self.fg_color,
              font=("Helvetica", 12)).pack()

        num_only = root.register(lambda input: input.isdigit() or input == "")
        time_limit_entry = Entry(frame, width=10, justify='center', validate="key",
                                 validatecommand=(num_only, "%P"),
                                 bg=self.bg_color,
                                 fg=self.fg_color,
                                 font=("Helvetica", 9))
        time_limit_entry.pack(pady=10)

        Label(frame, text="NOTE: You can input '0' to turn off the countdown timer",
              bg=self.bg_color,
              fg=self.fg_color,
              font=("Helvetica", 12, "bold")).pack()

        error_label = Label(frame, text="", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 9, "bold"))
        error_label.pack()

        select_button = Button(frame, text="UPLOAD EXCEL FILE", command=select_file,
                               bg=self.fg_color,
                               fg=self.bg_color,
                               font=("Helvetica", 12))
        select_button.pack(pady=10)

        upload_button = Button(frame, text="PROCEED TO QUIZ FORM", command=upload_file,
                               bg=self.fg_color,
                               fg=self.bg_color,
                               font=("Helvetica", 12, "bold"))
        upload_button.pack(pady=10)

        # Bind the ENTER key to the upload_file function
        root.bind('<Return>', upload_file)

        root.mainloop()

    def is_cell_bold(self, ws, row, col):
        cell = ws.cell(row=row, column=col)
        return cell.font.bold

    def run(self):
        self.login_gui.create()


if __name__ == "__main__":
    app = MainApp()
    app.run()