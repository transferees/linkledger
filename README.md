# LinkLedger

LinkLedger is a lightweight Python tool that watches your computer’s network interfaces and records changes to their status and assigned IP addresses.

It checks periodically and appends detected changes to a local JSON Lines (`.jsonl`) log. It does not scan other devices or capture network traffic.

## Features

- Detects when an interface appears, disappears, comes up, or goes down
- Records changes to assigned IP addresses
- Writes timestamped events to a local log file
- Omits MAC addresses from recorded data

## Requirements

- Python 3.8+
- `psutil`

## Installation

```bash
python -m pip install psutil
