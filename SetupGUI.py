import os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

window = tk.Tk()
window.title('Shortcut Script Setup')

lbl_email = tk.Label(text="Email")
ent_email = tk.Entry(width=50)
lbl_password = tk.Label(text="Password")
ent_password = tk.Entry(width=50, show='\u2022')

lbl_email.grid(row=0, column=0, columnspan=2, padx=3, pady=3)
ent_email.grid(row=0, column=2, sticky='nesw', columnspan=3, padx=3, pady=3)
lbl_password.grid(row=1, column=0, columnspan=2, padx=3, pady=3)
ent_password.grid(row=1, column=2, sticky='nesw', columnspan=3, padx=3, pady=3)

lbl_name = tk.Label(text='Shortcut Name')
ent_name = tk.Entry()
lbl_name.grid(row=2, column=0, columnspan=2, padx=3, pady=3)
ent_name.grid(row=2, column=2, columnspan=3, padx=3, pady=3)

exe_path = f'C:/Users/{os.getlogin()}/Documents/RealmOfTheMadGod/Production/RotMG Exalt.exe'

ent_path = tk.Entry(width=100)
ent_path.insert(0, exe_path)
ent_path.grid(row=3, column=1, columnspan=4, padx=3, pady=3)

def exe_path_callback():
    filename = askopenfilename(initialdir = f'C:/Users/{os.getlogin()}/Documents/RealmOfTheMadGod/Production', title = "Find your RotMG Client")
    ent_path.delete(0, 'end')
    ent_path.insert(0, filename)
    exe_path = filename

btn_browse = tk.Button(text='Browse', command=exe_path_callback, padx=3, pady=3)
btn_browse.grid(row=3, column=0)

shortcut_name = 'test'

def write_shortcut():
    shortcut_name = ent_name.get()
    with open(f'C:/Users/{os.getlogin()}/Desktop/{shortcut_name}.bat', 'w') as f:
        f.write('@ECHO OFF\n')
        f.write(f'set ROTMG_EMAIL={ent_email.get()}\n')
        f.write(f'set ROTMG_PASSWORD={ent_password.get()}\n')
        f.write(f'set ROTMG_PATH={exe_path}\n')
        f.write('"' + os.getcwd() + '/headless_launch.exe"')
    ent_email.delete(0, 'end')
    ent_password.delete(0, 'end')
    ent_name.delete(0, 'end')

    tk.messagebox.showinfo(title='Shortcut Created', message=f"Successfully created the shortcut {shortcut_name}.bat on your Desktop. Feel free to move the created shortcut wherever you'd like.")

btn_done = tk.Button(text='Make Shortcut Script', command=write_shortcut)
btn_done.grid(row=4, column=1, columnspan=3)

window.eval('tk::PlaceWindow . center')
window.mainloop()
