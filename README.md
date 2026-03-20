# CANopen Stepper Motor Driver

[![Python CI](https://github.com/Simon2022s/CANopen-Stepper-Motor-Driver/actions/workflows/python-ci.yml/badge.svg)](https://github.com/Simon2022s/CANopen-Stepper-Motor-Driver/actions/workflows/python-ci.yml)

A PyQt5-based CANopen stepper motor driver control software for UC42 series drivers. Supports position mode, velocity mode, and homing mode via CANopen protocol.

## Overview

This project is developed for the UC42 CANopen communication stepper motor driver. It provides a graphical user interface for configuring CANopen connections, sending CAN frames, and controlling the motor driver.

## Features

### 1. CANopen Network Settings
- **Port Types**: PCAN, UARTCAN, socketCAN
- **Serial Port Settings** (for serial-to-CAN gateway):
  - COM port selection
  - Serial baud rate setting (9600-921600)
- **CAN Settings**:
  - CAN bitrate selection (125K, 250K, 500K, 800K, 1M)
- **Connection Control**:
  - Connect/Disconnect buttons
  - Status display

### 2. Manual CAN Command
- **ID Input**: Enter CAN ID (e.g., 0x601)
- **Data Input**: Enter CAN data bytes (e.g., 2B 40 60 00 00 00 00 00)
- **Send/Clear buttons**: Send CAN frame or clear input fields

### 3. Communication Logs
- Real-time display of TX/RX messages
- Timestamps for each message
- Save logs to file functionality

## Installation

### Prerequisites

- Python 3.8+
- PyQt5 >= 5.15.0
- pyserial >= 3.5

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install core dependencies:

```bash
pip install PyQt5 pyserial
```

## Usage

### Run the Program

```bash
python canopen_main.py
```

Or use the launcher:

```bash
python run.py
```

### Basic Operations

1. **Select Port Type**: Choose PCAN, UARTCAN, or socketCAN
2. **Configure Channel**: Enter the appropriate channel (e.g., COM3 for UARTCAN, PCAN_USBBUS1 for PCAN)
3. **Set CAN Bitrate**: Select the CAN bitrate (default: 500K)
4. **Click Open**: Connect to the CAN bus
5. **Send CAN Commands**: Enter CAN ID and Data, then click Send
6. **View Logs**: Monitor communication in the logs area

### UARTCAN Settings

When selecting UARTCAN port type, a dialog will appear to configure the serial baud rate:
- Options: 9600, 19200, 38400, 57600, 115200 (default)

## File Structure

```
CANopen Stepper Motor Driver/
├── canopen_main.py          # Main program
├── canopen_ui.py            # UI definition
├── bruce_bg.jpg             # Background image
├── requirements.txt         # Dependencies
├── run.py                   # Launcher script
├── start.bat                # Windows launcher
└── INSTALL.md               # Installation guide
```

## CANopen Protocol

### Supported Port Types

1. **PCAN**: PEAK-System CAN adapters
2. **UARTCAN**: Serial-to-CAN gateway
3. **socketCAN**: Linux CAN interface

### CAN Bitrate Options

- 125K (125 kbps)
- 250K (250 kbps)
- 500K (500 kbps) - Default
- 800K (800 kbps)
- 1M (1000 kbps)

## Hardware Connection

1. Use a serial-to-CAN gateway to connect PC and UC42 driver
2. Connect CANH and CANL signal lines
3. Ensure terminal resistor (120Ω) is correctly configured

## Development

### Running in Development Mode

```bash
python canopen_main.py
```

### Dependencies

```
PyQt5>=5.15.0
pyserial>=3.5
```

## License

MIT License

## Acknowledgments

- PyQt5 - GUI framework
- pySerial - Serial communication library
- UC42 CANopen Stepper Motor Driver manual

## Notes

1. **Electrical Safety**: Ensure power supply voltage is within DC12-36V range
2. **CAN Bus**: Pay attention not to reverse CANH and CANL connections
3. **Node ID**: Ensure node IDs do not conflict on the network
4. **Bitrate**: All nodes must use the same CAN bitrate
5. **Terminal Resistor**: 120Ω terminal resistors must be connected at both ends of CAN bus

---

**Note**: This software is for learning and testing purposes only. Please test thoroughly before using in industrial environments.