import sys
# The exact path to the folder that contains your package/module file(s)
# Use a raw string (r'...') or double backslashes (\\) for Windows paths
CUSTOM_PACKAGE_PATH = r'C:\Users\Omer Rastgar\AppData\Local\Programs\Python\Python313\Lib\site-packages'

# Add the custom path to the list of directories Python searches
sys.path.append(CUSTOM_PACKAGE_PATH)


import curses
import mss
import time
import pyautogui
from PIL import Image
import uiautomation as auto
import sys

# Try import
try:
    import pyfiglet
    HAS_FIGLET = True
except ImportError:
    HAS_FIGLET = False

TARGET_FPS = 15

def get_text_under_mouse(element):
    try:
        if not element: return ""
        try:
            pat = element.GetPattern(auto.PatternId.ValuePattern)
            if pat and pat.Value: return pat.Value
        except: pass
        if element.Name: return element.Name
        try:
            child = element.GetFirstChildControl()
            if child and child.Name: return child.Name
        except: pass
        return ""
    except: return ""

def draw_screen(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    
    sct = mss.mss()
    monitor = sct.monitors[1]
    
    if HAS_FIGLET:
        f = pyfiglet.Figlet(font='standard') 
    
    BG_CHARS = " ..::xx##"
    frame_dur = 1.0 / TARGET_FPS
    last_big_text = "Ready..."
    last_type = "System"

    try:
        while True:
            start_time = time.time()
            
            # --- RESIZE CHECK ---
            try:
                rows, cols = stdscr.getmaxyx()
            except: continue
            
            # If window is closed/tiny, skip frame to prevent crash
            if rows < 10 or cols < 10: 
                time.sleep(0.1)
                continue

            split_row = int(rows * 0.6)
            map_h = split_row
            map_w = cols - 1

            # --- MAP ---
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img_small = img.resize((map_w, map_h), Image.Resampling.NEAREST)
            pixels = list(img_small.convert("L").getdata())
            
            mouse_x, mouse_y = pyautogui.position()
            mx = int((mouse_x / monitor["width"]) * map_w)
            my = int((mouse_y / monitor["height"]) * map_h)

            stdscr.move(0, 0)
            bg_len = len(BG_CHARS) - 1

            for y in range(map_h):
                row_idx = y * map_w
                row_px = pixels[row_idx : row_idx + map_w]
                row_chars = [BG_CHARS[int(p/255 * bg_len)] for p in row_px]
                
                if y == my and 0 <= mx < len(row_chars):
                    row_chars[mx] = "▲"
                
                try:
                    stdscr.addstr(y, 0, "".join(row_chars))
                except: pass
            
            try:
                stdscr.addstr(split_row, 0, "=" * (cols-1))
            except: pass

            # --- TEXT ---
            try:
                el = auto.ControlFromPoint(mouse_x, mouse_y)
                found = get_text_under_mouse(el)
                if found:
                    last_big_text = found
                    last_type = el.ControlTypeName
            except: pass

            # --- RENDER GIANT TEXT ---
            start_y = split_row + 2
            
            # Clear old text
            for erase_y in range(start_y, rows - 1):
                try:
                    stdscr.addstr(erase_y, 0, " " * (cols - 1))
                except: pass

            try:
                lbl = f" [{last_type}] "
                stdscr.addstr(split_row, 2, lbl, curses.A_REVERSE)
            except: pass
            
            if HAS_FIGLET:
                try:
                    f.width = cols - 4
                    ascii_art = f.renderText(last_big_text)
                    ascii_lines = ascii_art.split("\n")
                    for i, line in enumerate(ascii_lines):
                        if start_y + i >= rows - 1: break
                        try:
                            stdscr.addstr(start_y + i, 1, line, curses.A_BOLD)
                        except: pass
                except:
                    stdscr.addstr(start_y, 1, last_big_text)
            else:
                stdscr.addstr(start_y, 1, last_big_text)

            stdscr.refresh()
            
            elapsed = time.time() - start_time
            wait = frame_dur - elapsed
            if wait > 0: time.sleep(wait)
            
            if stdscr.getch() == ord('q'): break

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    try:
        curses.wrapper(draw_screen)
    except Exception as e:
        # If it crashes, print why and wait so you can read it
        print(f"Error: {e}")
        input("Press Enter to Exit...")