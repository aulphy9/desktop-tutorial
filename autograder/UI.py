import customtkinter as ctk
import ctypes
from PIL import Image
from autograder import main_function

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

csv_path = ""
selected_input_path = ""
expected_output_path = ""
selected_zip_path = ""

#class for final grading screen
class ThirdLevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x500")
        self.title("Grading: Step 3/3")

        #laurier logo at top (for consistencys sake)
        laurier_logo3 = ctk.CTkImage(light_image=Image.open("autograder\images\hawk.png"),
                                  dark_image=Image.open("autograder\images\hawk.png"),
                                  size=(150, 150))
        self.hawk_logo = ctk.CTkLabel(self, image=laurier_logo3, text="")  # display image with a CTkLabel
        self.hawk_logo.pack(pady=10)

        #title of window
        self.window_title = ctk.CTkLabel(self, text="Select your output folder and CSV template file:", font=("Berline Sans FB", 22))
        self.window_title.pack()
        self.window_title.place(x=60,y=180)

        #instructions to select csv file
        select_csv = """        Select the CSV file that holds each students information
        and upload information. This is downloaded from MyLS in the 
        dropbox submissions section."""

        #labels for selection process
        self.csv_select = ctk.CTkLabel(self, text=select_csv, font=("Calibri", 16))
        self.csv_select.pack()
        self.csv_select.place(x=50,y=230)

        self.csv_button = ctk.CTkButton(self, text="Select CSV File", command=self.get_csv_file, width=160, height=35)
        self.csv_button.pack()
        self.csv_button.place(x=210,y=310)

        #button to grade the submissions
        self.grade_submissions = ctk.CTkButton(self, text="Grade Submissions", command=self.grade_submission)
        self.grade_submissions.place(x=450,y=465)

    #function to get location of csv file with student information
    def get_csv_file(self):
        global csv_path
        file_path = ctk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path.endswith(".csv"):
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, 'You must select a csv file', 'Error', 0)
        else:
            csv_path = file_path
            self.display_input = ctk.CTkLabel(self, text=f"CSV grade file path: {csv_path}", font=("Calibri", 14))
            self.display_input.pack()
            self.display_input.place(x=75, y=360)


    #function that calls autograding software and updates csv file
    def grade_submission(self):
        print("-----------------------")
        print(csv_path)
        print(selected_input_path)
        print(selected_zip_path)
        print(expected_output_path)
        #main_function(selected_zip_path, selected_input_path, expected_output_path, csv_path)

#class window for getting expected input and output files
class SecondLevelWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x500")
        self.title("Grading: Step 2/3")
        self.third_level_window = None

        #laurier logo at top (for consistencys sake)
        laurier_logo2 = ctk.CTkImage(light_image=Image.open("autograder\images\hawk.png"),
                                  dark_image=Image.open("autograder\images\hawk.png"),
                                  size=(150, 150))
        self.hawk_logo = ctk.CTkLabel(self, image=laurier_logo2, text="")  # display image with a CTkLabel
        self.hawk_logo.pack(pady=10)

        #title of the window
        self.header_title = ctk.CTkLabel(self, text="Select your Sample Input and Expected Output Folders:", font=("Berline Sans FB", 22))
        self.header_title.place(x=45,y=180)

        #text for sample input selection
        sample_input_txt = """       Select your sample input folder 
        on your PC. Must have each 
        different test case on 
        their own respective lines."""

        #text for expected output selection
        expected_output_txt = """        Select your expected output folder for
        the proper output comparisons
        for each coding task."""

        #labels for instructions
        self.test_cases = ctk.CTkLabel(self, text=sample_input_txt, font=("Calibri", 16))
        self.test_cases.pack(padx=10)
        self.test_cases.place(x=15,y=220)

        self.expected_output = ctk.CTkLabel(self, text=expected_output_txt, font=("Calibri", 16))
        self.expected_output.pack(padx=10)
        self.expected_output.place(x=285, y=230)

        #buttons to get test case and expected output files
        self.get_input = ctk.CTkButton(self, text="Select sample input folder", command=self.get_sample_input, width=160, height=35) 
        self.get_input.place(x=70, y= 320)

        self.get_expected = ctk.CTkButton(self, text="Select expected output folder", command=self.get_expected_output, width=160, height=35)
        self.get_expected.place(x=350, y=320)

        #button to go to next window
        self.gotofinalwindow = ctk.CTkButton(self, text="Next step", command=self.open_thirdlevel)
        self.gotofinalwindow.place(x=450,y=465)

    #function to retrieve txt file of sample input from users local files
    def get_sample_input(self):
        global selected_input_path
        file_path = ctk.filedialog.askdirectory()
        selected_input_path = file_path
        print("Selected input file path: ", selected_input_path)
        self.display_input = ctk.CTkLabel(self, text=f"Sample input folder path: {selected_input_path}", font=("Calibri", 14))
        self.display_input.pack()
        self.display_input.place(x=75, y=360)
    
    #function to retrieve txt file of expected output from users local files
    def get_expected_output(self):
        global expected_output_path
        file_path = ctk.filedialog.askdirectory()
        expected_output_path = file_path
        print("Selected expected output file path: ", expected_output_path)
        self.display_output = ctk.CTkLabel(self, text=f"Expected output folder path: {expected_output_path}", font=("Calibri", 14))
        self.display_output.pack()
        self.display_output.place(x=75, y=380)
    
    #function to open up third window to select user input and expected output files
    def open_thirdlevel(self):
        self.wm_state('iconic')
        if self.third_level_window is None or not self.third_level_window.winfo_exists():
            self.third_level_window = ThirdLevelWindow(self)  # create window if its None or destroyed
            self.third_level_window.focus()
        else:
            self.third_level_window.focus()  # if window exists focus it

