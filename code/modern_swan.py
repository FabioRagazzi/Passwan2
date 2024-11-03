from tkinter import messagebox, IntVar, StringVar, filedialog
from PIL import Image
import shutil
import customtkinter
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from AES import *
from Functions import *

# List of all the special characters available
Special_Characters = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                      "_", "-", "+", "=", "{", "}", "[", "]", "|", ":", ";", "'",
                      "<", ">", ",", ".", "?", "/"]

# Loading the settings
try:
    with open("SETTINGS.json", 'r') as settings_file:
        SETTINGS = json.load(settings_file)
except FileNotFoundError:
    # If it is the first time the app is used, create the SETTINGS.json file
    temp_str_script_path = os.path.dirname(os.path.abspath(__file__))
    str_script_path = temp_str_script_path.replace("\\", "/")
    SETTINGS = {"MODE": "JSON",
                "PATH_OF_JSON_DATA": str_script_path + "/",
                "PATH_OF_CERTIFICATE": " ",
                "DATABASE_URL": "",
                "WIDTH": 450,
                "LINE_HEIGHT": 35,
                "LABEL_WIDTH": 100,
                "NEW_PASS_LABEL_WIDTH": 90,
                "SETTINGS_LABEL_WIDTH": 100,
                "BROWSE_BUTTON_WIDTH": 45,
                "CHECK_BUTTONS_WIDTH": 60,
                "CHECK_BUTTONS_HEIGHT": 40,
                "INC_DEC_WIDTH": 95,
                "BUTTON_VIEW_WIDTH": 35,
                "PADX": 15,
                "PADY": 2,
                "FONT_NAME": "Roboto",
                "FONT_SIZE": 13
                }
    with open("SETTINGS.json", 'w') as settings_file:
        json.dump(SETTINGS, settings_file, indent=2)

db_PASSWORDS = None
db_CHARACTERS_SETS = None
PASSWORDS = None
if SETTINGS["MODE"] == "JSON":
    # Read the JSON files
    PASSWORDS = read_json_file(SETTINGS["PATH_OF_JSON_DATA"]+"PASSWORDS.json", [])
    CHARACTERS_SETS = read_json_file(SETTINGS["PATH_OF_JSON_DATA"]+"CHARACTERS_SETS.json", {})
elif SETTINGS["MODE"] == "DATABASE":
    # Read from online DB
    cred = credentials.Certificate(SETTINGS["PATH_OF_CERTIFICATE"])
    firebase_admin.initialize_app(cred, {'databaseURL': SETTINGS["DATABASE_URL"]})

    db_PASSWORDS = db.reference('PASSWORDS')
    db_CHARACTERS_SETS = db.reference('CHARACTERS_SETS')
    PASSWORDS = db_PASSWORDS.get()
    CHARACTERS_SETS = db_CHARACTERS_SETS.get()
    if PASSWORDS is None:
        PASSWORDS = []
    if CHARACTERS_SETS is None:
        CHARACTERS_SETS = {}


def browse_folder():
    folder_path = filedialog.askdirectory(
        title="Select the .json files folder"
    )
    json_folder_string_var.set(folder_path)


def browse_certificate():
    certificate_path = filedialog.askopenfilename(
        title="Select your database certificate",
        filetypes=(("JSON files", "*.json"), ("All files", "*.*"))  # Filter for .json files
    )
    certificate_path_string_var.set(certificate_path)


def set_mode(button_json, button_database, entry_database, flag):
    if flag == "JSON":
        button_json.configure(state="normal")
        button_database.configure(state="disabled")
        entry_database.configure(state="disabled")
    elif flag == "DATABASE":
        button_json.configure(state="disabled")
        button_database.configure(state="normal")
        entry_database.configure(state="normal")


