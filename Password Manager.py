import tkinter as tk
import mysql.connector as c
import random

con = c.connect(host = 'localhost',user = 'root', passwd = 'root', database = 'passwordmanager')
cur = con.cursor()

uppercase = 'ABCDEFGHIJKLMNOPKRSTUVWXYX'
lst = list(uppercase)
lowercase = 'abcdefghijklmnopqrstuvwxyz'
lst.extend(list(lowercase))
numbers = '1234567890'
lst.extend(list(numbers))

window = tk.Tk()
window.title('Password Manager')
window.minsize(width = 250, height = 400)

def first_screen():
    for ele in window.winfo_children():
        ele.destroy()
    f1 = tk.Frame(window)
    f1.pack(fill = 'both')
    welcome = tk.Label(f1,text = 'Welcome to Password Manager!')
    welcome.pack(pady = 5)

    login_button = tk.Button(f1,text = 'Log in', width = 25, height = 3, bg = 'white', fg = 'black', command = login)
    login_button.pack(pady = 10)

    signup_button = tk.Button(f1,text = 'Sign up', width = 25, height = 3, bg = 'white', fg = 'black', command = signup)
    signup_button.pack()

    quit_button = tk.Button(f1, text = 'Quit', width = 25, height = 3, bg = 'white', fg = 'black', command = quit)
    quit_button.pack(pady = 10)
    owner = tk.Label(text = 'Made by Shaun Ramsay', font = ('TkDefaultFont', 10))
    owner.pack(side = tk.RIGHT, anchor = 's')

def login():

    for ele in window.winfo_children():
        ele.destroy()
    f2 = tk.Frame(window)
    f2.pack(fill = 'both')
    space = tk.Label(f2,text = ' ')
    space.pack()
    loginwelcome = tk.Label(f2,text = 'Log in')
    loginwelcome.pack()
    def check():
        global Username
        global con
        con.close()
        con = c.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'passwordmanager')
        cur = con.cursor()
        Username = username.get()
        Password = password.get()
        cur.execute('select* from profiles')
        r = cur.fetchall()
        if (Username,Password) not in r:
            msg = tk.Label(f2,text = 'Incorrect username or password entered.')
            msg.pack()
            username.delete(0,tk.END)
            password.delete(0,tk.END)
        else:
            menu()
    label = tk.Label(f2,text = 'Enter Username:')
    label.pack()
    username = tk.Entry(f2)
    username.pack()

    label = tk.Label(f2,text = 'Enter Password:')
    label.pack()
    password = tk.Entry(f2,show = '*')
    password.pack()
    login_button = tk.Button(f2,text = 'Log in', command = check)
    login_button.pack()
    home_button = tk.Button(text = 'Return to Home Screen', command = first_screen)
    home_button.pack(side = tk.BOTTOM)
    
def signup():
    for ele in window.winfo_children():
        ele.destroy()
    f3 = tk.Frame(window)
    f3.pack(fill = 'both')
    space = tk.Label(f3,text = ' ')
    space.pack()
    signupwelcome = tk.Label(f3,text = 'Sign up')
    signupwelcome.pack()
    def check():
        global con
        con.close()
        con = c.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'passwordmanager')
        cur = con.cursor()
        Username1 = username1.get()
        Password1 = password1.get()
        Confirm_password1 = confirm_password1.get()
        cur.execute('select* from profiles')
        r = cur.fetchall()
        username_check = True
        password_check = True
        for i in r:
            if Username1 == i[0]:
                msg = tk.Label(f3,text = 'Username already in use.')
                msg.pack()
                username_check = False
                break
        if Password1 != Confirm_password1:
            msg = tk.Label(f3,text = "Password does not match.")
            msg.pack()
            password_check = False
        if username_check == True and password_check == True:
            s = "insert into profiles values('{}','{}')".format(Username1,Password1)
            cur.execute(s)
            con.commit()
            success = tk.Label(f3,text = 'Profile successfully created!')
            success.pack()
        username1.delete(0,tk.END)
        password1.delete(0,tk.END)
        confirm_password1.delete(0,tk.END)
    username = tk.Label(f3,text = 'Username:')
    username.pack()
    username1 = tk.Entry(f3)
    username1.pack()

    password = tk.Label(f3,text = 'Password:')
    password.pack()
    password1 = tk.Entry(f3,show = '*')
    password1.pack()

    confirm_password = tk.Label(f3,text = 'Confirm password:')
    confirm_password.pack()
    confirm_password1 = tk.Entry(f3,show = '*')
    confirm_password1.pack()

    signup_button = tk.Button(f3,text = 'Sign up', command = check)
    signup_button.pack()

    home_button = tk.Button(text = 'Return to Home Screen', command = first_screen)
    home_button.pack(side = tk.BOTTOM)