#window to select zip file for grading submissions
class ToplevelWindow(ctk.CTkToplevel):
    global selected_input_path
    global selected_zip_path
    global csv_path
    global expected_output_path

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x500")
        self.title("Grading: Step 1/3")
        laurier_logo1 = ctk.CTkImage(light_image=Image.open("autograder\images\hawk.png"),
                                  dark_image=Image.open("autograder\images\hawk.png"),
                                  size=(150, 150))
        self.hawk_logo = ctk.CTkLabel(self, image=laurier_logo1, text="")  # display image with a CTkLabel
        self.hawk_logo.pack(pady=10)
        selected_zip_path = ""
        
        #zip file select button
        self.button = ctk.CTkButton(self, text="Select Zip File", command=self.check_zip_file, width=160, height=35)
        self.button.pack(padx=20, pady=20)
        self.button.place(x=230, y=340)

        #title of the window
        self.header_title = ctk.CTkLabel(self, text="Select your MyLS Grading Zip File:", font=("Berline Sans FB", 22))
        self.header_title.pack()
        self.header_title.place(x=130,y=180)

        #window description
        text_zip = """        To start the grading process, hit the download submissions 
        button on MyLS dropbox submissons page and save the zip file
        on your PC. Upload it to the autograder by clicking the button 
        below to select the correct zip file."""
        self.zip_descrip = ctk.CTkLabel(self, text=text_zip, font=("Calibri", 16), anchor="center")
        self.zip_descrip.pack(padx=0,pady=0)
        self.zip_descrip.place(x=65,y=230)

        #button to go to next window
        self.open_input = ctk.CTkButton(self, text="Next Step", command=self.open_secondlevel)
        self.open_input.pack(padx=10,pady=10)
        self.open_input.place(x=450,y=465) #placing next
    
        #variable for next window
        self.second_level_window = None
    
    #function to retrieve zip file of submissions from users local files
    def check_zip_file(self):
        global selected_zip_path
        file_path = ctk.filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        if not file_path.endswith(".zip"):
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, 'You must select a zip file', 'Error', 0)
        else:
            selected_zip_path = file_path
            self.test_label = ctk.CTkLabel(self, text=f"Selected zip path: {selected_zip_path}", font=("Calibri", 14))
            self.test_label.place(x=90, y=400)
            print("Selected ZIP file:", selected_zip_path)

    #function to open up third window to select user input and expected output files
    def open_secondlevel(self):
        self.wm_state('iconic')
        if self.second_level_window is None or not self.second_level_window.winfo_exists():
            self.second_level_window = SecondLevelWindow(self)  # create window if its None or destroyed
            self.second_level_window.focus()
        else:
            self.second_level_window.focus()  # if window exists focus it
        
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #images
        laurier_logo = ctk.CTkImage(light_image=Image.open("autograder\images\hawk.png"),
                                  dark_image=Image.open("autograder\images\hawk.png"),
                                  size=(200, 200))
        python_logo = ctk.CTkImage(light_image=Image.open("autograder\images\pylogo.png"),
                                  dark_image=Image.open("autograder\images\pylogo.png"),
                                  size=(136, 146.9))
        java_logo = ctk.CTkImage(light_image=Image.open("autograder\images\javalogo.png"),
                                  dark_image=Image.open("autograder\images\javalogo.png"),
                                  size=(175, 175))
        #setting window size
        self.geometry("800x600")

        
        #button to go to zip file selection window
        self.button_1 = ctk.CTkButton(self, text="Start Grading", command=self.open_toplevel)
        self.button_1.pack()
        self.button_1.place(x=650, y=565)
        
        #golden hawk logo for fun
        self.hawk_logo = ctk.CTkLabel(self, image=laurier_logo, text="")  # display image with a CTkLabel
        self.hawk_logo.pack(pady=10)

        #title under golden hawk logo
        self.window_name = ctk.CTkLabel(self, text="Hawk Eye Autograder", font=("Berlin Sans FB", 32))
        self.window_name.pack(pady=10)
        self.window_name.place(x=250,y=240)

        #description label introducing the app and what it does
        description = """                     Welcome to the Hawk Eye Autograding platform. This application 
                        allows you to automate the marking process of Python and Java files
                        and projects. Simply download MyLearning Space submissions, provide 
                        your sample input and expected output, and mark all submissions. 
                        The next few windows will take you through the process. Click the 
                        start grading button below to begin."""
        self.title_description = ctk.CTkLabel(self, text=description, font=("Calibri", 16))
        self.title_description.pack(padx=1)
        self.title_description.place(x=55, y=285)

        #python logo
        self.pylogo = ctk.CTkLabel(self, image=python_logo, text="")  # display image with a CTkLabel
        self.pylogo.pack(pady=10)
        self.pylogo.place(x=200, y=420)

        #python logo
        self.jlogo = ctk.CTkLabel(self, image=java_logo, text="")  # display image with a CTkLabel
        self.jlogo.pack(pady=10)
        self.jlogo.place(x=400, y=400)
        
        self.toplevel_window = None

    def open_toplevel(self):
        self.wm_state('iconic')
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()  # if window exists focus it

app = App()
app.title("Hawk Eye Grading")
app.mainloop()