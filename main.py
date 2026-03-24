"""
System Health & Cleanup Utility
===============================
A cross-platform (Windows-focused) system utility for:
- Temp file cleanup
- Browser cache cleanup
- Security posture checks
- AI/Scam awareness tips

GitHub: https://github.com/YOUR_USERNAME/system-health-utility
Author: Your Name
License: MIT

USAGE:
  1. pip install psutil  (optional but recommended)
  2. Run as Administrator for full features:
     python system_health_utility.py
"""

import logging
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime

# Optional: psutil for richer system info
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("💡 TIP: Install psutil for full features: pip install psutil")

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION — Users can edit these defaults
# ═══════════════════════════════════════════════════════════════════
CONFIG = {
    "log_dir": pathlib.Path.home() / "SystemUtility_Logs",
    "temp_skip_minutes": 10,  # Skip files modified within this time
    "dry_run": True,  # Set False to apply changes (safe default)
}

CONFIG["log_dir"].mkdir(parents=True, exist_ok=True)

# Logging setup
_log_file = CONFIG["log_dir"] / f"session_{datetime.now():%Y-%m-%d_%H-%M-%S}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(_log_file, encoding="utf-8"), logging.StreamHandler()],
)
log = logging.getLogger("SystemUtility")


# ═══════════════════════════════════════════════════════════════════
# CROSS-PLATFORM HELPERS
# ═══════════════════════════════════════════════════════════════════

def is_windows() -> bool:
    return platform.system() == "Windows"


def is_admin() -> bool:
    """Check if running with elevated privileges."""
    if is_windows():
        try:
            import ctypes
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False
    else:
        return os.geteuid() == 0  # Unix/Mac


def run_cmd(args: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    """Safe subprocess wrapper — no shell=True."""
    log.debug("Running: %s", " ".join(args))
    try:
        return subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    except Exception as e:
        log.error("Command failed: %s", e)
        return subprocess.CompletedProcess(args, 1, "", str(e))


# ═══════════════════════════════════════════════════════════════════
# CLEANUP FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def safe_delete_folder_contents(path: pathlib.Path, skip_recent_min: int = 10) -> tuple[int, int]:
    """
    Delete files in folder, skipping:
    - Files modified recently (protects running apps)
    - Locked files
    Returns (deleted_count, skipped_count)
    """
    deleted = skipped = 0
    if not path.exists():
        return 0, 0

    cutoff = time.time() - (skip_recent_min * 60)
    for item in path.iterdir():
        try:
            if item.stat().st_mtime > cutoff:
                skipped += 1
                continue
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)
            deleted += 1
        except (PermissionError, OSError):
            skipped += 1
    return deleted, skipped


def clean_temp_files(dry_run: bool = True) -> None:
    """Clean Windows/user temp folders safely."""
    log.info("=" * 50)
    log.info("🧹 TEMP FILE CLEANUP")
    log.info("=" * 50)

    if is_windows():
        targets = [
            pathlib.Path(os.environ.get("TEMP", "")),
            pathlib.Path("C:/Windows/Temp"),
        ]
    else:
        targets = [pathlib.Path("/tmp")]

    for folder in {p.resolve() for p in targets if p.exists()}:
        if dry_run:
            log.info("[DRY RUN] Would clean: %s", folder)
        else:
            d, s = safe_delete_folder_contents(folder, CONFIG["temp_skip_minutes"])
            log.info("Cleaned %s: deleted %d, skipped %d", folder, d, s)


def clean_browser_cache(dry_run: bool = True) -> None:
    """Clear browser disk caches only (not profiles/passwords)."""
    log.info("=" * 50)
    log.info("🌐 BROWSER CACHE CLEANUP")
    log.info("=" * 50)

    if not is_windows():
        log.info("Browser cleanup currently Windows-only. Skipping.")
        return

    cache_paths = {
        "Chrome": pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/User Data/Default/Cache",
        "Edge": pathlib.Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Edge/User Data/Default/Cache",
    }

    # Firefox profiles
    ff_profiles = pathlib.Path(os.environ.get("APPDATA", "")) / "Mozilla/Firefox/Profiles"
    if ff_profiles.exists():
        for profile in ff_profiles.iterdir():
            cache_paths[f"Firefox-{profile.name}"] = profile / "cache2"

    for browser, path in cache_paths.items():
        if path.exists():
            if dry_run:
                log.info("[DRY RUN] Would clean %s cache: %s", browser, path)
            else:
                d, s = safe_delete_folder_contents(path, skip_recent_min=0)
                log.info("Cleaned %s cache: deleted %d, skipped %d", browser, d, s)

    # Flush DNS
    if not dry_run and is_windows():
        run_cmd(["ipconfig", "/flushdns"])
        log.info("DNS cache flushed")


