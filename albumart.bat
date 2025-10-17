REM This batch file is necessary solely because you can't reliably call a .py
REM from foobar's nowplaying plugin, it doesn't seem to honor the OS file associations.

REM Change CWD to the folder this batch file is located in
cd /D "%~dp0"
REM Run the python script
albumart.py %1