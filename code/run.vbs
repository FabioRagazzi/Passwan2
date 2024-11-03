Set shell = CreateObject("WScript.Shell")

' Path to the Python executable inside your virtual environment
pythonExe = "venv\Scripts\python.exe"

' Path to the Python script you want to run
pythonScript = "modern_swan.py"

' Run the Python script without showing a terminal window
shell.Run """" & pythonExe & """ """ & pythonScript & """", 0