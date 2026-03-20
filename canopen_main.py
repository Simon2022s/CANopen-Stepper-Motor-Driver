#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CANopen Stepper Motor Driver - Fixed Version
Port selection automatically matches Channel
"""

import sys
import os
from datetime import datetime

# Enable High DPI support
from PyQt5 import QtCore
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QTimer, pyqtSignal, QObject

from canopen_ui import Ui_MainWindow, CANopenButton, UartcanDialog


class CANopenCommunication(QObject):
    """CANopen Communication Handler"""
    message_received = pyqtSignal(str, int, list)
    connection_status = pyqtSignal(bool, str)
    
    def __init__(self):
        super().__init__()
        self.connected = False
    
    def connect(self, port, baudrate, can_rate):
        self.connected = True
        self.connection_status.emit(True, f"Connected: {port} @ {can_rate}")
        return True
    
    def disconnect(self):
        self.connected = False
        self.connection_status.emit(False, "Disconnected")


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window"""
    
    # Default Channel values for different Port types
    CHANNEL_DEFAULTS = {
        "PCAN": "PCAN_USBBUS1",
        "UARTCAN": "COM3",
        "socketCAN": "can0"
    }
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.connected = False
        self.uartcan_baud = "115200"
        self.canopen = CANopenCommunication()
        self.canopen.message_received.connect(self.on_can_message)
        self.canopen.connection_status.connect(self.on_connection_status)
        
        self.setup_connections()
        
        # Initialize Channel default values
        self.update_channel_default()
        
        self.read_timer = QTimer()
        self.read_timer.timeout.connect(self.read_can_messages)
        self.read_timer.start(100)
    
    def setup_connections(self):
        """Connect signals and slots"""
        self.comboBox_port.currentTextChanged.connect(self.on_port_changed)
        self.pushButton_open.clicked.connect(self.on_open)
        self.pushButton_close.clicked.connect(self.on_close)
        self.pushButton_send.clicked.connect(self.on_send)
        self.pushButton_clear.clicked.connect(self.on_clear)
        self.pushButton_fault_reset.clicked.connect(self.on_fault_reset)
        
        # Velocity & Position Mode
        self.comboBox_op_mode.currentTextChanged.connect(self.on_op_mode_changed)
        self.pushButton_start.clicked.connect(self.on_mode_start)
        self.pushButton_move_abs.clicked.connect(self.on_move_absolute)
        self.pushButton_move_rel.clicked.connect(self.on_move_relative)
        self.pushButton_stop.clicked.connect(self.on_mode_stop)
        
        # Homing Mode
        self.pushButton_homing_start.clicked.connect(self.on_homing_start)
        self.pushButton_homing_stop.clicked.connect(self.on_homing_stop)
        
        self.pushButton_clear_logs.clicked.connect(self.on_clear_logs)
        self.pushButton_save_logs.clicked.connect(self.on_save_logs)
        
        # Initialize mode-specific UI
        self.on_op_mode_changed("Position")
    
    def update_channel_default(self):
        """Update Channel default value based on current Port"""
        port = self.comboBox_port.currentText()
        if port in self.CHANNEL_DEFAULTS:
            self.lineEdit_channel.setText(self.CHANNEL_DEFAULTS[port])
    
    def on_port_changed(self, text):
        """Port changed - Update Channel default value"""
        # Update Channel to default value for the corresponding type
        self.update_channel_default()
        
        if text == "UARTCAN":
            dialog = UartcanDialog(self)
            result = dialog.exec_()
            if result == QtWidgets.QDialog.Accepted:
                self.uartcan_baud = dialog.baud_rate
                self.log_message(f"UARTCAN: {self.uartcan_baud}")
            else:
                self.log_message("UARTCAN: Cancelled")
    
    def on_open(self):
        """Open button"""
        port = self.comboBox_port.currentText()
        bitrate = self.comboBox_bitrate.currentText()
        channel = self.lineEdit_channel.text()
        
        if port == "UARTCAN":
            self.log_message(f"Connecting UARTCAN: {channel} @ {self.uartcan_baud}")
        else:
            self.log_message(f"Connecting: {port} {channel} @ {bitrate}")
        
        self.connected = True
        self.pushButton_open.setEnabled(False)
        self.pushButton_close.setEnabled(True)
        self.log_message("Connected")
    
    def on_close(self):
        """Close button"""
        self.connected = False
        self.pushButton_open.setEnabled(True)
        self.pushButton_close.setEnabled(False)
        self.log_message("Disconnected")

    def on_send(self):
        """Send button - Send ID and Data (Optimized: auto format + hex validation)"""
        can_id = self.lineEdit_id.text().strip()
        can_data = self.lineEdit_data.text().strip()

        # Validate ID: must be a valid hex number (supports 0x prefix)
        id_clean = can_id.lower().replace("0x", "")
        if not all(c in "0123456789abcdefABCDEF" for c in id_clean):
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "CAN ID must be a valid number!")
            return

        # Validate Data & auto format into 2-digit groups (HEX SUPPORTED)
        formatted_data = ""
        if can_data:
            # Remove all spaces
            data_clean = can_data.replace(" ", "")
            # Validate HEX: 0-9, a-f, A-F only
            if not all(c in "0123456789abcdefABCDEF" for c in data_clean):
                QtWidgets.QMessageBox.warning(self, "Invalid Input", "Data must be a valid number!")
                return

            # Auto format: split into 2-digit groups with space
            formatted_data = " ".join([data_clean[i:i + 2] for i in range(0, len(data_clean), 2)])

        # Send log
        if can_id:
            if formatted_data:
                self.log_message(f"TX: {can_id} {formatted_data}")
            else:
                self.log_message(f"TX: ID={can_id}")
            # Clear inputs
            self.lineEdit_id.clear()
            self.lineEdit_data.clear()
    
    def on_clear(self):
        """Clear button - Clear ID and Data"""
        self.lineEdit_id.clear()
        self.lineEdit_data.clear()
    
    def on_fault_reset(self):
        """Fault Reset button - Reset fault via CANopen controlword 0x6040
        According to CiA 402 state machine, Fault Reset sets bit 7 (0x80) of controlword
        """
        # Default Node ID is 1, so COB-ID is 0x6040 + 1 = 0x601
        # Controlword for Fault Reset: 0x80 (bit 7 set)
        # SDO command: 0x2B 0x40 0x60 0x00 0x80 0x00 0x00 0x00
        #   - 0x2B: SDO download, 4 bytes data
        #   - 0x6040: Controlword object index (low byte first)
        #   - 0x80: Fault Reset controlword value
        fault_reset_id = "0x601"
        fault_reset_data = "2B 40 60 00 80 00 00 00"
        
        self.log_message(f"TX: {fault_reset_id} {fault_reset_data} (Fault Reset)")
        self.log_message("SYS: Fault Reset command sent")
    
    def on_op_mode_changed(self, mode):
        """Handle Operation Mode combo box change"""
        if mode == "Velocity":
            # Velocity mode: hide Target Pos and Max Vel, show Target Vel
            self.lineEdit_target_pos.setText("-")
            self.lineEdit_target_pos.setEnabled(False)
            self.lineEdit_max_vel.setText("-")
            self.lineEdit_max_vel.setEnabled(False)
            self.lineEdit_target_vel.setEnabled(True)
            if self.lineEdit_target_vel.text() == "-" or not self.lineEdit_target_vel.text():
                self.lineEdit_target_vel.setText("")
        elif mode == "Position":
            # Position mode: show Target Pos and Max Vel, hide Target Vel
            self.lineEdit_target_pos.setEnabled(True)
            if self.lineEdit_target_pos.text() == "-":
                self.lineEdit_target_pos.setText("")
            self.lineEdit_max_vel.setEnabled(True)
            if self.lineEdit_max_vel.text() == "-":
                self.lineEdit_max_vel.setText("1000")
            self.lineEdit_target_vel.setText("-")
            self.lineEdit_target_vel.setEnabled(False)
    
    # ========== Velocity & Position Mode Functions ==========
    def on_mode_start(self):
        """Start Velocity or Position Mode"""
        mode = self.comboBox_op_mode.currentText()
        node_id = 1
        sdo_id = f"0x{600 + node_id:02X}"
        
        if mode == "Position":
            # Set Position Mode: 6060h = 1
            self.log_message(f"TX: {sdo_id} 2F 60 60 00 01 00 00 00 (Set Mode=Position)")
            
            # Set Target Position: 607Ah
            target_pos = self.lineEdit_target_pos.text() or "0"
            pos_val = int(target_pos)
            pos_bytes = pos_val.to_bytes(4, 'little', signed=True).hex().upper()
            self.log_message(f"TX: {sdo_id} 23 7A 60 00 {pos_bytes} (Target Pos={target_pos})")
            
            # Set Profile Velocity: 6081h
            max_vel = self.lineEdit_max_vel.text() or "1000"
            vel_bytes = int(max_vel).to_bytes(4, 'little').hex().upper()
            self.log_message(f"TX: {sdo_id} 23 81 60 00 {vel_bytes} (Max Vel={max_vel})")
            
            # Set Profile Accel: 6083h
            accel = self.lineEdit_accel.text() or "1000"
            accel_bytes = int(accel).to_bytes(4, 'little').hex().upper()
            self.log_message(f"TX: {sdo_id} 23 83 60 00 {accel_bytes} (Accel={accel})")
            
            # Set Profile Decel: 6084h
            decel = self.lineEdit_decel.text() or "1000"
            decel_bytes = int(decel).to_bytes(4, 'little').hex().upper()
            self.log_message(f"TX: {sdo_id} 23 84 60 00 {decel_bytes} (Decel={decel})")
            
            # Start: Controlword = 0x0F (enable operation)
            self.log_message(f"TX: {sdo_id} 2B 40 60 00 0F 00 00 00 (Start Position)")
            self.log_message("SYS: Position Mode Started")
            
        elif mode == "Velocity":
            # Set Velocity Mode: 6060h = 3
            self.log_message(f"TX: {sdo_id} 2F 60 60 00 03 00 00 00 (Set Mode=Velocity)")
            
            # Set Target Velocity: 60FFh
            target_vel = self.lineEdit_target_vel.text() or "0"
            vel_val = int(target_vel)
            vel_bytes = vel_val.to_bytes(4, 'little', signed=True).hex().upper()
            self.log_message(f"TX: {sdo_id} 23 FF 60 00 {vel_bytes} (Target Vel={target_vel})")
            
            # Set Profile Accel: 6083h
            accel = self.lineEdit_accel.text() or "1000"
            accel_bytes = int(accel).to_bytes(4, 'little').hex().upper()
            self.log_message(f"TX: {sdo_id} 23 83 60 00 {accel_bytes} (Accel={accel})")
            
            # Set Profile Decel: 6084h
            decel = self.lineEdit_decel.text() or "1000"
            decel_bytes = int(decel).to_bytes(4, 'little').hex().upper()
            self.log_message(f"TX: {sdo_id} 23 84 60 00 {decel_bytes} (Decel={decel})")
            
            # Start: Controlword = 0x0F
            self.log_message(f"TX: {sdo_id} 2B 40 60 00 0F 00 00 00 (Start Velocity)")
            self.log_message("SYS: Velocity Mode Started")
    
    def on_move_absolute(self):
        """Move Absolute - Position Mode with Controlword 0x0F -> 0x1F"""
        node_id = 1
        sdo_id = f"0x{600 + node_id:02X}"
        
        # Set Position Mode: 6060h = 1
        self.log_message(f"TX: {sdo_id} 2F 60 60 00 01 00 00 00 (Set Mode=Position)")
        
        # Set Target Position: 607Ah
        target_pos = self.lineEdit_target_pos.text() or "0"
        pos_val = int(target_pos)
        pos_bytes = pos_val.to_bytes(4, 'little', signed=True).hex().upper()
        self.log_message(f"TX: {sdo_id} 23 7A 60 00 {pos_bytes} (Target Pos={target_pos})")
        
        # Set Profile Velocity: 6081h
        max_vel = self.lineEdit_max_vel.text() or "1000"
        vel_bytes = int(max_vel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 81 60 00 {vel_bytes} (Max Vel={max_vel})")
        
        # Set Profile Accel: 6083h
        accel = self.lineEdit_accel.text() or "1000"
        accel_bytes = int(accel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 83 60 00 {accel_bytes} (Accel={accel})")
        
        # Set Profile Decel: 6084h
        decel = self.lineEdit_decel.text() or "1000"
        decel_bytes = int(decel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 84 60 00 {decel_bytes} (Decel={decel})")
        
        # Enable Operation: Controlword = 0x0F
        self.log_message(f"TX: {sdo_id} 2B 40 60 00 0F 00 00 00 (Enable Operation)")
        
        # Move Absolute: Controlword = 0x1F (bit 4 = new setpoint, bit 6 = absolute)
        self.log_message(f"TX: {sdo_id} 2B 40 60 00 1F 00 00 00 (Move Absolute)")
        self.log_message("SYS: Move Absolute command sent")
    
    def on_move_relative(self):
        """Move Relative - Position Mode with Controlword 0x4F -> 0x5F"""
        node_id = 1
        sdo_id = f"0x{600 + node_id:02X}"
        
        # Set Position Mode: 6060h = 1
        self.log_message(f"TX: {sdo_id} 2F 60 60 00 01 00 00 00 (Set Mode=Position)")
        
        # Set Target Position: 607Ah (relative distance)
        target_pos = self.lineEdit_target_pos.text() or "0"
        pos_val = int(target_pos)
        pos_bytes = pos_val.to_bytes(4, 'little', signed=True).hex().upper()
        self.log_message(f"TX: {sdo_id} 23 7A 60 00 {pos_bytes} (Rel Distance={target_pos})")
        
        # Set Profile Velocity: 6081h
        max_vel = self.lineEdit_max_vel.text() or "1000"
        vel_bytes = int(max_vel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 81 60 00 {vel_bytes} (Max Vel={max_vel})")
        
        # Set Profile Accel: 6083h
        accel = self.lineEdit_accel.text() or "1000"
        accel_bytes = int(accel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 83 60 00 {accel_bytes} (Accel={accel})")
        
        # Set Profile Decel: 6084h
        decel = self.lineEdit_decel.text() or "1000"
        decel_bytes = int(decel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 84 60 00 {decel_bytes} (Decel={decel})")
        
        # Enable Operation + Relative: Controlword = 0x4F
        self.log_message(f"TX: {sdo_id} 2B 40 60 00 4F 00 00 00 (Enable + Relative)")
        
        # Move Relative: Controlword = 0x5F (bit 4 = new setpoint, bit 5 = immediate, bit 6 = relative)
        self.log_message(f"TX: {sdo_id} 2B 40 60 00 5F 00 00 00 (Move Relative)")
        self.log_message("SYS: Move Relative command sent")
    
    def on_mode_stop(self):
        """Stop Velocity or Position Mode - Halt (bit 8 = 1)"""
        node_id = 1
        sdo_id = f"0x{600 + node_id:02X}"
        # Controlword = 0x10F (bit 8 halt = 1)
        self.log_message(f"TX: {sdo_id} 2B 40 60 00 0F 01 00 00 (Stop/Halt)")
        self.log_message("SYS: Motion Stopped")
    
    # ========== Homing Mode Functions ==========
    def on_homing_start(self):
        """Start Homing Mode"""
        node_id = 1
        sdo_id = f"0x{600 + node_id:02X}"
        
        # Set Homing Mode: 6060h = 6
        self.log_message(f"TX: {sdo_id} 2F 60 60 00 06 00 00 00 (Set Mode=Homing)")
        
        # Get homing method from combo box
        method_text = self.comboBox_homing_method.currentText()
        method_code = method_text.split(":")[0].strip()
        
        # Set Homing Method: 6098h
        method_bytes = int(method_code).to_bytes(1, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 2F 98 60 00 {method_bytes} (Method={method_text})")
        
        # Set Homing Velocity: 6099h subindex 01
        homing_vel = self.lineEdit_homing_vel.text() or "100"
        vel_bytes = int(homing_vel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 99 60 01 {vel_bytes} (Homing Vel={homing_vel})")
        
        # Set Homing Search Velocity: 6099h subindex 02
        search_vel = self.lineEdit_homing_search.text() or "20"
        search_bytes = int(search_vel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 99 60 02 {search_bytes} (Search Vel={search_vel})")
        
        # Set Homing Acceleration: 609Ah
        homing_accel = self.lineEdit_homing_accel.text() or "500"
        accel_bytes = int(homing_accel).to_bytes(4, 'little').hex().upper()
        self.log_message(f"TX: {sdo_id} 23 9A 60 00 {accel_bytes} (Homing Accel={homing_accel})")
        
        # Start Homing: Controlword = 0x1F (bit 4 = 1 for homing start)
        self.log_message(f"TX: {sdo_id} 2B 40 60 00 1F 00 00 00 (Homing Start)")
        self.log_message("SYS: Homing Started")
    
    def on_homing_stop(self):
        """Stop Homing Mode"""
        node_id = 1
        sdo_id = f"0x{600 + node_id:02X}"
        # Controlword = 0x0F (clear bit 4 to stop homing)
        self.log_message(f"TX: {sdo_id} 2B 40 60 00 0F 00 00 00 (Homing Stop)")
        self.log_message("SYS: Homing Stopped")
    
    def on_clear_logs(self):
        """Clear Logs button"""
        self.textEdit_log.clear()
    
    def on_save_logs(self):
        """Save Logs button"""
        filename, _ = QFileDialog.getSaveFileName(self, "Save Log", "canopen_log.txt", "Text Files (*.txt)")
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.textEdit_log.toPlainText())
                self.log_message(f"Saved: {filename}")
            except Exception as e:
                self.log_message(f"Save failed: {e}")
    
    def on_can_message(self, message):
        self.log_message(f"RX: {message}")
    
    def on_connection_status(self, status, message):
        self.log_message(f"SYS: {message}")
    
    def read_can_messages(self):
        pass
    
    def log_message(self, message):
        """Log message"""
        try:
            ts = datetime.now().strftime("%H:%M:%S")
            self.textEdit_log.append(f"[{ts}] {message}")
            scrollbar = self.textEdit_log.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        except:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)
    
    font = QtGui.QFont("Microsoft YaHei UI", 9)
    app.setFont(font)
    app.setWindowIcon(QtGui.QIcon("./logo.ico"))
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())