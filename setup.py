from cx_Freeze import setup, Executable

setup(
    name="KeyLoggerApp",
    version="1.0",
    description="Your application description",
    executables=[Executable("keylogger.py")],
)