def quit():
    window.destroy()

def add_():

    def generate():
        p = ''
        for i in range(6):
            char = random.choice(lst)
            p += char
        p += '-'
        for i in range(6):
            char = random.choice(lst)
            p += char
        p += '-'
        for i in range(6):
            char = random.choice(lst)
            p += char
        password.delete(0,tk.END)
        password.insert(0, p)
    def save_():
        global con
        global con1
        con.close()
        con = c.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'passwordmanager')
        con1 = c.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'passwordmanager')
        cur = con.cursor()
        cur1 = con1.cursor()
        
        Website = website.get()
        Password = password.get()
        cur1.execute(f"select website from passwords where username = '{Username}'")
        r = cur1.fetchall()
        unique = True
        for i in r:
            if Website in i:
                unique = False 
                break
        if Website == '' or Password == '':
            error = tk.Label(text = 'Please fill all the fields.')
            error.pack()
        elif unique != True:
            error2 = tk.Label(text = 'You already have a password saved for this website.')
            error2.pack()
        else:
            s = f"insert into passwords values('{Username}', '{Website}', '{Password}')"
            cur.execute(s)
            con.commit()
            website.delete(0, tk.END)
            password.delete(0, tk.END)
            if cur.rowcount > 0:
                success =  tk.Label(text = 'Password saved.')
                success.pack()
            
    for ele in window.winfo_children():
        ele.destroy()
    f_add = tk.Frame(window)
    f_add.pack(fil = 'both')

    title = tk.Label(text = 'Add Password')
    title.pack()

    website = tk.Label(text = 'Enter Website Name/URL:')
    website.pack(pady = 16)
    website = tk.Entry()
    website.pack()

    password = tk.Label(text = 'Enter Password:')
    password.pack()
    password = tk.Entry(width = 24)
    password.pack()

    Or = tk.Label(text = '(OR)')
    Or.pack(pady = 5)
    
    generate = tk.Button(text = 'Generate a Password', command = generate)
    generate.pack(pady = 5)

    save = tk.Button(text = 'Save Password', command = save_)
    save.pack(pady = 20)

    back = tk.Button(text = 'Back', command = menu)
    back.pack(side = tk.BOTTOM)
 

def view_():

    for ele in window.winfo_children():
        ele.destroy()

    f_view = tk.Frame(window)
    f_view.grid(column = 0, row = 0)
    
    back = tk.Button(text = 'Back', command = menu)
    back.grid(row = 1, column = 0)

    view = tk.Label(text = f"{Username}'s Saved Passwords:", font = ('SegoeUI 10 underline'))
    view.grid(row = 2, column = 0, pady = 5)

    global con
    con.close()
    con = c.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'passwordmanager')
    cur = con.cursor()
    s = f"select website, password from passwords where username = '{Username}'"
    cur.execute(s)
    r = cur.fetchall()

    if r == []:
        error = tk.Label(text = 'No Saved Passwords.')
        error.grid(row = 3, column = 0)
    for i in range(3,len(r)+3):
        j = i-3
        u = tk.Label(text = r[j][0])
        u.grid(row = i, column = 0, pady = 5)
        p = tk.Label(text = r[j][1])
        p.grid(row = i, column = 1)

