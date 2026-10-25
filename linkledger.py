import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import psutil


def snapshot():
    addresses = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    result = {}

    for name in sorted(set(addresses) | set(stats)):
        info = stats.get(name)
        ips = []

        for address in addresses.get(name, []):
            if address.family == psutil.AF_LINK:
                continue
            if address.address:
                ips.append(address.address)

        result[name] = {
            "up": info.isup if info else None,
            "addresses": sorted(set(ips)),
        }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Record changes to this computer's network interfaces."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=5,
        help="Seconds between checks (default: 5)",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=Path("linkledger.jsonl"),
        help="Local JSONL log file (default: linkledger.jsonl)",
    )
    args = parser.parse_args()

    if args.interval <= 0:
        parser.error("--interval must be greater than 0")

    previous = snapshot()
    print(f"Watching local network interfaces. Logging to {args.log}")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(args.interval)
            current = snapshot()

            if current != previous:
                event = {
                    "time": datetime.now(timezone.utc).isoformat(),
                    "before": previous,
                    "after": current,
                }
                with args.log.open("a", encoding="utf-8") as log_file:
                    log_file.write(json.dumps(event) + "\n")

                print(f"[{event['time']}] Network interface change recorded.")
                previous = current

    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
