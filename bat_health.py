#!/usr/bin/env python3
"""
battery_health.py
-----------------
A simple script to gather and display battery health info on Linux systems.

USAGE:
  1) Just run the script directly:
     ./battery_health.py
  2) Or make it a system alias if you like:
     alias bathealth="~/battery_health.py"
"""

import os
import sys
import math

# Adjust this if your battery device is named something else
BATTERY_PATH = "/sys/class/power_supply/BAT1"

def color_text(text, color_code):
    """Return the given text with ANSI color codes."""
    return f"\033[{color_code}m{text}\033[0m"

def read_sysfs_value(file_name):
    """Read a value from a sysfs file under BATTERY_PATH safely.""" 
    path = os.path.join(BATTERY_PATH, file_name)
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except PermissionError:
        return None

def main():
    # Check if BATTERY_PATH exists
    if not os.path.isdir(BATTERY_PATH):
        print(color_text(f"Error: Battery path '{BATTERY_PATH}' not found.", "91"))
        print("Are you sure this is the correct battery device on your system?")
        sys.exit(1)

    status = read_sysfs_value("status") or "Unknown"
    capacity_str = read_sysfs_value("capacity") or "0"
    capacity = int(capacity_str) if capacity_str.isdigit() else 0

    # Some systems use 'energy_full' and 'energy_full_design' (in mWh)
    # Others might use 'charge_full' and 'charge_full_design' (in mAh).
    # We'll attempt to read both forms gracefully.
    energy_full_str = read_sysfs_value("energy_full") or read_sysfs_value("charge_full")
    energy_design_str = read_sysfs_value("energy_full_design") or read_sysfs_value("charge_full_design")

    cycle_count_str = read_sysfs_value("cycle_count")
    technology = read_sysfs_value("technology") or "Unknown"

    # Convert them to floats if possible
    def to_float(s):
        try:
            return float(s)
        except (ValueError, TypeError):
            return 0.0

    energy_full = to_float(energy_full_str)
    energy_design = to_float(energy_design_str)
    cycle_count = to_float(cycle_count_str) if cycle_count_str else None

    # Estimate battery health as ratio of full vs. design
    # e.g., if full=40000 mWh and design=50000 mWh, health ~ 80%
    health = 0.0
    if energy_full > 0 and energy_design > 0:
        health = (energy_full / energy_design) * 100

    # Color-code the capacity
    if capacity >= 80:
        capacity_color = "92"  # green
    elif capacity >= 30:
        capacity_color = "93"  # yellow
    else:
        capacity_color = "91"  # red

    # Color-code the health
    # Typically, battery is considered "fair" if above ~80%.
    if health >= 85:
        health_color = "92"  # green
    elif health >= 60:
        health_color = "93"  # yellow
    else:
        health_color = "91"  # red

    # Print out the info
    print("\nBattery Health Report\n" + "-"*40)
    print(f" Status         : {status}")
    print(f" Capacity       : {color_text(f'{capacity}%', capacity_color)}")
    if cycle_count is not None:
        print(f" Cycle count    : {int(cycle_count)}")
    else:
        print(" Cycle count    : Unknown (not supported)")
    print(f" Technology     : {technology}")

    if health > 0:
        print(f" Health (est.)  : {color_text(f'{health:.2f}%', health_color)}")
    else:
        print(" Health (est.)  : Unknown (missing data)")

    print()

if __name__ == "__main__":
    main()
