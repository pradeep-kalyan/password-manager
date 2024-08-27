from tkinter import messagebox
from tkinter import *
import random,string,subprocess,json,time
from cipher import Crypt
from idle_time import IdleMonitor
global shift
shift=random.randint(0,10)
shift=shift%26
crypt=Crypt()
# change the username and pasword  line 145 and 146
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def pwd_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]
    nr_letters=random.randint(8, 10)
    nr_sym=random.randint(1,3)
    nr_num=random.randint(1,4)
    pwd_ltr=[random.choice(letters) for i in range(nr_letters)]
    pwd_num=[random.choice(numbers) for i in range(nr_num)]
    pwd_sym=[random.choice(symbols) for i in range(nr_sym)]
    pwd_list=pwd_ltr+pwd_num+pwd_sym
    random.shuffle(pwd_list)
    pwd= "".join(pwd_list)
    pwdentry.insert(0, pwd)
    subprocess.run("pbcopy",text=True,input=pwd)
# _______________________________________________________________
alphabet=string.ascii_lowercase
# alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
def caeser(text,shift,direction):
    caeser=""
    if direction=="decode":
            shift=-shift
    for letter in text:
        if letter in alphabet:
          index=alphabet.index(letter)
          new_index = (index + shift) % 26
          caeser+=alphabet[new_index]
        else:
             caeser+=letter
    global pwd
    pwd=caeser
    return pwd
 # ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pwd():
    website = wbentry.get()
    old_pwd = pwdentry.get()
    email=unentry.get()
    passd=caeser(old_pwd,shift,"encode")
    newdata={website:{
            "Username" : email,
            "Password":passd
        }}
    if website == "" or old_pwd == "" or email=="":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty !")
    else:
        try:
            with open("data.json", "r") as data_file:
                data=json.load(data_file)
        except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(newdata,data_file,indent=5)
        else:
            data.update(newdata)
            with open("data.json", "w") as data_file:
                json.dump(data,data_file,indent=5)
                wbentry.delete(0, END)
                pwdentry.delete(0, END)
                crypt.encrypt("data.json")
# ------------------------------ SEARCH PASSWORD ------------------------------- #
def searpd():
    website=wbentry.get()
    try:
        with open("data.json", "r") as data_file:
            data=json.load(data_file)
            srch_res=data[website]
            passd=caeser(srch_res["Password"],shift,"decode")
            # data=srch_res["Password"]
            messagebox.showinfo(title=f"{website},website found",message=f"UserName :{srch_res["Username"]} ,\n Password : {passd}")
            subprocess.run("pbcopy",text=True,input=passd)
    except KeyError :
        messagebox.showinfo(title="KeyError",message="password not saved!!")

def logout():
    crypt.encrypt("data.json")
    messagebox.showinfo(title="Thank You",message="thank you for using our service")
    window.destroy()
# ------------------------------------------------------------------------USERNAME/PWD---------------
def user():
    inpnam=username.get()
    inppwd=password.get()
    if inpnam==user_n and inppwd==pwd_n:
        messagebox.showinfo(title="Welcome",message="Welcome to our service")
        # crypt.decrypt("data.json")
        username.grid_forget()
        password.grid_forget()
        btnck.grid_forget()
        unlab.grid_forget()
        pwdlab.grid_forget()
        wb = Label(text="Website : ")
        un = Label(text="Email/UserName : ")
        pwd = Label(text="Password : ")
        gp_btn = Button(text="Generate password ", command=pwd_gen)
        wb.grid(row=1, column=0, pady=5, padx=5)
        un.grid(row=2, column=0, pady=5, padx=5)
        pwd.grid(row=3, column=0, pady=5, padx=5)
        gp_btn.grid(row=3, column=2)
        global wbentry 
        wbentry = Entry(width=19)
        wbentry.focus()
        srch_p=Button(text="Search password",command=searpd)
        global unentry
        unentry = Entry(width=35)
        unentry.insert(0, "pradeepkalyan1275@gmail.com")
        global pwdentry
        pwdentry = Entry(width=19)
        wbentry.grid(row=1, column=1, pady=5, padx=5)
        srch_p.grid(row=1,column=2,padx=5,pady=5)
        unentry.grid(row=2, column=1, columnspan=2, pady=5, padx=5)
        pwdentry.grid(row=3, column=1, pady=5, padx=5)
        add_btn = Button(text="Add", width=35, command=save_pwd)
        add_btn.grid(row=4, column=1, columnspan=2)
        logout_btn=Button(text="logout",width=35,command=logout)
        logout_btn.grid(row=5,column=1,columnspan=2,pady=10)
    else:
        messagebox.showinfo(title="Login", message="Login Failed")
        username.delete(0,END)
        password.delete(0,END)
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.minsize(width=400, height=350)
window.config(padx=20, pady=20)
canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)
unlab=Label(text="Username : ")
unlab.grid(row=1,column=0)
pwdlab=Label(text="Password : ")
pwdlab.grid(row=2,column=0)
username=Entry(width=20)
password=Entry(width=20,show="*")
user_n="..."
pwd_n="...."
btnck=Button(text="login",command=user)
btnck.grid(row=3,column=1)
username.grid(row=1,column=1,columnspan=2)
password.grid(row=2,column=1,columnspan=2)
window.mainloop()
