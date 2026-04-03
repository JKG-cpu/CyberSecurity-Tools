# fim — File Integrity Monitor

A command-line tool that detects unauthorized changes to files and folders using SHA-256 hashing. Run a baseline scan, then re-scan later to see exactly what was modified, added, or deleted.

## Installation

```
pip install file-integrity-monitor
```

Or with uv:

```
uv tool install file-integrity-monitor
```

## Usage

```
fim <path>
```

**Examples:**

```
fim "C:/Users/You/Documents"
fim ~/Desktop
fim . 
fim "C:/Users/You/Documents" --desktop
```

## Flags

| Flag | Description |
|------|-------------|
| `--desktop` | Save the log file to your Desktop instead of the default logs/ folder |
| `--log-dir <path>` | Save the log file to a custom directory |

## How it works

1. First scan — a baseline is created, storing the SHA-256 hash of every file
2. Subsequent scans — hashes are compared against the baseline and any changes are reported
3. A timestamped log file is saved after every scan with the full details

## Output

```
File Integrity Monitor
Scan: 2026-03-11 14:32:05

Changes detected!
    Modified : 2 files
    Added    : 1 file
    Deleted  : 1 file

Log file: C:/Users/You/fim/logs/scan_2026-03-11_14-32-05.txt
```

## Requirements

- Python 3.11+
- rich

## Source

https://github.com/JKG-cpu/CyberSecurity-Tools/tree/main/File%20Integrity%20Monitor

## License

MIT