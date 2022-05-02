from tkinter import *
from tkinter import messagebox
from random import choice,randint,shuffle
from urllib.parse import urlparse
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)
    random_pass = "".join(password_list)

    pass_entry.delete(0,END)
    pass_entry.insert(0, random_pass)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    email = email_entry.get()
    website = web_entry.get()
    password = pass_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    # Checks for empty input fields, and notify user if there are
    parsed_url = urlparse(website).netloc
    f_url = '.'.join(parsed_url.split('.')[-2:]).capitalize()

    if len(f_url) == 0:
        f_url = website

    if len(website) == 0 or len(password) == 0:
        retry = messagebox.askretrycancel(title=website, message = "You are missing an entry.\nFill-in all boxes and try again.")
        if retry:
            return
        else:
            web_entry.delete(0, END)
            pass_entry.delete(0, END)
    else:
        # read from data.json file if it exists
        try: 
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)

        # create data.json if it has not been created 
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)

        # Else, data.json exists and we update it with a new_data item (runs if no issues)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", mode="w") as data_file:

                # Saving updated data   
                json.dump(data, data_file, indent = 4)
    
        # After everything, we reset the entries (runs if fails or succeeds)
        finally:
            web_entry.delete(0, END)
            pass_entry.delete(0, END)
            web_entry.focus()
            window.clipboard_clear()
            pyperclip.copy(password)

# ---------------------------- SEARCH SAVED PASSWORDS ------------------------------- #
def search():
    website = web_entry.get()

    # gets key from json using website name
    # returns pop-up message w email and pass
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.askokcancel(message = "No details found for your website search.")
    else:   
        if website in data.keys():
            user = data[web_entry.get()]["email"]
            pswd = data[web_entry.get()]["password"]
            messagebox.askokcancel(title=website, message = f"User: {user}\nPass: {pswd}")
        else:
            messagebox.askokcancel(message = "No details found for your website search.")
                
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password manager")
window.config(bg = "white", padx = 20, pady = 20)
window.resizable(False,False)
window_height = 370
window_width = 540
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

# Image
canvas = Canvas(width = 200, height = 200, highlightthickness = 0, bg = "white")
logo_img = PhotoImage(file="logo.png")
window.config(padx=40,pady=20)
canvas.create_image(100, 100, image = logo_img)
canvas.grid(column=1,row=0,sticky="e")

# Labels
web_label = Label(text="Website:", bg="white")
email_label = Label(text="Email/Username:", bg="white")
pass_label = Label(text="Password:", bg="white")
web_label.grid(column=0,row=1)
email_label.grid(column=0,row=2)
pass_label.grid(column=0,row=3)

# Entries
web_entry = Entry(width=22,highlightbackground="white")
web_entry.focus()
email_entry = Entry(width=37,highlightbackground="white")
email_entry.insert(END, 'example@domain.com')
pass_entry = Entry(width=22,highlightbackground="white")
web_entry.grid(column=1,row=1)
email_entry.grid(column=1,row=2, columnspan=2)
pass_entry.grid(column=1,row=3)

# Buttons
gen_pass_button = Button(text="Generate Password", highlightbackground="white",width=11,command=gen_pass)
gen_pass_button.grid(column=2,row=3)
add_button = Button(text="add", width=34, highlightbackground="white",command=save_password)
add_button.grid(column=1,row=4,columnspan=2)
search_button = Button(text="Search", highlightbackground="white",width=11,command=search)
search_button.grid(column=2,row=1)

window.mainloop()
