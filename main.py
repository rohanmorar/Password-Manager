from tkinter import *
from tkinter import messagebox
from random import choice,randint,shuffle
from urllib.parse import urlparse
import pyperclip

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
        yes_click = messagebox.askyesno(title=website, message=f"Would you like to save the following informtion for {f_url}?\n\nEmail: {email}\nPassword: {password}")
        if yes_click:
            with open("data.txt", mode="a") as data_file:
                data_file.write(f"{website.upper()}\nUSERNAME| {email}\nPASSWORD| {password}\n\n")
                web_entry.delete(0, END)
                pass_entry.delete(0, END)
                web_entry.focus()
                window.clipboard_clear()
                pyperclip.copy(password)

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
web_entry = Entry(width=37,highlightbackground="white")
web_entry.focus()
email_entry = Entry(width=37,highlightbackground="white")
email_entry.insert(END, 'example@domain.com')
pass_entry = Entry(width=22,highlightbackground="white")
web_entry.grid(column=1,row=1,columnspan=2)
email_entry.grid(column=1,row=2, columnspan=2)
pass_entry.grid(column=1,row=3)

# Buttons
gen_pass_button = Button(text="Generate Password", highlightbackground="white",width=11,command=gen_pass)
gen_pass_button.grid(column=2,row=3)
add_button = Button(text="add", width=34, highlightbackground="white",command=save_password)
add_button.grid(column=1,row=4,columnspan=2)

window.mainloop()
