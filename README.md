

```markdown
# 🖥️ System Health & Cleanup Utility

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)]()

> A safe, beginner-friendly Python utility for Windows system cleanup, health checks, and security hardening. Includes AI-era scam awareness tips. Safe by default with dry-run mode.

![Screenshot placeholder](docs/screenshot.png)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧹 **Safe Cleanup** | Cleans temp files & browser cache — never touches passwords or bookmarks |
| ❤️ **Health Check** | Disk space, memory usage, top CPU processes, pending updates |
| 🛡️ **Security Hardening** | Disable SMBv1, RDP, Remote Registry, AutoRun (with restore points) |
| 🤖 **Scam Awareness** | Tips for avoiding AI-generated phishing & tech support scams |
| 🔒 **Dry-Run Mode** | Preview all changes before applying — **ON by default** |
| 📝 **Full Logging** | Every action logged to `~/SystemUtility_Logs/` |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/system-health-utility.git
cd system-health-utility
```
```


### 2. Install Dependencies (Optional but Recommended)

```shell script
pip install psutil
```


> `psutil` enables detailed disk, memory, and process info. The tool works without it, but with limited diagnostics.

### 3. Run the Utility

```shell script
python system_health_utility.py
```


> 💡 **Tip:** Right-click → "Run as Administrator" for full functionality.

---

## 📋 Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.10 or higher |
| **OS** | Windows 10 / Windows 11 |
| **Optional** | `psutil` for enhanced system info |

---

## 🎮 Usage

### CLI Menu

```
═══════════════════════════════════════════════════════════
  🖥  SYSTEM HEALTH & CLEANUP UTILITY
═══════════════════════════════════════════════════════════
  Mode: DRY RUN (preview only)
  Platform: Windows | Admin: True
═══════════════════════════════════════════════════════════
  1. Run Health Check
  2. Clean Temp Files
  3. Clean Browser Cache
  4. Show Security Tips
  5. Toggle Dry Run Mode
  6. Exit
═══════════════════════════════════════════════════════════
```


### What Each Option Does

| Option | Action | Safe? |
|--------|--------|-------|
| **1. Health Check** | Shows disk, RAM, CPU, battery status | ✅ Read-only |
| **2. Clean Temp Files** | Deletes old temp files (skips recent/locked) | ✅ Safe |
| **3. Clean Browser Cache** | Clears Chrome/Edge/Firefox cache + flushes DNS | ✅ Safe |
| **4. Security Tips** | Displays AI-era scam awareness tips | ✅ Read-only |
| **5. Toggle Dry Run** | Switch between preview and live mode | — |

---

## 🛡️ Safety Design Principles

This tool is built with **safety first**:

| Principle | Implementation |
|-----------|----------------|
| **Dry-run by default** | No changes until you explicitly toggle it off |
| **Never deletes user data** | Temp/cache only — profiles, passwords, bookmarks untouched |
| **Skips locked files** | Won't crash on files in use |
| **Skips recent files** | Protects running installers (configurable threshold) |
| **Full audit trail** | Every action logged with timestamps |
| **Reversible changes** | Security hardening creates restore points first |

---

## 📁 Project Structure

```
system-health-utility/
├── system_health_utility.py   # Main script
├── README.md                  # This file
├── LICENSE                    # MIT License
├── requirements.txt           # Optional dependencies
└── docs/
    └── screenshot.png         # UI screenshot
```


---

## 🎓 Learning Points

This project demonstrates:

1. **Safe file operations** — Using `pathlib`, `shutil`, and proper error handling
2. **Cross-platform detection** — `platform.system()` for OS-aware code
3. **Subprocess best practices** — No `shell=True`, proper timeout handling
4. **User-friendly CLI** — Clear menus and confirmation prompts
5. **Logging** — Professional audit trails with `logging` module
6. **Graceful degradation** — Works with or without optional dependencies

---

## 🔧 Configuration

Edit these values at the top of `system_health_utility.py`:

```python
CONFIG = {
    "log_dir": pathlib.Path.home() / "SystemUtility_Logs",
    "temp_skip_minutes": 10,  # Skip files modified within this time
    "dry_run": True,          # Set False to apply changes
}
```


---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

```
MIT License — Use freely, modify freely, contributions welcome!
```


---

## ⚠️ Disclaimer

This tool is provided **as-is** for educational purposes. While designed to be safe:

- Always run in **dry-run mode first** to preview changes
- **Back up important data** before running cleanup operations
- The author is not responsible for any data loss or system issues

---

## 🙏 Acknowledgments

- Built with Python 🐍
- Inspired by the need for simple, safe Windows maintenance tools
- Security tips based on real-world scam patterns observed in 2024–2026

---

## 📬 Contact

- **Author:** Your Name
- **LinkedIn:** ((https://www.linkedin.com/in/jmon360/))
- **GitHub:** [@jmon360 (https://github.com/jmon360)

---

<p align="center">
  <b>⭐ Star this repo if you found it useful! ⭐</b>
</p>
```
---

## 📄 `requirements.txt`
```

# Optional but recommended
psutil>=5.9.0
```
---

## 📄 `LICENSE`
```

MIT License

Copyright (c) 2026 jmon360

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
---

## 🔧 Issues Fixed

| Issue | Fix |
|-------|-----|
| Duplicate title headers | Removed redundant `# 🖥️ System Health...` blocks |
| Broken code fences | Fixed ` ```bash` → ````bash` (no space) |
| Missing blank lines | Added required spacing before/after code blocks |
| Broken tables | Restored proper Markdown table formatting |
| Inconsistent blockquotes | Fixed `>` tip formatting |
| Duplicate release notes section | Removed mid-document release template |
| License formatting | Proper line breaks for readability |
| Typo | "contribute welcome" → "contributions welcome" |

Your README is now **GitHub-ready**! 🚀
```


