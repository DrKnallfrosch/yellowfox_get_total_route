from read_csv import readcsv
from tkinter import ttk
from calendar import monthrange
from remove_bg_website import remove_background
import tkinter as tk
import datetime
import process
import webbrowser
import os


# open a html document if something went wrong in progress.py you can read it to manually paste the .csv in the right
# dir
def help_():
    # Opens the help file in the browser
    # use search_files_in_directory to find the correct file. It also works if the file is an .exe file
    webbrowser.open(*search_files_in_directory(os.getcwd(), 'comment.html'))


def on_month_year_selected():
    # Gets the selected start and end month and year from the comboboxes
    start_selected_month = start_month_combobox.get()
    start_selected_year = start_year_combobox.get()
    end_selected_month = end_month_combobox.get()
    end_selected_year = end_year_combobox.get()

    # Dictionary to map month names to numbers
    month_dict = {
        "Januar": 1,
        "Februar": 2,
        "März": 3,
        "April": 4,
        "Mai": 5,
        "Juni": 6,
        "Juli": 7,
        "August": 8,
        "September": 9,
        "Oktober": 10,
        "November": 11,
        "Dezember": 12
    }
    start_month_number = month_dict.get(start_selected_month)
    end_month_number = month_dict.get(end_selected_month)
    return str(start_month_number), str(end_month_number), str(start_selected_year), str(end_selected_year)


def check_year():
    # Checks if the selected start and end year are the same and validates the input
    month = (start_month_combobox.get(), end_month_combobox.get())
    start_year = start_year_combobox.get()
    end_year = end_year_combobox.get()
    error_label = error

    if (start_year != end_year) or ((len(start_year)) != (len(end_year))):
        # Display error if years do not match
        second_error.place_forget()
        error_label.place(x=295, y=100)
    elif ((len(start_year) > 3) and (len(end_year) > 3)) and ((len(month[0]) and len(month[1])) > 2):
        # Proceed if input lengths are valid
        error_label.place_forget()
        second_error.place_forget()
        ttk_window_data()
    if not (len(start_year) > 2 or len(end_year) > 2 or (len(month[0]) > 2 and len(month[1]) > 2)):
        # Display error if any input length is invalid
        second_error.pack()
        second_error.place(x=275, y=100)


def ttk_window_data():
    def send():
        # Sends user data to process
        code = user_code_input.get()
        name = user_name_input.get()
        password = user_password_input.get()
        root.destroy()  # close the root window if button send was clicked
        start_year = start_year_combobox.get()
        end_year = end_year_combobox.get()
        end_day = monthrange(int(end_year), int(on_month_year_selected()[1]))
        try:
            process.process_main("1", on_month_year_selected()[0], start_year, str(end_day[1]),
                                 on_month_year_selected()[1], end_year, user_data=[code, name, password])
            going_ahead()
        except:
            # Display error button if processing fails
            error_button = ttk.Button(window, text="HELP", command=help_)
            error_button.pack()
            error_button.place(x=310, y=300)

            continue_button = continue_btn
            notice_label = notice_lbl
            continue_button.pack()
            continue_button.place(x=310, y=250)
            notice_label.pack()
            notice_label.place(x=195, y=230)

    # Create a new window for user data input
    root = tk.Tk()
    root.title('USER DATA')
    root.geometry('250x150')
    root.iconbitmap('icon/icon.ico')
    # Create a field to enter the user code
    user_code_label = ttk.Label(root, text="ENTER USER CODE:")
    user_code_label.pack()
    user_code_input = ttk.Entry(root)
    user_code_input.pack()
    # Create a field to enter the username
    user_name_label = ttk.Label(root, text="ENTER USERNAME:")
    user_name_label.pack()
    user_name_input = ttk.Entry(root)
    user_name_input.pack()
    # Create a field to enter the password. An input show a * to hidde the password
    user_password_label = ttk.Label(root, text="ENTER PASSWORD:")
    user_password_label.pack()
    user_password_input = ttk.Entry(root, show="•")
    user_password_input.pack()

    another_submit_button = ttk.Button(root, text='Send', command=send)
    another_submit_button.pack()

    root.mainloop()


