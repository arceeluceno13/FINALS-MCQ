from tkinter import Tk, Label, Entry, Button, StringVar, ttk

class UserInputGUI:
    def __init__(self, bg_color, fg_color, exam_gui, button_color):
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.exam_gui = exam_gui
        self.button_color = button_color

    def center_window(self, window, width=500, height=400):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        center_x = int((screen_width - width) / 2)
        center_y = int((screen_height - height) / 2)
        window.geometry(f"{width}x{height}+{center_x}+{center_y}")

    def create(self, ws, time_limit):
        user = Tk()  # Use Tk() instead of Toplevel()
        user.title("STUDENT INFORMATION")
        user.geometry("1000x700")
        user.configure(bg=self.bg_color)

        self.center_window(user, 1000, 700)

        validate_command = user.register(lambda input: input.isdigit() or input == "")
        title_label = Label(user, text="STUDENT INFORMATION", font=("Helvetica", 18, "bold"), bg=self.bg_color, fg=self.fg_color)
        title_label.place(relx=0.5, rely=0.1, anchor='center')

        Label(user, text="FIRST NAME:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 15)).place(relx=0.5, rely=0.2,anchor='center')
        fname_entry = Entry(user, bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 9), width=30, justify='center')
        fname_entry.place(relx=0.5, rely=0.25, anchor='center')

        Label(user, text="LAST NAME:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 15)).place(relx=0.5, rely=0.3, anchor='center')
        lname_entry = Entry(user, bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 9), width=30, justify='center')
        lname_entry.place(relx=0.5, rely=0.35, anchor='center')

        Label(user, text="COURSE:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 15)).place(relx=0.5,
                                                                                                      rely=0.4,
                                                                                                      anchor='center')
        course_var = StringVar(user)
        course_var.set("SELECT COURSE")  # default value
        course_options = ["BSIT", "DEVCOM", "HM", "TM", "BSED","BEED"]
        course_menu = ttk.Combobox(user, textvariable=course_var, values=course_options, state="readonly")
        course_menu.place(relx=0.5, rely=0.45, anchor='center')

        # Change the bg and fg color of the Combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.map('TCombobox',
                  fieldbackground=[('readonly', self.fg_color)],
                  fieldforeground=[('readonly', self.bg_color)],
                  selectbackground=[('readonly', self.fg_color)],
                  selectforeground=[('readonly', self.bg_color)])
        course_menu.config(style='TCombobox')
        style.configure('TCombobox', font=('Helvetica', 12))


        Label(user, text="YEAR LEVEL:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 15)).place(relx=0.5, rely=0.5, anchor='center')
        year_entry = Entry(user, bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 9), width=30, justify='center', validate="key", validatecommand=(validate_command, "%P"))
        year_entry.place(relx=0.5, rely=0.55, anchor='center')

        Label(user, text="SECTION:", bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 15)).place(relx=0.5, rely=0.6, anchor='center')
        section_entry = Entry(user, bg=self.bg_color, fg=self.fg_color, font=("Helvetica", 9), width=30, justify='center', validate="key", validatecommand=(validate_command, "%P"))
        section_entry.place(relx=0.5, rely=0.65, anchor='center')

        error_label = Label(user, bg=self.bg_color, fg=self.fg_color)
        error_label.place(relx=0.5, rely=0.8, anchor='center')

        def submit(event=None):
            fname = fname_entry.get().upper()
            lname = lname_entry.get().upper()
            course = course_var.get()
            year = year_entry.get()
            section = section_entry.get()

            if not fname or not lname or not year or not section or course == "Select Course":
                error_label.config(text="Name, Year, Section, and Course are required.")
                return

            if not year.isdigit() or int(year) > 4 or int(year) < 1:
                error_label.config(text="Year Level: Only 1 - 4 input.")
                return

            user.destroy()  # Destroy the UserInputGUI window after the user's information is submitted
            self.exam_gui.create(ws, time_limit, fname, lname, year, section, course)  # Call the create method of ExamGUI  # Call the create method of ExamGUI

        submit_button = Button(user, text="Start Quiz", command=submit, bg=self.fg_color, fg=self.bg_color)
        submit_button.place(relx=0.5, rely=0.75, anchor='center')  # Place the button at the center bottom of the window


        user.bind('<Return>', submit)
        
        user.mainloop()