def apply_settings(window, num_radio_button, entry_url_text):

    error_flag = 0

    # CASE 1: Remained in JSON mode, but changed folder
    if SETTINGS["MODE"] == "JSON" and num_radio_button == 1:  # Remained in JSON mode
        if SETTINGS["PATH_OF_JSON_DATA"] != (json_folder_string_var.get() + "/"):  # but changed folder
            # Copy .json files
            shutil.copyfile(SETTINGS["PATH_OF_JSON_DATA"]+"PASSWORDS.json",
                            json_folder_string_var.get() + "/" + "PASSWORDS.json")
            shutil.copyfile(SETTINGS["PATH_OF_JSON_DATA"] + "CHARACTERS_SETS.json",
                            json_folder_string_var.get() + "/" + "CHARACTERS_SETS.json")
            # Delete previous ones
            os.remove(SETTINGS["PATH_OF_JSON_DATA"]+"PASSWORDS.json")
            os.remove(SETTINGS["PATH_OF_JSON_DATA"] + "CHARACTERS_SETS.json")
            # Change folder path
            SETTINGS["PATH_OF_JSON_DATA"] = json_folder_string_var.get() + "/"

    # CASE 2: Switched from JSON mode to DATABASE mode
    if SETTINGS["MODE"] == "JSON" and num_radio_button == 2:
        global db_PASSWORDS
        global db_CHARACTERS_SETS
        try:
            cred_in = credentials.Certificate(certificate_path_string_var.get())
            firebase_admin.initialize_app(cred_in, {'databaseURL': entry_url_text})

            db_PASSWORDS = db.reference('PASSWORDS')
            db_CHARACTERS_SETS = db.reference('CHARACTERS_SETS')
            db_PASSWORDS.get()
        except Exception as e:
            error_flag = 1
            messagebox.showerror("Error", str(e))

        if not error_flag:
            # Move .json files to database
            db_PASSWORDS.set(PASSWORDS)
            db_CHARACTERS_SETS.set(CHARACTERS_SETS)
            # Delete local .json files
            os.remove(SETTINGS["PATH_OF_JSON_DATA"] + "PASSWORDS.json")
            os.remove(SETTINGS["PATH_OF_JSON_DATA"] + "CHARACTERS_SETS.json")
            # Update settings
            SETTINGS["MODE"] = "DATABASE"
            SETTINGS["PATH_OF_CERTIFICATE"] = certificate_path_string_var.get()
            SETTINGS["DATABASE_URL"] = entry_url_text

    # CASE 3: Switched from DATABASE mode to JSON mode
    if SETTINGS["MODE"] == "DATABASE" and num_radio_button == 1:
        # Updating the settings
        SETTINGS["MODE"] = "JSON"
        SETTINGS["PATH_OF_JSON_DATA"] = json_folder_string_var.get() + "/"
        # Copying file in local folder
        write_json_file(SETTINGS["PATH_OF_JSON_DATA"] + "PASSWORDS.json", PASSWORDS)
        write_json_file(SETTINGS["PATH_OF_JSON_DATA"] + "CHARACTERS_SETS.json", CHARACTERS_SETS)
        # Clearing database
        ref = db.reference('/')  # Reference to the root node
        ref.delete()  # Deletes everything under the root node

    # CASE 4: Remained in DATABASE mode, but changed url or certificate
    if SETTINGS["MODE"] == "DATABASE" and num_radio_button == 2:  # Remained in DATABASE mode
        if (SETTINGS["PATH_OF_CERTIFICATE"] != certificate_path_string_var.get()) or \
                (SETTINGS["DATABASE_URL"] != entry_url_text):  # but changed url or certificate
            error_flag = 1
            messagebox.showerror("Error", "Changing your database is not implemented yet")

    if not error_flag:
        with open("SETTINGS.json", 'w') as temp_settings_file:
            json.dump(SETTINGS, temp_settings_file, indent=2)

        close_new_window(window)