# ═══════════════════════════════════════════════════════════════════
# SYSTEM HEALTH CHECK
# ═══════════════════════════════════════════════════════════════════

def health_check() -> None:
    """Non-destructive system health snapshot."""
    log.info("=" * 50)
    log.info("❤ SYSTEM HEALTH CHECK")
    log.info("=" * 50)

    # Disk space
    log.info("\n📀 Disk Space:")
    if PSUTIL_AVAILABLE:
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                log.info("  %s: %.1f GB free / %.0f GB (%.0f%% used)",
                         part.mountpoint, usage.free / 1e9, usage.total / 1e9, usage.percent)
            except PermissionError:
                pass
    else:
        log.info("  (Install psutil for disk info)")

    # Memory
    log.info("\n🧠 Memory:")
    if PSUTIL_AVAILABLE:
        mem = psutil.virtual_memory()
        log.info("  %.0f%% used — %.1f GB available of %.0f GB",
                 mem.percent, mem.available / 1e9, mem.total / 1e9)
    else:
        log.info("  (Install psutil for memory info)")

    # Top CPU processes
    log.info("\n⚙ Top CPU Processes:")
    if PSUTIL_AVAILABLE:
        procs = sorted(
            [p.info for p in psutil.process_iter(["pid", "name", "cpu_percent"])],
            key=lambda x: x.get("cpu_percent") or 0, reverse=True
        )[:5]
        for p in procs:
            log.info("  PID %6d: %5.1f%% — %s", p["pid"], p.get("cpu_percent", 0), p["name"])

    # Platform info
    log.info("\n💻 System Info:")
    log.info("  OS: %s %s", platform.system(), platform.release())
    log.info("  Machine: %s", platform.machine())
    log.info("  Python: %s", platform.python_version())


# ═══════════════════════════════════════════════════════════════════
# SECURITY TIPS (AI-ERA AWARENESS)
# ═══════════════════════════════════════════════════════════════════

SECURITY_TIPS = [
    "Microsoft/Apple will NEVER call you about viruses on your PC.",
    "Legitimate AI tools do NOT require you to disable antivirus.",
    "Never paste code into Terminal/PowerShell from a pop-up or unsolicited email.",
    "Tech support scam red flag: being asked to install AnyDesk/TeamViewer by someone who called you.",
    "Before running any .exe: right-click → Properties → Digital Signatures. No signature = high risk.",
    "Use a dedicated browser profile for banking and sensitive accounts.",
    "AI-generated phishing emails are grammatically perfect now — verify sender domains.",
]


def show_security_tips() -> None:
    """Display rotating security awareness tips."""
    log.info("=" * 50)
    log.info("🛡 SECURITY AWARENESS TIPS")
    log.info("=" * 50)
    import random
    for i, tip in enumerate(random.sample(SECURITY_TIPS, min(3, len(SECURITY_TIPS))), 1):
        log.info("  %d. %s", i, tip)


# ═══════════════════════════════════════════════════════════════════
# MAIN MENU
# ═══════════════════════════════════════════════════════════════════

def main_menu():
    """Simple CLI menu for the utility."""
    print("\n" + "=" * 55)
    print("  🖥  SYSTEM HEALTH & CLEANUP UTILITY")
    print("=" * 55)
    print(f"  Mode: {'DRY RUN (preview only)' if CONFIG['dry_run'] else 'LIVE (changes applied)'}")
    print(f"  Platform: {platform.system()} | Admin: {is_admin()}")
    print("=" * 55)
    print("  1. Run Health Check")
    print("  2. Clean Temp Files")
    print("  3. Clean Browser Cache")
    print("  4. Show Security Tips")
    print("  5. Toggle Dry Run Mode")
    print("  6. Exit")
    print("=" * 55)

    while True:
        choice = input("\nSelect option (1-6): ").strip()
        if choice == "1":
            health_check()
        elif choice == "2":
            clean_temp_files(CONFIG["dry_run"])
        elif choice == "3":
            clean_browser_cache(CONFIG["dry_run"])
        elif choice == "4":
            show_security_tips()
        elif choice == "5":
            CONFIG["dry_run"] = not CONFIG["dry_run"]
            print(f"Dry run mode: {'ON' if CONFIG['dry_run'] else 'OFF'}")
        elif choice == "6":
            print("Goodbye! Stay secure. 🛡")
            break
        else:
            print("Invalid choice. Enter 1-6.")


if __name__ == "__main__":
    if not is_admin():
        print("⚠ TIP: Run as Administrator for full features.\n")
    main_menu()
