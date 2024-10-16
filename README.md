# Passwan 2.0

## Installation on Windows
### Getting the code
This is a password manager application. 

If you want to use it, 
the first thing to do is to install python.
You can do it from the page: [Install Python](https://www.python.org/downloads/).
Please note that the most recent release might not work, and you will need to download a previous one.

Remember to check the option **add to PATH** during the installation process.

Once you have python, you can download the code from this repository by clicking
on the green button **Code** and selecting **Download ZIP**.

You can also download the code using *git* by running on your terminal the commands:
```
cd <path/of/your/project>
```
```
git clone https://github.com/FabioRagazzi/Passwan2.git
```
Please note that in order to do that you will need *git* installed on your computer.

Also, be aware of the fact that `<path/of/your/project>` is a token, you need to replace it with
the actual path of your project.

To open your terminal you can:
- Press **Windows** + **R**
- Type **cmd**
- Press **Enter**

### Creating the virtual environment
Once you have the code on your machine, you will need to set up a python virtual environment,
that is basically a folder with all the packages needed to run your code.
You can do it by running on your terminal the following commands, one by one:
```
cd <path/of/your/project>
```
```
python -m venv venv
```
```
venv\Scripts\activate
```
```
pip install customtkinter
```
```
deactivate
```

At this point you can create a shortcut to the file `run.vbs` and place it wherever you like 
(usually you want to have it on your desktop).
You can rename the shortcut and maybe even change the icon 
(a good choice for the icon might be the file `passwan2.ico` that you have in this repository).

To change the icon of a file you need to:
- Right-click on that file
- Select **Properties** (maybe after having clicked on **Show more options**)
- Click on **Change Icon...**
- Browse your desired **.ico** file

### Running Passwan 2.0
If you completed the above steps, you can lunch the application just by double-clicking on the
shortcut to the file `run.vbs` you previously created.

If you have an antivirus, it might complain about the execution of such file.

## How to use Passwan
### Creating Characters Sets
In order to start generating passwords, you will first need to create some **Characters Sets**.
They are just a list of all the allowed characters for your password. 

This is needed because different 
sites have different sets of allowed characters. In this way, you can select only the allowed characters when
generating a new password, avoiding the creation of an invalid password.

Each **Characters Set** must have a unique name, and you can reuse the same set for different passwords.

From the main screen, you can click on **New Characters Set** to generate a new one.
Give a name to it and select from the list the desired characters.

Note that letters (**a - z**), capital letters (**A - Z**), and digits (**0 - 9**) are grouped together.

### Creating a Password for a New Account
Clicking on **New Account** a window will open, and you can insert:
- **Name** of your new account (Amazon, Paypal, Google, ...)
- **Email** linked to your account
- **Extra** information when needed
- **Version** of your password (can be useful to change the password for that account, you just need to change the version)
- **Characters Set** for that specific password (you will be able to select from the sets you have already created)

### Getting the Password of an Account
On the top of the main screen you will need to insert your master password.

This password should be ideally 16 characters long.
This is because the code will ignore any extra character if it is longer, and will add zeros until reaching 
a length of 16 characters if it is shorter.

The master password you choose will be the only password you need to remember and will be used to generate all your other passwords.

Once you have typed in the master password, you can select between your saved accounts. 
Once you have made your selection, the **Email** and **Extra** fields will be filled with
the information you provided when creating the account.

The password for that account will be directly saved to your clipboard. 
You can paste it wherever you need to just by pressing **Ctrl** + **V**

### Modifying the Information of an Account
Maybe you realize that you have typed in some extra information wrong, or you have changed your email,
or you want to save that account with a different name, 
or you want to update the password by changing the version. 

To do that, just select the account you want to modify and
click on **Modify Account**. A window will open that will allow you to modify
whatever information you want.

## Working Modes

### Json Mode
The code can work in two different modes. The default mode will store your data
inside some `.json` files. You can to specify the directory where those files will be saved (the default is
the same directory of ypur project, and if you are happy with it, you can leave it like that).

If you want to change the path, a good choice could be some directory with a back-up on the cloud 
(for example with **OneDrive** or **Google Drive** or whatever).
Once you have chosen your directory, copy its path and paste it (enclosed in quotation marks) in the file `Work_in_json_mode.py`
after the equal sign that follows **PATH_OF_DATA**. You should obtain something like this:
```python
PATH_OF_DATA = "G:/My Drive/Mario/BackUp/Passwan Data/"
```
Note that the `/` character before closing the quotation marks is essential.
Also note that the path provided above is completely fictional.


### DataBase Mode
You can store the data needed for the application to work in a Firebase real time database.
To do that you will need first to create a database, and then generate a certificate with your credentials. 
Save the certificate in your computer and then paste its path in the file `Work_in_database_mode.py`.
In the same file you will also need to paste the url of your database.
This video [Firebase with Python](https://www.youtube.com/watch?v=BnrkTpgH5Vc) can help you to set up your database.

You will also need to replace the name ***Work_in_json_mode*** with 
***Work_in_database_mode*** in the third row of the file `Functions.py`
if you want to use the real time database.

## Advantages of Using Passwan 2.0
Using Passwan 2.0, you will need to remember just one password, but at the same time
you will get some very safe ones (and different every time) for all your accounts.

Also, the passwords are not stored anywhere, they are generated using an encryption algorithm
each time you select an account. 

The files that the application saves don't contain your passwords, but just the information
needed to generate them. Those files are useless without your master password. 
You could send them to everyone without any problem.
This grants maximum safety.
