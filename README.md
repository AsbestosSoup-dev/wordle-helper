# 🧩 Wordle Helper CLI

**Wordle Helper CLI** is a fast, offline command-line tool that helps you solve Wordle puzzles using smart pattern matching and letter filtering logic.  
It supports flexible inclusion/exclusion of letters, handles duplicate letters correctly, and automatically downloads a full English word list on first run.

---

## ✨ Features

- 🔍 **Pattern-based search** — Use `?` for unknown letters (`a??le` finds *apple*).
- 🧠 **Smart letter filtering** — Include known letters, exclude gray ones, and handle yellow/gray duplicates accurately.
- ⚙️ **Offline operation** — Automatically downloads `words.txt` once, then runs fully offline.
- 💡 **Intuitive interface** — Color-coded prompts and feedback for clarity.
- 🧾 **Cross-platform** — Works on macOS, Windows, and Linux.  
  Can be compiled into a single binary using **PyInstaller**.

---

## 🖥️ Installation

### Using the included installer script (recommended)
```bash
git clone https://github.com/AsbestosSoup/wordle-helper.git
cd wordle-helper
bash install.sh
```

This will:
- Create a virtual environment in `.venv`
- Upgrade `pip`
- Install dependencies from `requirements.txt`
- Create a convenience launcher script (`run.sh`)

Then, to start the app:
```bash
bash run.sh
```

---

### Manual installation
If you prefer to set things up manually:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

---

## 🧱 Building a Binary

To create a single-file executable:
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

The compiled binary will appear in the `dist/` folder as `wordle-helper`.  
When run for the first time, it will automatically download `words.txt` into the same directory.

---

## 🗂️ Project Structure

```
wordle-helper/
├── main.py          # CLI entry point
├── utils.py         # Core logic and formatting
├── install.sh       # Installer that creates .venv and sets up run.sh
├── run.sh           # Launcher script
├── requirements.txt # Python dependencies
├── LICENSE          # License file (MIT or similar)
└── README.md        # This file
```

---

## 📦 Download

If you just want to run it quickly, download the latest binary from the  
**[Releases](https://github.com/AsbestosSoup/wordle-helper/releases)** page.

---

## ⚖️ License

This project is licensed under the terms of the [LICENSE](LICENSE) file.
