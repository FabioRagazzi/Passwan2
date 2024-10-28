from tkinter import messagebox, IntVar, StringVar
from PIL import Image
from AES import *
from Functions import *
import customtkinter
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# List of all the special characters available
Special_Characters = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                      "_", "-", "+", "=", "{", "}", "[", "]", "|", ":", ";", "'",
                      "<", ">", ",", ".", "?", "/"]

# Loading the settings
with open("SETTINGS.json", 'r') as settings_file:
    SETTINGS = json.load(settings_file)

if SETTINGS["MODE"] == "JSON":
    # Read the JSON files
    PASSWORDS = read_json_file(SETTINGS["PATH_OF_JSON_DATA"]+"PASSWORDS.json", [])
    CHARACTERS_SETS = read_json_file(SETTINGS["PATH_OF_JSON_DATA"]+"CHARACTERS_SETS.json", {})
elif SETTINGS["MODE"] == "DATABASE":
    # Read from online DB
    cred = credentials.Certificate(SETTINGS["PATH_OF_CERTIFICATE"])
    firebase_admin.initialize_app(cred,
                                  {'databaseURL': SETTINGS["DATABASE_URL"]})

    db_PASSWORDS = db.reference('PASSWORDS')
    db_CHARACTERS_SETS = db.reference('CHARACTERS_SETS')
    PASSWORDS = db_PASSWORDS.get()
    CHARACTERS_SETS = db_CHARACTERS_SETS.get()
    if PASSWORDS is None:
        PASSWORDS = []
    if CHARACTERS_SETS is None:
        CHARACTERS_SETS = {}


def settings_window():
    sw = customtkinter.CTkToplevel(root)  # settings window
    sw.title("Settings")
    sw.resizable(False, False)
    sw.protocol("WM_DELETE_WINDOW", lambda: close_new_window(sw))
    root.state('withdrawn')

