import os
import sys
import ctypes
import time
import subprocess

def set_tiny_font(font_size=5):
    """Sets console font to size 5 for high resolution."""
    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
    class CONSOLE_FONT_INFOEX(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong), ("nFont", ctypes.c_ulong),
                    ("dwFontSize", COORD), ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint), ("FaceName", ctypes.c_wchar * 32)]
    
    STD_OUTPUT_HANDLE = -11
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.dwFontSize.X = 0 
    font.dwFontSize.Y = font_size 
    font.FontWeight = 400 
    font.FaceName = "Consolas" 
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, False, ctypes.byref(font))

def force_maximize():
    """Forces window to maximize."""
    kernel32 = ctypes.windll.kernel32
    user32 = ctypes.windll.user32
    hWnd = kernel32.GetConsoleWindow()
    if hWnd:
        user32.ShowWindow(hWnd, 3) # SW_MAXIMIZE

def main():
    print("Setting up High-Res Display...")
    
    # 1. Set Font
    set_tiny_font(5)
    
    # 2. Maximize
    force_maximize()
    
    # 3. Wait a moment for Windows to resize the buffer
    time.sleep(1.0)
    
    # 4. Run the Main App in THIS same window
    print("Launching TUI...")
    subprocess.run([sys.executable, "main_app.py"])

if __name__ == "__main__":
    main()