from AES import *
from Functions import *
from tkinter import Tk, Label, Entry, Button, Toplevel, ttk, StringVar, \
    IntVar, Checkbutton, Frame, Canvas, Scrollbar

# # Read the JSON files
# PASSWORDS = read_json_file("PASSWORDS.json", [])
# CHARACTER_SETS = read_json_file("CHARACTER_SETS.json", {})

# Read from online DB
PASSWORDS = db_PASSWORDS.get()
CHARACTER_SETS = db_CHARACTER_SETS.get()
if PASSWORDS is None:
    PASSWORDS = []
if CHARACTER_SETS is None:
    CHARACTER_SETS = {}

# List of all the special characters available
Special_Characters = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                      "_", "-", "+", "=", "{", "}", "[", "]", "|", ":", ";", "'",
                      "<", ">", ",", ".", "?", "/"]


def account_combobox_selected(index):
    root.focus()
    Button_modify_password.config(state='normal')
    selected_password = PASSWORDS[index]
    email_string_var.set(selected_password.get("e_mail"))
    extra_string_var.set(selected_password.get("extra"))
    text_to_cript = "myPassword!!" + selected_password.get("version") + selected_password.get("password_id")
    add_to_clipboard(get_password(text_to_cript,
                                  Entry_main_password.get(),
                                  CHARACTER_SETS.get(selected_password.get("character_list"))))


def get_password(pass_text, key_text, char_list):
    # ensuring that key_text is at least 16 characters long
    while len(key_text) < 16:
        key_text += "0"

    pass_state = text_to_state(pass_text)
    key_state = text_to_state(key_text)
    return state_to_text(crypt(pass_state, key_state), char_list)


def character_sets_combobox_selected(window_npw):
    window_npw.focus()


def create_modify_password_window(index):
    npw = Toplevel(root)  # new password window
    npw.title("New Password" if index == -1 else "Modify Password")
    npw.protocol("WM_DELETE_WINDOW", lambda: close_new_window(npw))
    root.state('withdrawn')

    if index == -1:
        if len(PASSWORDS) == 0:
            id_num = 0
        else:
            id_num = max([int(p.get("password_id")) for p in PASSWORDS])+1
    else:
        id_num = PASSWORDS[index].get("password_id")

    label_name = Label(npw, text="Name:")
    label_name.pack()

    entry_name = Entry(npw, width=WIDTH)
    entry_name.pack()
    if index != -1:
        entry_name.insert(0, PASSWORDS[index].get("name"))

    label_email = Label(npw, text="Email:")
    label_email.pack()

    entry_email = Entry(npw, width=WIDTH)
    entry_email.pack()
    if index != -1:
        entry_email.insert(0, PASSWORDS[index].get("e_mail"))

    label_extra = Label(npw, text="Extra:")
    label_extra.pack()

    entry_extra = Entry(npw, width=WIDTH)
    entry_extra.pack()
    if index != -1:
        entry_extra.insert(0, PASSWORDS[index].get("extra"))

    label_version = Label(npw, text="Version:")
    label_version.pack()

    if index == -1:
        version_string_var.set("0")
    else:
        version_string_var.set(PASSWORDS[index].get("version"))
    entry_version = Entry(npw, width=WIDTH, state="readonly", textvariable=version_string_var)
    entry_version.pack()

    button_increment = Button(npw, text="+", command=increment_button_pressed)
    button_increment.pack()

    label_character_set = Label(npw, text="Character set:")
    label_character_set.pack()

    cbb_character_list = ttk.Combobox(npw,
                                      width=WIDTH - 5,
                                      state="readonly",
                                      values=list(CHARACTER_SETS.keys()))
    cbb_character_list.pack()
    cbb_character_list.bind("<<ComboboxSelected>>", lambda event: character_sets_combobox_selected(npw))
    if index != -1:
        cbb_character_list.set(PASSWORDS[index].get("character_list"))

    button_add_modify_password = Button(npw,
                                        text="Add" if index == -1 else "Modify",
                                        command=lambda: add_modify_password(npw,
                                                                            entry_name.get(),
                                                                            entry_email.get(),
                                                                            entry_extra.get(),
                                                                            entry_version.get(),
                                                                            cbb_character_list.get(),
                                                                            id_num,
                                                                            index)
                                        )
    button_add_modify_password.pack()


def add_modify_password(window, name, email, extra, version, charcater_set, num_id, index):
    # index is -1 for adding and an integer for modify
    new_password_dict = {"name": name,
                         "e_mail": email,
                         "password_id": id_num_to_str(num_id),
                         "version": version,
                         "character_list": charcater_set,
                         "extra": extra}
    if index == -1:  # adding
        PASSWORDS.append(new_password_dict)
    else:  # modify
        PASSWORDS[index] = new_password_dict

    PASSWORDS.sort(key=lambda x: x['name'].lower())
    # write_json_file("PASSWORDS.json", PASSWORDS)
    db_PASSWORDS.set(PASSWORDS)
    close_new_window(window)