def update_():

    def generate():

        p = ''
        for i in range(6):
            char = random.choice(lst)
            p += char
        p += '-'
        for i in range(6):
            char = random.choice(lst)
            p += char
        p += '-'
        for i in range(6):
            char = random.choice(lst)
            p += char
        password1.delete(0,tk.END)
        password1.insert(0, p)

    for ele in window.winfo_children():
        ele.destroy()

    global con
    con.close()
    con = c.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'passwordmanager')
    cur = con.cursor()

    f_update = tk.Frame(window)
    f_update.pack()

    title = tk.Label(text = 'Delete Password')
    title.pack()

    website = tk.Label(text = 'Enter Website:')
    website.pack(pady = 5)
    website1 = tk.Entry()
    website1.pack()
    
    password = tk.Label(text = 'Enter New Password:')
    password.pack(pady = 5)
    password1 = tk.Entry(width = 24)
    password1.pack()

    Or = tk.Label(text = '(OR)')
    Or.pack(pady = 5)
    generate = tk.Button(text = 'Generate a Password', command = generate)
    generate.pack(pady = 5)

    def updater():
        Website = website1.get()
        Password = password1.get()
        cur.execute(f"select website from passwords where username = '{Username}'")
        r = cur.fetchall()
        found = False
        for i in r:
            if Website in i:
                found = True
                s = f"update passwords set password = '{Password}' where username = '{Username}' and website = '{Website}'"
                cur.execute(s)
                con.commit()

                if cur.rowcount >0:
                    success =  tk.Label(text = f'Password updated for {Website}.')
                    success.pack()
                website1.delete(0, tk.END)
                password1.delete(0, tk.END)

        if found != True:
            error = tk.Label(text = f'No password saved for {Website}')
            error.pack()

    save = tk.Button(text = 'Update Password', command = updater)
    save.pack(pady = 16)

    back = tk.Button(text = 'Back', command = menu)
    back.pack(side = tk.BOTTOM)

def delete_():
    for ele in window.winfo_children():
        ele.destroy()

    global con
    con.close()
    con = c.connect(host = 'localhost', user = 'root', passwd = 'root', database = 'passwordmanager')
    cur = con.cursor()

    f_delete = tk.Frame(window)
    f_delete.pack()    

    title = tk.Label(text = 'Delete Website')
    title.pack()

    website = tk.Label(text = 'Enter Website:')
    website.pack(pady = 5)
    website1 = tk.Entry()
    website1.pack()

    def deleter():
        Website = website1.get()
        s = f"delete from passwords where website = '{Website}' and username = '{Username}'"
        cur.execute(s)
        con.commit()

        if Website == '':
            error = tk.Label(text = 'Please enter name of website.')
            error.pack(pady = 5)
        elif cur.rowcount > 0:
            success = tk.Label(text = "Website deleted successfully.")
            success.pack(pady = 5)
            website1.delete(0, tk.END)
    
    delete_button = tk.Button(text = 'Delete Website', command = deleter)
    delete_button.pack(pady = 5)

    back = tk.Button(text = 'Back', command = menu)
    back.pack(side = tk.BOTTOM)

def menu():
    for ele in window.winfo_children():
        ele.destroy()
    f4 = tk.Frame(window)
    f4.pack(fill = 'both')

    msg = tk.Label(f4,text = f"Welcome {Username}!")
    msg.pack()

    add = tk.Button(text = 'Add a Password', command = add_)
    add.pack(pady = 16)

    view = tk.Button(text = 'View Saved Passwords', command = view_)
    view.pack(pady = 16)

    update = tk.Button(text = 'Update a Password', command = update_)
    update.pack(pady = 16)

    delete = tk.Button(text = 'Delete a Website', command = delete_)
    delete.pack(pady = 16)

    logout = tk.Button(text = 'Log Out', command = first_screen)
    logout.pack(pady = 16)
    
first_screen()

window.mainloop()