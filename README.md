# Passwan 2.0 
<img src="img/passwan2.ico" alt="folder" width="100">

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

You can also download the code using *git* by running on your terminal the command:
```
git clone https://github.com/FabioRagazzi/Passwan2.git
```
Please note that in order to do that you will need *git* installed on your computer.

To open your terminal you can:
- Press **Windows** + **R**
- Type **cmd**
- Press **Enter**

### Creating the virtual environment
Once you have the code on your machine, you will need to set up a python virtual environment,
that is basically a folder with all the packages needed to run your code.
You can do that by navigating inside the `code/` folder of the project and double-clicking 
on the file `initial_set_up.bat`. This will open your terminal, create the virtual environment, install all the necessary
python packages, and close the terminal once the operation is completed.

### Running Passwan 2.0
If you completed the above steps, you can launch the application just by double-clicking on the file `run.vbs`
that is inside the folder `code/`.
If you have an antivirus, it might complain about the execution of such file.


If you were able to run the application, you could also create a shortcut to the file `run.vbs` and place it wherever you like 
(usually you want to have it on your desktop).
You can rename the shortcut and maybe even change the icon 
(a good choice for the icon might be the file `passwan2.ico` that you have inside the folder `img/`).

To change the icon of a file you need to:
- Right-click on that file
- Select **Properties** (maybe after having clicked on **Show more options**)
- Click on **Change Icon...**
- Browse your desired **.ico** file

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
inside some `.json` files. You can specify the directory where those files will be saved (the default is
the same directory of your project, inside the `code/` folder, and if you are happy with it, you can leave it like that).

If you want to change the path, a good choice could be some directory with a back-up on the cloud 
(for example with **OneDrive** or **Google Drive** or whatever). To change the path, click on the 
**Settings** button in the main window. Another screen will open, make sure that the option *JSON MODE* is selected,
and then you will be able to browse your
desired directory by clicking on the folder icon: 

<img src="img/folder.png" alt="folder" width="100">

### DataBase Mode
You can store the data needed for the application to work in a Firebase real time database.
To do that, you will first need to create a database.

You can watch this video [Firebase with Python](https://www.youtube.com/watch?v=BnrkTpgH5Vc)
to see how to do it. 
In particular, you can watch:
- 0:55 - 2:25 to learn how to set up the database
and where to find the database url
- 4:29 - 4:54 to see how you can generate a certificate (a `.json` file)
with your private key to access the database

You will need to save the certificate in your computer, in a place you will remember.
Also, you will need the database url.

To switch to database mode, click on the **Settings** button and a new window will open. 
You will need to select the option *DATABASE MODE* and browse the 
certificate file (that you previously downloaded) by clicking on the file icon: 

<img src="img/file.png" alt="folder" width="100">


In the same window you will also need to paste the url of your database.


## Advantages of Using Passwan 2.0
Using Passwan 2.0, you will need to remember just one password, but at the same time
you will get some very safe ones (and different every time) for all your accounts.

Also, the passwords are not stored anywhere, they are generated using an encryption algorithm
each time you select an account. 

The files that the application saves don't contain your passwords, but just the information
needed to generate them. Those files are useless without your master password. 
You could send them to everyone without any problem.
This grants maximum safety.

## Acknowledgments
- **Yuliya Murakami**, for trying to test this application but ending up testing the previous version instead 
(much uglier and difficult to use)
- **Arturo Popoli**, for creating such a great name for this application
- **Elisa Ragazzi**, for spending some time trying to install this application following my instructions
(which resulted in finding herself with an impossible-to-delete file on her computer)