def confirm_new_character_set(window, set_name, bool_a_z, bool_capa_capz, bool_0_9, bool_special_characters):
    new_set = []
    if bool_a_z:
        new_set.extend(["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                        "s", "t", "u", "v", "w", "x", "y", "z"])
    if bool_capa_capz:
        new_set.extend(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                        "S", "T", "U", "V", "W", "X", "Y", "Z"])
    if bool_0_9:
        new_set.extend(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

    new_set.extend([char for char, bool_var in zip(Special_Characters, bool_special_characters) if bool_var.get() == 1])

    CHARACTER_SETS[set_name] = new_set
    # write_json_file("CHARACTER_SETS.json", CHARACTER_SETS)
    db_CHARACTER_SETS.set(CHARACTER_SETS)
    close_new_window(window)


def create_new_character_set():
    ncsw = Toplevel(root)  # new character set window
    ncsw.title("New Character Set")
    ncsw.protocol("WM_DELETE_WINDOW", lambda: close_new_window(ncsw))
    root.state('withdrawn')

    label_name = Label(ncsw, text="Name:")
    label_name.pack()

    entry_name = Entry(ncsw, width=WIDTH)
    entry_name.pack()

    bool_az = IntVar()
    checkbutton_az = Checkbutton(ncsw, text="a-z", variable=bool_az, onvalue=1, offvalue=0)
    checkbutton_az.pack(padx=PADX, pady=PADY)

    bool_cap_a_cap_z = IntVar()
    checkbutton_cap_a_cap_z = Checkbutton(ncsw, text="A-Z", variable=bool_cap_a_cap_z, onvalue=1, offvalue=0)
    checkbutton_cap_a_cap_z.pack(padx=PADX, pady=PADY)

    bool_0_9 = IntVar()
    checkbutton_0_9 = Checkbutton(ncsw, text="0-9", variable=bool_0_9, onvalue=1, offvalue=0)
    checkbutton_0_9.pack(padx=PADX, pady=PADY)

    main_frame = Frame(ncsw)
    main_frame.pack(expand=1, fill="both")

    # Create a canvas for scrolling
    canvas = Canvas(main_frame)
    canvas.pack(side="left", fill="both", expand=1)

    # Add a scrollbar to the canvas
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame inside the canvas to hold the checkbuttons
    checkbutton_frame = Frame(canvas)

    # Add the frame to the canvas window
    canvas.create_window((0, 0), window=checkbutton_frame, anchor="nw")

    bool_check_vars = []
    # Create checkbuttons in a loop
    for i, char in enumerate(Special_Characters):
        var = IntVar()  # Create a new IntVar for each checkbutton
        bool_check_vars.append(var)  # Store the IntVar in a list

        # Create a Checkbutton with the character as its label
        checkbutton = Checkbutton(checkbutton_frame, text=char, variable=var, onvalue=1, offvalue=0)
        checkbutton.pack(padx=PADX, pady=PADY)

    button_confirm_new_character_set = Button(ncsw,
                                              text="Add",
                                              command=lambda: confirm_new_character_set(ncsw,
                                                                                        entry_name.get(),
                                                                                        bool_az.get(),
                                                                                        bool_cap_a_cap_z.get(),
                                                                                        bool_0_9.get(),
                                                                                        bool_check_vars)
                                              )
    button_confirm_new_character_set.pack()


def close_new_window(new_window):
    new_window.destroy()
    root.deiconify()
    Combobox_account.config(values=[p.get("name") for p in PASSWORDS])
    Combobox_account.set('')
    email_string_var.set('')
    extra_string_var.set('')


def increment_button_pressed():
    version_string_var.set(increment_string(version_string_var.get()))


root = Tk()
root.title("PASSWAN")
root.resizable(False, False)

version_string_var = StringVar()
email_string_var = StringVar()
extra_string_var = StringVar()

WIDTH = 40
PADX = 10
PADY = 2

Label_main_password = Label(root, text="Main Password:")
Label_main_password.pack(padx=PADX, pady=PADY)

Entry_main_password = Entry(root, width=WIDTH, show='*')
Entry_main_password.pack(padx=PADX, pady=PADY)

Label_email = Label(root, text="Email:")
Label_email.pack(padx=PADX, pady=PADY)

Entry_email = Entry(root, width=WIDTH, state="readonly", textvariable=email_string_var)
Entry_email.pack(padx=PADX, pady=PADY)

Label_extra = Label(root, text="Extra:")
Label_extra.pack(padx=PADX, pady=PADY)

Entry_extra = Entry(root, width=WIDTH, state="readonly", textvariable=extra_string_var)
Entry_extra.pack(padx=PADX, pady=PADY)

Combobox_account = ttk.Combobox(root, width=WIDTH - 5, state="readonly", values=[p.get("name") for p in PASSWORDS])
Combobox_account.bind("<<ComboboxSelected>>",
                      lambda event: account_combobox_selected(Combobox_account.current()))
Combobox_account.pack(padx=PADX, pady=PADY)

Button_new_password = Button(root,
                             text="Add New Password",
                             command=lambda: create_modify_password_window(-1)
                             )
Button_new_password.pack(padx=PADX, pady=PADY)

Button_modify_password = Button(root,
                                text="Modify Password",
                                command=lambda: create_modify_password_window(Combobox_account.current()),
                                state="disabled")
Button_modify_password.pack(padx=PADX, pady=PADY)

Button_new_character_set = Button(root, text="Add New Character Set", command=create_new_character_set)
Button_new_character_set.pack(padx=PADX, pady=PADY)

root.mainloop()