def create_modify_password_window(index):
    npw = customtkinter.CTkToplevel(root)  # new password window
    npw.title("New Account" if index == -1 else "Modify Account")
    npw.resizable(False, False)
    npw.protocol("WM_DELETE_WINDOW", lambda: close_new_window(npw))
    root.state('withdrawn')

    if index == -1:
        if len(PASSWORDS) == 0:
            id_num = 0
        else:
            id_num = max([int(p.get("password_id")) for p in PASSWORDS])+1
    else:
        id_num = PASSWORDS[index].get("password_id")

    # # Frame 1 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_1 = customtkinter.CTkFrame(npw)
    frame_1.pack(expand=1, fill="both")

    label_name = customtkinter.CTkLabel(frame_1,
                                        text="Name:",
                                        anchor="e",
                                        width=NEW_PASS_LABEL_WIDTH,
                                        height=LINE_HEIGHT
                                        )
    label_name.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

    entry_name = customtkinter.CTkEntry(frame_1, width=WIDTH, height=LINE_HEIGHT)
    entry_name.grid(row=0, column=1, padx=[5, PADX], pady=PADY)
    if index != -1:
        entry_name.insert(0, PASSWORDS[index].get("name"))

    # # Frame 2 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_2 = customtkinter.CTkFrame(npw)
    frame_2.pack(expand=1, fill="both")

    label_email = customtkinter.CTkLabel(frame_2,
                                         text="Email:",
                                         anchor="e",
                                         width=NEW_PASS_LABEL_WIDTH,
                                         height=LINE_HEIGHT
                                         )
    label_email.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

    entry_email = customtkinter.CTkEntry(frame_2, width=WIDTH, height=LINE_HEIGHT)
    entry_email.grid(row=0, column=1, padx=[5, PADX], pady=PADY)
    if index != -1:
        entry_email.insert(0, PASSWORDS[index].get("e_mail"))

    # # Frame 3 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_3 = customtkinter.CTkFrame(npw)
    frame_3.pack(expand=1, fill="both")

    label_extra = customtkinter.CTkLabel(frame_3,
                                         text="Extra:",
                                         anchor="e",
                                         width=NEW_PASS_LABEL_WIDTH,
                                         height=LINE_HEIGHT
                                         )
    label_extra.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

    entry_extra = customtkinter.CTkEntry(frame_3, width=WIDTH, height=LINE_HEIGHT)
    entry_extra.grid(row=0, column=1, padx=[5, PADX], pady=PADY)
    if index != -1:
        entry_extra.insert(0, PASSWORDS[index].get("extra"))

    # # Frame 4 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_4 = customtkinter.CTkFrame(npw)
    frame_4.pack(expand=1, fill="both")

    label_version = customtkinter.CTkLabel(frame_4,
                                           text="Version:",
                                           anchor="e",
                                           width=NEW_PASS_LABEL_WIDTH,
                                           height=LINE_HEIGHT
                                           )
    label_version.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

    if index == -1:
        version_string_var.set("0")
    else:
        version_string_var.set(PASSWORDS[index].get("version"))
    entry_version = customtkinter.CTkEntry(frame_4,
                                           width=WIDTH-2*INC_DEC_WIDTH-10,
                                           height=LINE_HEIGHT,
                                           state="readonly",
                                           textvariable=version_string_var
                                           )
    entry_version.grid(row=0, column=1, padx=[5, 5], pady=PADY)

    button_decrement = customtkinter.CTkButton(frame_4,
                                               text="<<<",
                                               width=INC_DEC_WIDTH,
                                               height=LINE_HEIGHT,
                                               command=decrement_button_pressed
                                               )
    button_decrement.grid(row=0, column=2, padx=[0, 5], pady=PADY)

    button_increment = customtkinter.CTkButton(frame_4,
                                               text=">>>",
                                               width=INC_DEC_WIDTH,
                                               height=LINE_HEIGHT,
                                               command=increment_button_pressed
                                               )
    button_increment.grid(row=0, column=3, padx=[0, PADX], pady=PADY)

    # # Frame 5 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_5 = customtkinter.CTkFrame(npw)
    frame_5.pack(expand=1, fill="both")

    label_character_set = customtkinter.CTkLabel(frame_5,
                                                 text="Characters Set:",
                                                 anchor="e",
                                                 width=NEW_PASS_LABEL_WIDTH,
                                                 height=LINE_HEIGHT
                                                 )
    label_character_set.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

    cbb_characters_list = customtkinter.CTkComboBox(frame_5,
                                                    width=WIDTH,
                                                    height=LINE_HEIGHT,
                                                    state="readonly",
                                                    values=list(CHARACTERS_SETS.keys())
                                                    )
    cbb_characters_list.grid(row=0, column=1, padx=[5, PADX], pady=PADY)
    if index != -1:
        cbb_characters_list.set(PASSWORDS[index].get("characters_list"))

    # # Frame 6 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_6 = customtkinter.CTkFrame(npw)
    frame_6.pack(expand=1, fill="both")

    button_add_modify_password = customtkinter.CTkButton(frame_6,
                                                         height=LINE_HEIGHT,
                                                         text="Add" if index == -1 else "Modify",
                                                         command=lambda: add_modify_password(npw,
                                                                                             entry_name.get(),
                                                                                             entry_email.get(),
                                                                                             entry_extra.get(),
                                                                                             entry_version.get(),
                                                                                             cbb_characters_list.get(),
                                                                                             id_num,
                                                                                             index)
                                                         )
    button_add_modify_password.pack(pady=PADY*2)


