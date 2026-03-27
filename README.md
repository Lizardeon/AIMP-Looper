
# AIMP Looper

A lightweight Python utility for **AIMP Player** that allows you to define custom loops (sections) within tracks and switch between them seamlessly in real-time. 

Perfect for musicians practicing specific song parts or DJs who want to extend track sections.

---

## Features
* **Automatic Track Detection**: Syncs with AIMP to find loops for the currently playing song.
* **Smart Transitions**: Queue the next loop; it will wait for the current one to finish before switching.
* **Live Reload**: Update your `loops.txt` file and reload it without restarting the script.
* **CLI Interface**: Simple, numbered controls for easy navigation.

---

## Installation

1.  **Enable AIMP WebControl**:
    * Open AIMP Settings -> Plugins.
    * Ensure **WebControl** is enabled (this script uses it to communicate with the player).
2.  **Install Dependencies**:
    ```bash
    pip install pyaimp
    ```
3.  **Download the Script**:
    Save `aimp_looper.py` and create a `loops.txt` in the same folder.

---

## Configuration (`loops.txt`)

The script looks for a file named `loops.txt`. Use the following format:
* `#` followed by the **exact** track title in AIMP.
* `Start Time | End Time | Name` (Time format: `MM:SS.mmm`)

**Example:**
```text
# Interstellar Main Theme
00:00.000 | 00:45.000 | Intro
00:45.000 | 02:10.500 | Build Up
02:10.500 | 03:30.000 | Climax

# Stay Hgh - Tove Lo
00:15.000 | 00:45.200 | Verse 1
```

---

## How to Use

1.  Start AIMP and play a track defined in your config.

2.  Run the script:
    ```bash
    python aimp_looper.py
    ```

3.  **Controls**:
    * **[Numbers]**: Type a number and hit Enter to queue that loop.
    * **[R]**: Reload the `loops.txt` file after making changes.
    * **[Q]**: Quit the application.

---

## Requirements
* Windows (AIMP is Windows-native).
* Python 3.x.
* [pyaimp](https://pypi.org/project/pyaimp/) library.