def open_excel():
    # Opens the Excel file with vehicle data
    os.startfile(os.getcwd() + "/out/Fahrzeugdaten.xlsx")


def going_ahead():
    try:
        # Reads CSV data and sets up the next step
        readcsv()
        notice_lbl.forget()
        continue_btn.forget()
        open_excel_button = open_excel_btn
        open_excel_button.pack()
        open_excel_button.place(x=310, y=200)
    except IndexError:
        print("Empty 'csv_file' Folder")


def search_files_in_directory(directory, search_term):
    found_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(search_term):
                found_files.append(os.path.join(root, file))
    return found_files


current_path = os.getcwd()
# Create necessary directories and remove old files if they exist
if not os.path.exists(current_path + "/out/"):
    os.mkdir('out/')
elif os.path.isfile(current_path + '/out/VehicleData.xlsx'):
    os.remove(current_path + '/out/VehicleData.xlsx')
if not os.path.exists(current_path + "/csv_file/"):
    os.mkdir(current_path + '/csv_file/')
if not os.path.exists(current_path + '/icon/'):
    os.mkdir(current_path + '/icon/')
    remove_background("https://www.cooleru.de/wp-content/uploads/2022/09/cooleru-400x400.png",
                      "icon/icon.ico")

# Get the current year
date = datetime.date.today()
year = date.strftime("%Y")
year = int(year)

# Set up the main window
window = tk.Tk()
window.geometry("700x400")
window.title("Select Month and Year")
window.iconbitmap("icon/icon.ico")

start_label = ttk.Label(window, text="Start Month/Year")
start_label.pack()
start_label.place(x=100, y=0)

start_month_label = ttk.Label(window, text="Select Month:")
start_month_label.pack()
start_month_label.place(x=100, y=30)

start_month_combobox = ttk.Combobox(window, values=["Januar", "Februar", "März", "April", "Mai", "Juni",
                                                    "Juli", "August", "September", "Oktober", "November", "Dezember"])
start_month_combobox.pack()
start_month_combobox.place(x=100, y=50)

start_year_label = ttk.Label(window, text="Select Year:")
start_year_label.pack()
start_year_label.place(x=100, y=80)

start_year_combobox = ttk.Combobox(window, values=[f"{year - 2}", f"{year - 1}", f"{year}", f"{year + 1}"])
start_year_combobox.pack()
start_year_combobox.place(x=100, y=100)

end_label = ttk.Label(window, text="End Month/Year")
end_label.pack()
end_label.place(x=450, y=0)

end_month_label = ttk.Label(window, text="Select Month:")
end_month_label.pack()
end_month_label.place(x=450, y=30)

end_month_combobox = ttk.Combobox(window, values=["Januar", "Februar", "März", "April", "Mai", "Juni",
                                                  "Juli", "August", "September", "Oktober", "November", "Dezember"])
end_month_combobox.pack()
end_month_combobox.place(x=450, y=50)

end_year_label = ttk.Label(window, text="Select Year:")
end_year_label.pack()
end_year_label.place(x=450, y=80)

end_year_combobox = ttk.Combobox(window, values=[f"{year - 2}", f"{year - 1}", f"{year}", f"{year + 1}"])
end_year_combobox.pack()
end_year_combobox.place(x=450, y=100)

# Labels for errors
error = ttk.Label(window, text="Year range too high!", foreground="red", justify="center")
second_error = ttk.Label(window, text='Enter a value for each field!', foreground='red', justify="center")

# Button to open Excel file
open_excel_btn = ttk.Button(window, text="Open Excel", command=open_excel)

# Button to continue processing
continue_btn = ttk.Button(window, text="Continue", command=going_ahead)

# Notice label for CSV file
notice_lbl = ttk.Label(window, text="Add the CSV file to the csv_file folder and click Continue!")

# Submit button to validate and proceed
submit_button = ttk.Button(window, text="Select", command=check_year)
submit_button.pack()
submit_button.place(x=310, y=150)

# Label for processing time notice
processing_time_label = ttk.Label(window, text="Maximum processing time is ca. 24 minutes!")
processing_time_label.place(x=225, y=180)

window.mainloop()