def create_new_character_set():
    ncsw = customtkinter.CTkToplevel(root)  # new character set window
    ncsw.title("New Characters Set")
    ncsw.protocol("WM_DELETE_WINDOW", lambda: close_new_window(ncsw))
    ncsw.resizable(False, False)
    root.state('withdrawn')

    # # Frame 1 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_1 = customtkinter.CTkFrame(ncsw)
    frame_1.pack(expand=1, fill="both")

    label_name = customtkinter.CTkLabel(frame_1, text="Name:", anchor="e", height=LINE_HEIGHT)
    label_name.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

    entry_name = customtkinter.CTkEntry(frame_1, width=WIDTH, height=LINE_HEIGHT)
    entry_name.grid(row=0, column=1, padx=[5, PADX], pady=PADY)

    # # Scrollable Frame # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    scrollable_frame = customtkinter.CTkScrollableFrame(ncsw, label_text="Select Characters")
    scrollable_frame.pack(expand=1, fill="both")

    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    scrollable_frame.grid_columnconfigure(2, weight=1)

    bool_az = IntVar()
    checkbutton_az = customtkinter.CTkCheckBox(scrollable_frame,
                                               text="a - z",
                                               width=CHECK_BUTTONS_WIDTH,
                                               variable=bool_az,
                                               onvalue=1,
                                               offvalue=0)
    checkbutton_az.grid(row=0, column=0, padx=0, pady=2 * PADY)

    bool_cap_a_cap_z = IntVar()
    checkbutton_cap_a_cap_z = customtkinter.CTkCheckBox(scrollable_frame,
                                                        text="A - Z",
                                                        width=CHECK_BUTTONS_WIDTH,
                                                        variable=bool_cap_a_cap_z,
                                                        onvalue=1,
                                                        offvalue=0)
    checkbutton_cap_a_cap_z.grid(row=0, column=1, padx=0, pady=2 * PADY)

    bool_0_9 = IntVar()
    checkbutton_0_9 = customtkinter.CTkCheckBox(scrollable_frame,
                                                text="0 - 9",
                                                width=CHECK_BUTTONS_WIDTH,
                                                variable=bool_0_9,
                                                onvalue=1,
                                                offvalue=0)
    checkbutton_0_9.grid(row=0, column=2, padx=0, pady=2 * PADY)

    bool_check_vars = []
    # Create checkbuttons in a loop
    for i, char in enumerate(Special_Characters):
        var = IntVar()  # Create a new IntVar for each checkbutton
        bool_check_vars.append(var)  # Store the IntVar in a list

        # Create a Checkbutton with the character as its label
        checkbutton = customtkinter.CTkCheckBox(scrollable_frame,
                                                text=char,
                                                width=CHECK_BUTTONS_WIDTH,
                                                font=("Segoe UI", 20),
                                                variable=var,
                                                onvalue=1,
                                                offvalue=0)
        checkbutton.grid(row=i // 3 + 1, column=i % 3, padx=0, pady=2*PADY)

    # Frame 3 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_3 = customtkinter.CTkFrame(ncsw)
    frame_3.pack(expand=1, fill="both")

    button_confirm_new_character_set = \
        customtkinter.CTkButton(frame_3,
                                text="Add",
                                height=LINE_HEIGHT,
                                command=lambda: confirm_new_character_set(ncsw,
                                                                          entry_name.get(),
                                                                          bool_az.get(),
                                                                          bool_cap_a_cap_z.get(),
                                                                          bool_0_9.get(),
                                                                          bool_check_vars)
                                )
    button_confirm_new_character_set.pack(pady=PADY*2)


def add_modify_password(window, name, email, extra, version, charcater_set, num_id, index):
    if (not name) or (not charcater_set):
        messagebox.showerror("Error", "An Account needs at least a Name and a Characters Set")
    elif (name in [p.get("name") for p in PASSWORDS]) and (index == -1):
        messagebox.showerror("Error", "An Account with the same name already exists")
    else:
        # index is -1 for adding and an integer for modify
        new_password_dict = {"name": name,
                             "e_mail": email,
                             "password_id": id_num_to_str(num_id),
                             "version": version,
                             "characters_list": charcater_set,
                             "extra": extra}
        if index == -1:  # adding
            PASSWORDS.append(new_password_dict)
        else:  # modify
            PASSWORDS[index] = new_password_dict

        PASSWORDS.sort(key=lambda x: x['name'].lower())
        if SETTINGS["MODE"] == "JSON":
            write_json_file(SETTINGS["PATH_OF_JSON_DATA"]+"PASSWORDS.json", PASSWORDS)
        elif SETTINGS["MODE"] == "DATABASE":
            db_PASSWORDS.set(PASSWORDS)
        close_new_window(window)


def confirm_new_character_set(window, set_name, bool_a_z, bool_capa_capz, bool_0_9, bool_special_characters):
    if (not set_name) or not (any(bool_var.get() == 1 for bool_var in bool_special_characters) or bool_a_z or bool_0_9 or bool_capa_capz):
        messagebox.showerror("Error", "A Characters Set needs a name and at least one character")
    elif set_name in list(CHARACTERS_SETS.keys()):
        messagebox.showerror("Error", "A Characters Set with the same name already exists")
    else:
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

        CHARACTERS_SETS[set_name] = new_set
        if SETTINGS["MODE"] == "JSON":
            write_json_file(SETTINGS["PATH_OF_JSON_DATA"]+"CHARACTERS_SETS.json", CHARACTERS_SETS)
        elif SETTINGS["MODE"] == "DATABASE":
            db_CHARACTERS_SETS.set(CHARACTERS_SETS)
        close_new_window(window)


def close_new_window(new_window):
    new_window.destroy()
    root.deiconify()
    Button_modify_password.configure(state='disabled')
    Combobox_account.configure(values=[p.get("name") for p in PASSWORDS])
    Combobox_account.set('')
    email_string_var.set('')
    extra_string_var.set('')


def account_combobox_selected(choice):
    root.focus()
    index = get_index(Combobox_account.cget("values"), choice)
    Button_modify_password.configure(state='normal')
    selected_password = PASSWORDS[index]
    email_string_var.set(selected_password.get("e_mail"))
    extra_string_var.set(selected_password.get("extra"))
    text_to_cript = "myPassword!!" + selected_password.get("version") + selected_password.get("password_id")
    add_to_clipboard(get_password(text_to_cript,
                                  Entry_main_password.get(),
                                  CHARACTERS_SETS.get(selected_password.get("characters_list"))))


def increment_button_pressed():
    version_string_var.set(increment_string(version_string_var.get()))


def decrement_button_pressed():
    version_string_var.set(decrement_string(version_string_var.get()))


def get_password(pass_text, key_text, char_list):
    # ensuring that key_text is at least 16 characters long
    while len(key_text) < 16:
        key_text += "0"

    pass_state = text_to_state(pass_text)
    key_state = text_to_state(key_text)
    return state_to_text(crypt(pass_state, key_state), char_list)


def on_button_view_press(_):
    Entry_main_password.configure(show="")


def on_button_view_release(_):
    Entry_main_password.configure(show="*")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# MAIN WINDOW
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

root = customtkinter.CTk()
root.title("PASSWAN")
root.iconbitmap("passwan2.ico")
root.resizable(False, False)

# StringVars
email_string_var = StringVar()
extra_string_var = StringVar()
version_string_var = StringVar()

# General constants
WIDTH = 350
LABEL_WIDTH = 100
NEW_PASS_LABEL_WIDTH = 90
PADX = 15
PADY = 5
CHECK_BUTTONS_WIDTH = 60
LINE_HEIGHT = 30
BUTTON_VIEW_WIDTH = 35
INC_DEC_WIDTH = 95

# Image
eye_image = Image.open("eye.png")

# Settings Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_settings = customtkinter.CTkFrame(root)
Frame_settings.pack(expand=1, fill="both")

Button_Settings = customtkinter.CTkButton(Frame_settings,
                                          height=LINE_HEIGHT,
                                          text="Settings",
                                          command=settings_window
                                          )
Button_Settings.pack(fill="both", padx=1, pady=(1, 2*PADY))

# First Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_First_Row = customtkinter.CTkFrame(root)
Frame_First_Row.pack(expand=1, fill="both")

Label_main_password = customtkinter.CTkLabel(Frame_First_Row,
                                             text="Master Password:",
                                             anchor="e",
                                             width=LABEL_WIDTH,
                                             height=LINE_HEIGHT
                                             )
Label_main_password.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

Entry_main_password = customtkinter.CTkEntry(Frame_First_Row,
                                             width=WIDTH - BUTTON_VIEW_WIDTH - 7,
                                             show='*',
                                             height=LINE_HEIGHT
                                             )
Entry_main_password.grid(row=0, column=1, padx=[5, 0], pady=PADY)

Button_view = customtkinter.CTkButton(Frame_First_Row,
                                      text="",
                                      image=customtkinter.CTkImage(light_image=eye_image),
                                      width=BUTTON_VIEW_WIDTH,
                                      height=LINE_HEIGHT
                                      )
Button_view.grid(row=0, column=2, padx=[5, PADX], pady=PADY, ipadx=0, ipady=0)
Button_view.bind("<ButtonPress-1>", on_button_view_press)
Button_view.bind("<ButtonRelease-1>", on_button_view_release)

# Second Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_Second_Row = customtkinter.CTkFrame(root)
Frame_Second_Row.pack(expand=1, fill="both")

Label_email = customtkinter.CTkLabel(Frame_Second_Row,
                                     text="Email:",
                                     anchor="e",
                                     width=LABEL_WIDTH,
                                     height=LINE_HEIGHT)
Label_email.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

Entry_email = customtkinter.CTkEntry(Frame_Second_Row,
                                     width=WIDTH,
                                     height=LINE_HEIGHT,
                                     state="readonly",
                                     textvariable=email_string_var)
Entry_email.grid(row=0, column=1, padx=[5, PADX], pady=PADY)

# Third Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_Third_Row = customtkinter.CTkFrame(root)
Frame_Third_Row.pack(expand=1, fill="both")

Label_extra = customtkinter.CTkLabel(Frame_Third_Row, text="Extra:", anchor="e", width=LABEL_WIDTH, height=LINE_HEIGHT)
Label_extra.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

Entry_extra = customtkinter.CTkEntry(Frame_Third_Row,
                                     width=WIDTH,
                                     state="readonly",
                                     textvariable=extra_string_var,
                                     height=LINE_HEIGHT)
Entry_extra.grid(row=0, column=1, padx=[5, PADX], pady=PADY)

# Fourth Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_Fourth_Row = customtkinter.CTkFrame(root)
Frame_Fourth_Row.pack(expand=1, fill="both")

Label_combobox = customtkinter.CTkLabel(Frame_Fourth_Row,
                                        text="Account:", anchor="e",
                                        width=LABEL_WIDTH,
                                        height=LINE_HEIGHT)
Label_combobox.grid(row=0, column=0, padx=[PADX, 0], pady=PADY)

Combobox_account = customtkinter.CTkComboBox(Frame_Fourth_Row,
                                             width=WIDTH,
                                             height=LINE_HEIGHT,
                                             state="readonly",
                                             values=[p.get("name") for p in PASSWORDS],
                                             command=account_combobox_selected
                                             )
Combobox_account.grid(row=0, column=1, padx=[5, PADX], pady=PADY)

# Buttons Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_Buttons_Row = customtkinter.CTkFrame(root)
Frame_Buttons_Row.pack(expand=1, fill="both")
Frame_Buttons_Row.grid_columnconfigure(0, weight=1)
Frame_Buttons_Row.grid_columnconfigure(1, weight=1)
Frame_Buttons_Row.grid_columnconfigure(2, weight=1)

Button_modify_password = \
    customtkinter.CTkButton(Frame_Buttons_Row,
                            text="Modify Account",
                            height=LINE_HEIGHT,
                            command=lambda: create_modify_password_window(
                                get_index(Combobox_account.cget("values"), Combobox_account.get())),
                            state="disabled")
Button_modify_password.grid(row=0, column=0, padx=[PADX, 5], pady=PADY, sticky="nsew")

Button_new_password = customtkinter.CTkButton(Frame_Buttons_Row,
                                              text="New Account",
                                              height=LINE_HEIGHT,
                                              command=lambda: create_modify_password_window(-1)
                                              )
Button_new_password.grid(row=0, column=1, padx=[5, 5], pady=PADY, sticky="nsew")

Button_new_character_set = customtkinter.CTkButton(Frame_Buttons_Row,
                                                   text="New Characters Set",
                                                   height=LINE_HEIGHT,
                                                   command=create_new_character_set
                                                   )
Button_new_character_set.grid(row=0, column=2, padx=[5, PADX], pady=PADY, sticky="nsew")

root.mainloop()
