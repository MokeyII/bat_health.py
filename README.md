# Battery Health Monitor

This Python script retrieves and displays battery health information for Linux systems using the sysfs interface. It provides insights into battery status, capacity, cycle count, and estimated health percentage.

---

## Features

- Displays current battery status (e.g., Charging, Discharging, Full).
- Shows battery capacity and cycle count (if supported).
- Estimates battery health as a percentage of the original design capacity.
- Color-coded output for easy readability:
  - **Green**: Good battery health/capacity.
  - **Yellow**: Moderate battery health/capacity.
  - **Red**: Low battery health/capacity.

---

## Requirements

- **Python 3**
- A Linux system with battery information available under `/sys/class/power_supply/`.
- Ensure you have read permissions for battery-related sysfs files (may require `sudo` on some systems).

---

## Tutorial

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/battery-health-monitor.git
cd battery-health-monitor
```

### 2. Make the Script Executable

```bash
chmod +x bat_health.py
```

### 3. Run the Script

#### Basic Usage:
```bash
./bat_health.py
```

#### Run with Python Directly:
```bash
python3 bat_health.py
```

If the battery information is in a path other than `/sys/class/power_supply/BAT1`, update the `BATTERY_PATH` variable in the script accordingly.

---

## Usage

1. Just run the script directly:
   ```bash
   ./battery_health.py
   ```

2. Or make it a system alias if you like:
   ```bash
   alias bathealth="~/battery_health.py"
   ```

---

## Example Output

If the script successfully retrieves battery data, the output will look like this:

```
Battery Health Report
----------------------------------------
 Status         : Discharging
 Capacity       : 85% (Green text)
 Cycle count    : 120
 Technology     : Li-ion
 Health (est.)  : 95.00% (Green text)
```

If the battery information is unavailable or the path is incorrect, an error message will appear:

```
Error: Battery path '/sys/class/power_supply/BAT1' not found.
Are you sure this is the correct battery device on your system?
```

---

## How It Works

1. **Battery Path**: Reads battery data from `/sys/class/power_supply/BAT1` by default. Update the `BATTERY_PATH` variable in the script if needed. You can find this by running `ls /sys/class/power_supply/`
2. **Retrieve Data**: Gathers information on status, capacity, energy levels, cycle count, and battery technology.
3. **Calculate Health**: Estimates health as a percentage of the current full charge vs. design capacity.
4. **Color-Coding**: Adds color-coded output to highlight key metrics.


### Cycle Count

The cycle count refers to the number of charge and discharge cycles that the battery has gone through. 

A charge cycle is typically defined as using 100% of the battery's capacity, whether done in one full discharge or incrementally (e.g., using 50% twice counts as one cycle).

The cycle count is retrieved from the battery's sysfs files, specifically from `/sys/class/power_supply/BAT1/cycle_count` (or the equivalent path for your battery). This value provides an estimate of the battery's usage and wear over time, as the number of cycles is a key metric for determining a battery's lifespan.

Modern batteries are designed to last for a certain number of cycles (e.g., 300–1000 cycles) before their capacity significantly degrades. If the cycle count value is not supported on your system, the script will display it as "Unknown."

---

## Troubleshooting

- **Permission Issues**:
  Run the script with `sudo` if you encounter permission errors accessing sysfs files:
  ```bash
  sudo ./bat_health.py
  ```

- **Incorrect Battery Path**:
  Check your system's battery path under `/sys/class/power_supply/` and update `BATTERY_PATH` in the script.

---

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute it.

---

Monitor your battery health with ease!

