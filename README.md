# 💻 TUI Remote Desktop (Stage 1: The Inspector)

A High-Performance Text-Based Interface for Remote System Interaction.

⚠️ **Project Status: Stage 1 (Proof of Concept)**

This is the foundational phase of a larger initiative to build a fully functional TUI-based RDP/VNC client.

The Goal: To allow full remote desktop control over extremely **low-bandwidth connections** (e.g., slow satellite links, GPRS) by rendering the desktop entirely in text.

Current Focus: Solves the "**Visibility**" problem—how to read screen content when a video stream is too slow or blurry.

![WhatsApp Image 2025-12-16 at 6 28 05 PM](https://github.com/user-attachments/assets/0125bee5-7c18-4d25-b2a1-94211338ae78)

---

## 🚀 Current Status: Stage 1 (The "Inspector")

At this stage, the project focuses on **Legibility** over visual fidelity. Instead of trying to squeeze a 1080p image into a terminal, it uses a hybrid approach:

* **Visual Navigation (The Map):** A low-fidelity, real-time ASCII map of the desktop helps you locate windows and understand layout.
* **Semantic Inspection (The Reader):** A "Smart Inspector" bypasses visual pixels and asks the OS (via UI Automation) exactly what text, button, or file is under your mouse cursor.
* **High-Res Rendering:** It forces the terminal into a "micro-font" mode (Size **5px**), creating a massive grid (e.g., **400x150 chars**) for maximum detail.

### ✨ Key Features

* **Auto-Resolution Scaling:** Includes a launcher that forces the terminal font to 5px and maximizes the window for "**HD**" text resolution.
* **Smart Text Extraction:** Uses Windows **UI Automation** to "**read**" buttons, menus, and code editors even if they are visually blurry.
* **Giant Text Display:** Renders the text under your cursor using `pyfiglet` ASCII art, making it readable instantly without squinting.
* **Ghost-Free Engine:** Custom rendering logic clears the text buffer frame-by-frame to prevent visual artifacts.

---

## 🛠️ Installation

### Prerequisites

* **OS:** Windows 10/11 (Required for the `uiautomation` and `ctypes` font scaling APIs).
* **Python:** 3.8 or higher.
* **Terminal:** CMD or PowerShell (Windows Terminal users may need to adjust profiles manually).

### Dependencies

Install the required libraries:

    pip install windows-curses mss pyautogui pillow uiautomation pyfiglet

---

## 🏃‍♂️ Usage

This project uses a two-part system: a `Launcher` (to set up the environment) and the `Main App` (the logic).

1.  Download the files. Ensure `launcher.py` and `main_app.py` are in the same folder.
2.  Run the Launcher:

    python launcher.py

    (Do not run `main_app.py` directly; the resolution will be too low.)

### How to Use:

* **Move Mouse:** Move your physical mouse. The "**Triangle**" cursor on the TUI will follow.
* **Inspect:** Hover over any text, button, or file.
* **Read:** The bottom half of the terminal will display the content in **GIANT BLOCK TEXT**.
* **Quit:** Press `q` or `Ctrl+C`.

---

## 🗺️ Roadmap

* [x] **Stage 1:** Read-only visibility via "**Inspection**" and ASCII mirroring.
* [ ] **Stage 2:** Interactive Input. Sending mouse clicks and keyboard events from the TUI to the host.
* [ ] **Stage 3:** Network Layer. Separating the "Viewer" from the "Host" to run over SSH/TCP.
* [ ] **Stage 4:** Protocol Integration. Full RDP/VNC handshake implementation for standalone use.

---

## 🤝 Contributing

This is an experimental project. Contributions are welcome, specifically for:

* Optimizing the frame rate of the `curses` loop.
* Improving UI Automation support for non-native apps (e.g., Electron/Chrome).
* Porting the "**Inspector**" logic to Linux (using `at-spi`).

**Author:** [Your Name/Handle]\
**License:** MIT