def settings_window():
    sw = customtkinter.CTkToplevel(root)  # settings window
    sw.title("Settings")
    sw.resizable(False, False)
    sw.protocol("WM_DELETE_WINDOW", lambda: close_new_window(sw))
    root.state('withdrawn')

    # # Frame Radio Buttons # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_radio = customtkinter.CTkFrame(sw)
    frame_radio.pack(expand=1, fill="both")
    frame_radio.grid_columnconfigure(0, weight=1)
    frame_radio.grid_columnconfigure(1, weight=1)

    radio_var = IntVar()

    if SETTINGS["MODE"] == "JSON":
        radio_var.set(1)
    elif SETTINGS["MODE"] == "DATABASE":
        radio_var.set(2)

    # Initializing the entries
    json_folder_string_var.set(SETTINGS["PATH_OF_JSON_DATA"][:-1])
    certificate_path_string_var.set(SETTINGS["PATH_OF_CERTIFICATE"])
    url_string = SETTINGS["DATABASE_URL"]

    radiobutton_json = customtkinter.CTkRadioButton(frame_radio,
                                                    font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                    text="JSON MODE",
                                                    height=SETTINGS["LINE_HEIGHT"],
                                                    variable=radio_var,
                                                    command=lambda: set_mode(button_browse_json_path,
                                                                             button_browse_certificate_path,
                                                                             entry_url, "JSON"),
                                                    value=1)
    radiobutton_database = customtkinter.CTkRadioButton(frame_radio,
                                                        font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                        text="DATABASE MODE",
                                                        height=SETTINGS["LINE_HEIGHT"],
                                                        variable=radio_var,
                                                        command=lambda: set_mode(button_browse_json_path,
                                                                                 button_browse_certificate_path,
                                                                                 entry_url, "DATABASE"),
                                                        value=2)
    radiobutton_json.grid(row=0, column=0, padx=SETTINGS["PADX"], pady=SETTINGS["PADY"])
    radiobutton_database.grid(row=0, column=1, padx=SETTINGS["PADX"], pady=SETTINGS["PADY"])

    # # Frame Json # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_json = customtkinter.CTkFrame(sw, border_width=2)
    frame_json.pack(expand=1, fill="both", pady=(0, 3*SETTINGS["PADY"]))

    title_label_json = customtkinter.CTkLabel(frame_json,
                                              font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                              width=SETTINGS["SETTINGS_LABEL_WIDTH"],
                                              anchor="w",
                                              text="JSON")
    title_label_json.grid(row=0, column=0, padx=SETTINGS["PADX"], pady=SETTINGS["PADY"], sticky="nsew")

    label_json_path = customtkinter.CTkLabel(frame_json,
                                             text="Json Folder:",
                                             anchor="e",
                                             font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                             width=SETTINGS["SETTINGS_LABEL_WIDTH"],
                                             height=SETTINGS["LINE_HEIGHT"])
    label_json_path.grid(row=1, column=0, padx=(SETTINGS["PADX"], 0), pady=SETTINGS["PADY"], sticky="nsew")

    entry_json_path = customtkinter.CTkEntry(frame_json,
                                             font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                             width=SETTINGS["WIDTH"],
                                             height=SETTINGS["LINE_HEIGHT"],
                                             textvariable=json_folder_string_var,
                                             state="readonly")
    entry_json_path.grid(row=1, column=1, padx=(5, 0), pady=SETTINGS["PADY"], sticky="nsew")

    button_browse_json_path = customtkinter.CTkButton(frame_json,
                                                      image=customtkinter.CTkImage(light_image=folder_image),
                                                      text="",
                                                      width=SETTINGS["BROWSE_BUTTON_WIDTH"],
                                                      height=SETTINGS["LINE_HEIGHT"],
                                                      command=browse_folder)
    button_browse_json_path.grid(row=1, column=2, padx=(5, SETTINGS["PADX"]), pady=SETTINGS["PADY"], sticky="nsew")

    # # Frame DataBase # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_database = customtkinter.CTkFrame(sw, border_width=2)
    frame_database.pack(expand=1, fill="both", pady=(0, 3*SETTINGS["PADY"]))

    title_label_database = customtkinter.CTkLabel(frame_database,
                                                  font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                  width=SETTINGS["SETTINGS_LABEL_WIDTH"],
                                                  anchor="w",
                                                  text="DATABASE")
    title_label_database.grid(row=0, column=0, padx=SETTINGS["PADX"], pady=SETTINGS["PADY"], sticky="nsew")

    label_certificate_path = customtkinter.CTkLabel(frame_database,
                                                    text="Certificate File:",
                                                    anchor="e",
                                                    font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                    width=SETTINGS["SETTINGS_LABEL_WIDTH"],
                                                    height=SETTINGS["LINE_HEIGHT"])
    label_certificate_path.grid(row=1, column=0, padx=(SETTINGS["PADX"], 0), pady=SETTINGS["PADY"], sticky="nsew")

    entry_certificate_path = customtkinter.CTkEntry(frame_database,
                                                    font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                    width=SETTINGS["WIDTH"],
                                                    height=SETTINGS["LINE_HEIGHT"],
                                                    textvariable=certificate_path_string_var,
                                                    state="readonly")
    entry_certificate_path.grid(row=1, column=1, padx=(5, 0), pady=SETTINGS["PADY"], sticky="nsew")

    button_browse_certificate_path = customtkinter.CTkButton(frame_database,
                                                             image=customtkinter.CTkImage(light_image=file_image),
                                                             text="",
                                                             width=SETTINGS["BROWSE_BUTTON_WIDTH"],
                                                             height=SETTINGS["LINE_HEIGHT"],
                                                             command=browse_certificate)
    button_browse_certificate_path.grid(row=1, column=2,
                                        padx=(5, SETTINGS["PADX"]), pady=SETTINGS["PADY"], sticky="nsew")

    label_url = customtkinter.CTkLabel(frame_database,
                                       text="Database URL:",
                                       anchor="e",
                                       font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                       width=SETTINGS["SETTINGS_LABEL_WIDTH"],
                                       height=SETTINGS["LINE_HEIGHT"])
    label_url.grid(row=2, column=0, padx=(SETTINGS["PADX"], 0), pady=SETTINGS["PADY"], sticky="nsew")

    entry_url = customtkinter.CTkEntry(frame_database,
                                       font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                       width=SETTINGS["WIDTH"],
                                       height=SETTINGS["LINE_HEIGHT"])
    entry_url.grid(row=2, column=1, padx=(5, 0), pady=SETTINGS["PADY"], sticky="nsew")
    entry_url.insert(0, url_string)

    # # Frame Button # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_button = customtkinter.CTkFrame(sw)
    frame_button.pack(expand=1, fill="both")
    apply_button = customtkinter.CTkButton(frame_button,
                                           font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                           text="Apply",
                                           command=lambda: apply_settings(sw, radio_var.get(), entry_url.get()),
                                           height=SETTINGS["LINE_HEIGHT"])
    apply_button.pack(pady=2*SETTINGS["PADY"])

    set_mode(button_browse_json_path, button_browse_certificate_path, entry_url, SETTINGS["MODE"])


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
                                        font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                        text="Name:",
                                        anchor="e",
                                        width=SETTINGS["NEW_PASS_LABEL_WIDTH"],
                                        height=SETTINGS["LINE_HEIGHT"]
                                        )
    label_name.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

    entry_name = customtkinter.CTkEntry(frame_1,
                                        font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                        width=SETTINGS["WIDTH"],
                                        height=SETTINGS["LINE_HEIGHT"])
    entry_name.grid(row=0, column=1, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"])
    if index != -1:
        entry_name.insert(0, PASSWORDS[index].get("name"))

    # # Frame 2 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_2 = customtkinter.CTkFrame(npw)
    frame_2.pack(expand=1, fill="both")

    label_email = customtkinter.CTkLabel(frame_2,
                                         font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                         text="Email:",
                                         anchor="e",
                                         width=SETTINGS["NEW_PASS_LABEL_WIDTH"],
                                         height=SETTINGS["LINE_HEIGHT"]
                                         )
    label_email.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

    entry_email = customtkinter.CTkEntry(frame_2,
                                         font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                         width=SETTINGS["WIDTH"],
                                         height=SETTINGS["LINE_HEIGHT"])
    entry_email.grid(row=0, column=1, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"])
    if index != -1:
        entry_email.insert(0, PASSWORDS[index].get("e_mail"))

    # # Frame 3 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_3 = customtkinter.CTkFrame(npw)
    frame_3.pack(expand=1, fill="both")

    label_extra = customtkinter.CTkLabel(frame_3,
                                         font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                         text="Extra:",
                                         anchor="e",
                                         width=SETTINGS["NEW_PASS_LABEL_WIDTH"],
                                         height=SETTINGS["LINE_HEIGHT"]
                                         )
    label_extra.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

    entry_extra = customtkinter.CTkEntry(frame_3,
                                         font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                         width=SETTINGS["WIDTH"],
                                         height=SETTINGS["LINE_HEIGHT"])
    entry_extra.grid(row=0, column=1, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"])
    if index != -1:
        entry_extra.insert(0, PASSWORDS[index].get("extra"))

    # # Frame 4 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_4 = customtkinter.CTkFrame(npw)
    frame_4.pack(expand=1, fill="both")

    label_version = customtkinter.CTkLabel(frame_4,
                                           font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                           text="Version:",
                                           anchor="e",
                                           width=SETTINGS["NEW_PASS_LABEL_WIDTH"],
                                           height=SETTINGS["LINE_HEIGHT"]
                                           )
    label_version.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

    if index == -1:
        version_string_var.set("0")
    else:
        version_string_var.set(PASSWORDS[index].get("version"))
    entry_version = customtkinter.CTkEntry(frame_4,
                                           font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                           width=SETTINGS["WIDTH"]-2*SETTINGS["INC_DEC_WIDTH"]-10,
                                           height=SETTINGS["LINE_HEIGHT"],
                                           state="readonly",
                                           textvariable=version_string_var
                                           )
    entry_version.grid(row=0, column=1, padx=[5, 5], pady=SETTINGS["PADY"])

    button_decrement = customtkinter.CTkButton(frame_4,
                                               font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                               text="<<<",
                                               width=SETTINGS["INC_DEC_WIDTH"],
                                               height=SETTINGS["LINE_HEIGHT"],
                                               command=decrement_button_pressed
                                               )
    button_decrement.grid(row=0, column=2, padx=[0, 5], pady=SETTINGS["PADY"])

    button_increment = customtkinter.CTkButton(frame_4,
                                               font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                               text=">>>",
                                               width=SETTINGS["INC_DEC_WIDTH"],
                                               height=SETTINGS["LINE_HEIGHT"],
                                               command=increment_button_pressed
                                               )
    button_increment.grid(row=0, column=3, padx=[0, SETTINGS["PADX"]], pady=SETTINGS["PADY"])

    # # Frame 5 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_5 = customtkinter.CTkFrame(npw)
    frame_5.pack(expand=1, fill="both")

    label_character_set = customtkinter.CTkLabel(frame_5,
                                                 font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                 text="Characters Set:",
                                                 anchor="e",
                                                 width=SETTINGS["NEW_PASS_LABEL_WIDTH"],
                                                 height=SETTINGS["LINE_HEIGHT"]
                                                 )
    label_character_set.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

    cbb_characters_list = customtkinter.CTkComboBox(frame_5,
                                                    font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                    width=SETTINGS["WIDTH"],
                                                    height=SETTINGS["LINE_HEIGHT"],
                                                    state="readonly",
                                                    values=list(CHARACTERS_SETS.keys())
                                                    )
    cbb_characters_list.grid(row=0, column=1, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"])
    if index != -1:
        cbb_characters_list.set(PASSWORDS[index].get("characters_list"))

    # # Frame 6 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_6 = customtkinter.CTkFrame(npw)
    frame_6.pack(expand=1, fill="both")

    button_add_modify_password = customtkinter.CTkButton(frame_6,
                                                         font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                         height=SETTINGS["LINE_HEIGHT"],
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
    button_add_modify_password.pack(pady=SETTINGS["PADY"]*2)


def create_new_character_set():
    ncsw = customtkinter.CTkToplevel(root)  # new character set window
    ncsw.title("New Characters Set")
    ncsw.protocol("WM_DELETE_WINDOW", lambda: close_new_window(ncsw))
    ncsw.resizable(False, False)
    root.state('withdrawn')

    # # Frame 1 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_1 = customtkinter.CTkFrame(ncsw)
    frame_1.pack(expand=1, fill="both")

    label_name = customtkinter.CTkLabel(frame_1,
                                        font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                        text="  Name:",
                                        anchor="e",
                                        height=SETTINGS["LINE_HEIGHT"])
    label_name.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=(SETTINGS["PADY"], 2*SETTINGS["PADY"]))

    entry_name = customtkinter.CTkEntry(frame_1,
                                        font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                        width=SETTINGS["WIDTH"],
                                        height=SETTINGS["LINE_HEIGHT"])
    entry_name.grid(row=0, column=1, padx=[5, SETTINGS["PADX"]], pady=(SETTINGS["PADY"], 2*SETTINGS["PADY"]))

    # # Scrollable Frame # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    scrollable_frame = customtkinter.CTkScrollableFrame(ncsw,
                                                        label_font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                        label_text="Select Characters")
    scrollable_frame.pack(expand=1, fill="both")

    scrollable_frame.grid_columnconfigure(0, weight=1)
    scrollable_frame.grid_columnconfigure(1, weight=1)
    scrollable_frame.grid_columnconfigure(2, weight=1)

    bool_az = IntVar()
    checkbutton_az = customtkinter.CTkCheckBox(scrollable_frame,
                                               font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                               text="a - z",
                                               height=SETTINGS["CHECK_BUTTONS_HEIGHT"],
                                               width=SETTINGS["CHECK_BUTTONS_WIDTH"],
                                               variable=bool_az,
                                               onvalue=1,
                                               offvalue=0)
    checkbutton_az.grid(row=0, column=0, padx=0, pady=2 * SETTINGS["PADY"])

    bool_cap_a_cap_z = IntVar()
    checkbutton_cap_a_cap_z = customtkinter.CTkCheckBox(scrollable_frame,
                                                        font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                        text="A - Z",
                                                        height=SETTINGS["CHECK_BUTTONS_HEIGHT"],
                                                        width=SETTINGS["CHECK_BUTTONS_WIDTH"],
                                                        variable=bool_cap_a_cap_z,
                                                        onvalue=1,
                                                        offvalue=0)
    checkbutton_cap_a_cap_z.grid(row=0, column=1, padx=0, pady=2 * SETTINGS["PADY"])

    bool_0_9 = IntVar()
    checkbutton_0_9 = customtkinter.CTkCheckBox(scrollable_frame,
                                                font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                text="0 - 9",
                                                height=SETTINGS["CHECK_BUTTONS_HEIGHT"],
                                                width=SETTINGS["CHECK_BUTTONS_WIDTH"],
                                                variable=bool_0_9,
                                                onvalue=1,
                                                offvalue=0)
    checkbutton_0_9.grid(row=0, column=2, padx=0, pady=2 * SETTINGS["PADY"])

    bool_check_vars = []
    # Create checkbuttons in a loop
    for i, char in enumerate(Special_Characters):
        var = IntVar()  # Create a new IntVar for each checkbutton
        bool_check_vars.append(var)  # Store the IntVar in a list

        # Create a Checkbutton with the character as its label
        checkbutton = customtkinter.CTkCheckBox(scrollable_frame,
                                                text=char,
                                                height=SETTINGS["CHECK_BUTTONS_HEIGHT"],
                                                width=SETTINGS["CHECK_BUTTONS_WIDTH"],
                                                font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                variable=var,
                                                onvalue=1,
                                                offvalue=0)
        checkbutton.grid(row=i // 3 + 1, column=i % 3, padx=0, pady=2*SETTINGS["PADY"])

    # # Frame 2 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_2 = customtkinter.CTkFrame(ncsw)
    frame_2.pack(expand=1, fill="both")
    frame_2.grid_columnconfigure(0, weight=1)
    frame_2.grid_columnconfigure(1, weight=1)

    select_all_button = customtkinter.CTkButton(frame_2,
                                                font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                text="Select All",
                                                height=round(SETTINGS["LINE_HEIGHT"]/2),
                                                command=lambda: set_all(bool_az, bool_cap_a_cap_z,
                                                                        bool_0_9, bool_check_vars, 1)
                                                )
    select_all_button.grid(row=0, column=0, padx=(SETTINGS["PADX"], 5), pady=(1, 2*SETTINGS["PADY"]), sticky="nsew")

    deselect_all_button = customtkinter.CTkButton(frame_2,
                                                  font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                  text="Deselect All",
                                                  height=round(SETTINGS["LINE_HEIGHT"] / 2),
                                                  command=lambda: set_all(bool_az, bool_cap_a_cap_z,
                                                                          bool_0_9, bool_check_vars, 0)
                                                  )
    deselect_all_button.grid(row=0, column=1, padx=(0, SETTINGS["PADX"]), pady=(1, 2*SETTINGS["PADY"]), sticky="nsew")

    # Frame 3 # # # # # # # # # # # #  # # # # # # # # # # #  # # # # # # # # # # #
    frame_3 = customtkinter.CTkFrame(ncsw)
    frame_3.pack(expand=1, fill="both")

    button_confirm_new_character_set = \
        customtkinter.CTkButton(frame_3,
                                font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                text="Add",
                                height=SETTINGS["LINE_HEIGHT"],
                                command=lambda: confirm_new_character_set(ncsw,
                                                                          entry_name.get(),
                                                                          bool_az.get(),
                                                                          bool_cap_a_cap_z.get(),
                                                                          bool_0_9.get(),
                                                                          bool_check_vars)
                                )
    button_confirm_new_character_set.pack(pady=SETTINGS["PADY"]*2)


def set_all(bool_az_in, bool_cap_a_cap_z_in, bool_0_9_in, bool_check_vars_in, num_to_set_to):
    bool_az_in.set(num_to_set_to)
    bool_cap_a_cap_z_in.set(num_to_set_to)
    bool_0_9_in.set(num_to_set_to)
    for bool_var_special in bool_check_vars_in:
        bool_var_special.set(num_to_set_to)


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
    if (not set_name) or \
            not (any(bool_var.get() == 1 for bool_var in bool_special_characters) or
                 bool_a_z or bool_0_9 or bool_capa_capz):
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

        new_set.extend(
            [char for char, bool_var in zip(Special_Characters, bool_special_characters) if bool_var.get() == 1])

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
root.iconbitmap("../img/passwan2.ico")
root.resizable(False, False)

# StringVars
email_string_var = StringVar()
extra_string_var = StringVar()
version_string_var = StringVar()
json_folder_string_var = StringVar()
certificate_path_string_var = StringVar()

# Image
eye_image = Image.open("../img/eye.png")
folder_image = Image.open("../img/folder.png")
file_image = Image.open("../img/file.png")

# Settings Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_settings = customtkinter.CTkFrame(root)
Frame_settings.pack(expand=1, fill="both")

Button_Settings = customtkinter.CTkButton(Frame_settings,
                                          font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                          height=round(SETTINGS["LINE_HEIGHT"]/2),
                                          text="Settings",
                                          command=settings_window
                                          )
Button_Settings.pack(fill="both", padx=1, pady=(1, 2*SETTINGS["PADY"]))

# First Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_First_Row = customtkinter.CTkFrame(root)
Frame_First_Row.pack(expand=1, fill="both")

Label_main_password = customtkinter.CTkLabel(Frame_First_Row,
                                             font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                             text="Master Password:",
                                             anchor="e",
                                             width=SETTINGS["LABEL_WIDTH"],
                                             height=SETTINGS["LINE_HEIGHT"]
                                             )
Label_main_password.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

Entry_main_password = customtkinter.CTkEntry(Frame_First_Row,
                                             font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                             width=SETTINGS["WIDTH"] - SETTINGS["BUTTON_VIEW_WIDTH"] - 7,
                                             show='*',
                                             height=SETTINGS["LINE_HEIGHT"]
                                             )
Entry_main_password.grid(row=0, column=1, padx=[5, 0], pady=SETTINGS["PADY"])

Button_view = customtkinter.CTkButton(Frame_First_Row,
                                      text="",
                                      image=customtkinter.CTkImage(light_image=eye_image),
                                      width=SETTINGS["BUTTON_VIEW_WIDTH"],
                                      height=SETTINGS["LINE_HEIGHT"]
                                      )
Button_view.grid(row=0, column=2, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"], ipadx=0, ipady=0)
Button_view.bind("<ButtonPress-1>", on_button_view_press)
Button_view.bind("<ButtonRelease-1>", on_button_view_release)

# Second Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_Second_Row = customtkinter.CTkFrame(root)
Frame_Second_Row.pack(expand=1, fill="both")

Label_email = customtkinter.CTkLabel(Frame_Second_Row,
                                     font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                     text="Email:",
                                     anchor="e",
                                     width=SETTINGS["LABEL_WIDTH"],
                                     height=SETTINGS["LINE_HEIGHT"])
Label_email.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

Entry_email = customtkinter.CTkEntry(Frame_Second_Row,
                                     font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                     width=SETTINGS["WIDTH"],
                                     height=SETTINGS["LINE_HEIGHT"],
                                     state="readonly",
                                     textvariable=email_string_var)
Entry_email.grid(row=0, column=1, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"])

# Third Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_Third_Row = customtkinter.CTkFrame(root)
Frame_Third_Row.pack(expand=1, fill="both")

Label_extra = customtkinter.CTkLabel(Frame_Third_Row,
                                     font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                     text="Extra:",
                                     anchor="e",
                                     width=SETTINGS["LABEL_WIDTH"],
                                     height=SETTINGS["LINE_HEIGHT"])
Label_extra.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

Entry_extra = customtkinter.CTkEntry(Frame_Third_Row,
                                     font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                     width=SETTINGS["WIDTH"],
                                     state="readonly",
                                     textvariable=extra_string_var,
                                     height=SETTINGS["LINE_HEIGHT"])
Entry_extra.grid(row=0, column=1, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"])

# Fourth Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_Fourth_Row = customtkinter.CTkFrame(root)
Frame_Fourth_Row.pack(expand=1, fill="both")

Label_combobox = customtkinter.CTkLabel(Frame_Fourth_Row,
                                        font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                        text="Account:",
                                        anchor="e",
                                        width=SETTINGS["LABEL_WIDTH"],
                                        height=SETTINGS["LINE_HEIGHT"])
Label_combobox.grid(row=0, column=0, padx=[SETTINGS["PADX"], 0], pady=SETTINGS["PADY"])

Combobox_account = customtkinter.CTkComboBox(Frame_Fourth_Row,
                                             font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                             width=SETTINGS["WIDTH"],
                                             height=SETTINGS["LINE_HEIGHT"],
                                             state="readonly",
                                             values=[p.get("name") for p in PASSWORDS],
                                             command=account_combobox_selected
                                             )
Combobox_account.grid(row=0, column=1, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"])

# Buttons Row # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
Frame_Buttons_Row = customtkinter.CTkFrame(root)
Frame_Buttons_Row.pack(expand=1, fill="both")
Frame_Buttons_Row.grid_columnconfigure(0, weight=1)
Frame_Buttons_Row.grid_columnconfigure(1, weight=1)
Frame_Buttons_Row.grid_columnconfigure(2, weight=1)

Button_modify_password = \
    customtkinter.CTkButton(Frame_Buttons_Row,
                            font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                            text="Modify Account",
                            height=SETTINGS["LINE_HEIGHT"],
                            width=round((SETTINGS["WIDTH"] - 20 - 2*SETTINGS["PADX"])/3),
                            command=lambda: create_modify_password_window(
                                get_index(Combobox_account.cget("values"), Combobox_account.get())),
                            state="disabled")
Button_modify_password.grid(row=0, column=0, padx=[SETTINGS["PADX"], 5], pady=SETTINGS["PADY"], sticky="nsew")

Button_new_password = customtkinter.CTkButton(Frame_Buttons_Row,
                                              font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                              text="New Account",
                                              height=SETTINGS["LINE_HEIGHT"],
                                              width=round((SETTINGS["WIDTH"] - 20 - 2*SETTINGS["PADX"])/3),
                                              command=lambda: create_modify_password_window(-1)
                                              )
Button_new_password.grid(row=0, column=1, padx=[5, 5], pady=SETTINGS["PADY"], sticky="nsew")

Button_new_character_set = customtkinter.CTkButton(Frame_Buttons_Row,
                                                   font=(SETTINGS["FONT_NAME"], SETTINGS["FONT_SIZE"]),
                                                   text="New Characters Set",
                                                   height=SETTINGS["LINE_HEIGHT"],
                                                   width=round((SETTINGS["WIDTH"] - 20 - 2*SETTINGS["PADX"])/3),
                                                   command=create_new_character_set
                                                   )
Button_new_character_set.grid(row=0, column=2, padx=[5, SETTINGS["PADX"]], pady=SETTINGS["PADY"], sticky="nsew")

root.mainloop()
