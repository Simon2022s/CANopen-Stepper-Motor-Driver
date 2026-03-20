# -*- coding: utf-8 -*-
"""
CANopen UI - Fixed Version
UI proportions match background image (800x667), top bar evenly distributed
"""

from PyQt5 import QtCore, QtGui, QtWidgets

class CANopenButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(26)
        self.setFont(QtGui.QFont("Microsoft YaHei UI", 9))
        self.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 161, 203, 220),
                    stop:1 rgba(0, 131, 173, 220));
                color: white;
                border: 2px solid #00a1cb;
                border-radius: 4px;
                padding: 2px 12px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 181, 223, 230),
                    stop:1 rgba(0, 151, 193, 230));
                border: 2px solid #4cd964;
            }
            QPushButton:pressed {
                background-color: rgba(0, 111, 153, 240);
            }
        """)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 900)
        
        # Create central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Set background image - tiled display, starting from top
        try:
            import os
            bg_path = os.path.join(os.path.dirname(__file__), "bruce_bg.jpg")
            if os.path.exists(bg_path):
                self.centralwidget.setStyleSheet(f"""
                    QWidget#centralwidget {{
                        background-image: url({bg_path.replace(chr(92), '/')});
                        background-repeat: repeat-x;
                        background-position: top left;
                        background-attachment: fixed;
                    }}
                """)
        except Exception as e:
            print(f"Background error: {e}")
        
        # ========== Row 1: Port / Channel / Bit Rate / Open / Close ==========
        # Evenly distributed: total width 800, left/right margins 20 each, available 760
        # Port(40+90) + Channel(70+110) + BitRate(90+90) + Open(80) + Close(80) = 650
        # Spacing = (760-650)/4 = 27.5, rounded to 28
        
        y = 20
        margin = 20
        spacing = 28
        x = margin
        
        # Port: label 40 + dropdown 90 = 130
        self.label_port = QtWidgets.QLabel("Port:", self.centralwidget)
        self.label_port.setGeometry(QtCore.QRect(x, y, 40, 26))
        self.label_port.setStyleSheet("color: #000000; font-weight: bold; background: transparent;")
        
        x += 40
        self.comboBox_port = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_port.setGeometry(QtCore.QRect(x, y, 90, 26))
        self.comboBox_port.addItems(["PCAN", "UARTCAN", "socketCAN"])
        self.comboBox_port.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(255, 255, 255, 220);
                color: #000000;
                selection-background-color: #00a1cb;
            }
        """)
        
        # Channel: label 70 + text box 110 = 180
        x += 90 + spacing
        self.label_channel = QtWidgets.QLabel("Channel:", self.centralwidget)
        self.label_channel.setGeometry(QtCore.QRect(x, y, 70, 26))
        self.label_channel.setStyleSheet("color: #000000; font-weight: bold; background: transparent;")
        
        x += 70
        self.lineEdit_channel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_channel.setGeometry(QtCore.QRect(x, y, 110, 26))
        self.lineEdit_channel.setPlaceholderText("...")
        self.lineEdit_channel.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Bit Rate: label 90 + dropdown 90 = 180
        x += 110 + spacing
        self.label_bitrate = QtWidgets.QLabel("CAN Bit Rate:", self.centralwidget)
        self.label_bitrate.setGeometry(QtCore.QRect(x, y, 90, 26))
        self.label_bitrate.setStyleSheet("color: #000000; font-weight: bold; background: transparent;")
        
        x += 90
        self.comboBox_bitrate = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_bitrate.setGeometry(QtCore.QRect(x, y, 90, 26))
        self.comboBox_bitrate.addItems(["125K", "250K", "500K", "800K", "1M"])
        self.comboBox_bitrate.setCurrentText("500K")
        self.comboBox_bitrate.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(255, 255, 255, 220);
                color: #000000;
                selection-background-color: #00a1cb;
            }
        """)
        
        # Open button: 80
        x += 90 + spacing
        self.pushButton_open = CANopenButton("Open", self.centralwidget)
        self.pushButton_open.setGeometry(QtCore.QRect(x, y, 80, 26))
        
        # Close button: 80
        x += 80 + spacing
        self.pushButton_close = CANopenButton("Close", self.centralwidget)
        self.pushButton_close.setGeometry(QtCore.QRect(x, y, 80, 26))
        self.pushButton_close.setEnabled(False)
        
        # ========== Row 2: Manual CAN Command (ID + Data) ==========
        y = 60
        x = margin
        
        self.label_manual = QtWidgets.QLabel("Manual CAN Command:", self.centralwidget)
        self.label_manual.setGeometry(QtCore.QRect(x, y, 150, 20))
        self.label_manual.setStyleSheet("color: #000000; background: transparent;")
        
        y = 85
        x = margin
        
        # ID label and text box
        self.label_id = QtWidgets.QLabel("ID:", self.centralwidget)
        self.label_id.setGeometry(QtCore.QRect(x, y, 25, 26))
        self.label_id.setStyleSheet("color: #000000; font-weight: bold; background: transparent;")
        
        x += 30
        self.lineEdit_id = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_id.setGeometry(QtCore.QRect(x, y, 100, 26))
        self.lineEdit_id.setPlaceholderText("601")
        self.lineEdit_id.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Data label and text box
        x += 100 + 15
        self.label_data = QtWidgets.QLabel("Data:", self.centralwidget)
        self.label_data.setGeometry(QtCore.QRect(x, y, 40, 26))
        self.label_data.setStyleSheet("color: #000000; font-weight: bold; background: transparent;")
        
        x += 45
        self.lineEdit_data = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_data.setGeometry(QtCore.QRect(x, y, 250, 26))
        self.lineEdit_data.setPlaceholderText("2B 40 60 00 00 00 00 00")
        self.lineEdit_data.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Send, Clear and Fault Reset buttons
        x += 250 + 20
        self.pushButton_send = CANopenButton("Send", self.centralwidget)
        self.pushButton_send.setGeometry(QtCore.QRect(x, y, 70, 26))
        
        x += 70 + 10
        self.pushButton_clear = CANopenButton("Clear", self.centralwidget)
        self.pushButton_clear.setGeometry(QtCore.QRect(x, y, 60, 26))
        
        x += 60 + 10
        self.pushButton_fault_reset = CANopenButton("Fault Reset", self.centralwidget)
        self.pushButton_fault_reset.setGeometry(QtCore.QRect(x, y, 90, 26))
        self.pushButton_fault_reset.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 100, 100, 220),
                    stop:1 rgba(220, 80, 80, 220));
                color: white;
                border: 2px solid #ff4444;
                border-radius: 4px;
                padding: 2px 8px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 120, 120, 230),
                    stop:1 rgba(240, 100, 100, 230));
                border: 2px solid #ff6666;
            }
            QPushButton:pressed {
                background-color: rgba(200, 60, 60, 240);
            }
        """)
        
        # ========== Velocity & Position Mode Area ==========
        y = 125
        x = 340
        
        self.label_mode = QtWidgets.QLabel("Velocity & Position Mode:", self.centralwidget)
        self.label_mode.setGeometry(QtCore.QRect(x, y, 180, 20))
        self.label_mode.setStyleSheet("color: #000000; font-weight: bold; background: transparent;")
        
        # Mode selection
        y += 25
        self.label_op_mode = QtWidgets.QLabel("Work Mode:", self.centralwidget)
        self.label_op_mode.setGeometry(QtCore.QRect(x, y, 45, 24))
        self.label_op_mode.setStyleSheet("color: #000000; background: transparent;")
        
        x += 50
        self.comboBox_op_mode = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_op_mode.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.comboBox_op_mode.addItems(["Position", "Velocity"])
        self.comboBox_op_mode.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView {
                background-color: rgba(255, 255, 255, 220);
                color: #000000;
                selection-background-color: #00a1cb;
            }
        """)
        
        # Row 1: Target Pos
        y += 32
        x = 340
        self.label_target_pos = QtWidgets.QLabel("Target Pos:", self.centralwidget)
        self.label_target_pos.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_target_pos.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.lineEdit_target_pos = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_target_pos.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.lineEdit_target_pos.setPlaceholderText("0")
        self.lineEdit_target_pos.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Row 2: Target Vel
        y += 32
        x = 340
        self.label_target_vel = QtWidgets.QLabel("Target Vel:", self.centralwidget)
        self.label_target_vel.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_target_vel.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.lineEdit_target_vel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_target_vel.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.lineEdit_target_vel.setPlaceholderText("0")
        self.lineEdit_target_vel.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Row 3: Max Vel
        y += 32
        x = 340
        self.label_max_vel = QtWidgets.QLabel("Max Vel:", self.centralwidget)
        self.label_max_vel.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_max_vel.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.lineEdit_max_vel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_max_vel.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.lineEdit_max_vel.setPlaceholderText("1000")
        self.lineEdit_max_vel.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Row 4: Accel
        y += 32
        x = 340
        self.label_accel = QtWidgets.QLabel("Accel:", self.centralwidget)
        self.label_accel.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_accel.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.lineEdit_accel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_accel.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.lineEdit_accel.setPlaceholderText("1000")
        self.lineEdit_accel.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Row 5: Decel
        y += 32
        x = 340
        self.label_decel = QtWidgets.QLabel("Decel:", self.centralwidget)
        self.label_decel.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_decel.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.lineEdit_decel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_decel.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.lineEdit_decel.setPlaceholderText("1000")
        self.lineEdit_decel.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Start/Move Abs/Move Rel/Stop buttons
        y += 35
        x = 340
        self.pushButton_start = CANopenButton("Start", self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(x, y, 65, 28))
        
        x += 72
        self.pushButton_move_abs = CANopenButton("Move Abs", self.centralwidget)
        self.pushButton_move_abs.setGeometry(QtCore.QRect(x, y, 75, 28))
        self.pushButton_move_abs.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(100, 200, 100, 220),
                    stop:1 rgba(80, 180, 80, 220));
                color: white;
                border: 2px solid #4cd964;
                border-radius: 4px;
                padding: 2px 8px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(120, 220, 120, 230),
                    stop:1 rgba(100, 200, 100, 230));
            }
        """)
        
        x += 82
        self.pushButton_move_rel = CANopenButton("Move Rel", self.centralwidget)
        self.pushButton_move_rel.setGeometry(QtCore.QRect(x, y, 75, 28))
        self.pushButton_move_rel.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(150, 100, 200, 220),
                    stop:1 rgba(130, 80, 180, 220));
                color: white;
                border: 2px solid #9b59b6;
                border-radius: 4px;
                padding: 2px 8px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(170, 120, 220, 230),
                    stop:1 rgba(150, 100, 200, 230));
            }
        """)
        
        x += 82
        self.pushButton_stop = CANopenButton("Stop", self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(x, y, 60, 28))
        self.pushButton_stop.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 150, 50, 220),
                    stop:1 rgba(220, 120, 30, 220));
                color: white;
                border: 2px solid #ff9933;
                border-radius: 4px;
                padding: 2px 12px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 170, 70, 230),
                    stop:1 rgba(240, 140, 50, 230));
            }
        """)
        
        # ========== Homing Mode Area (Vertical Layout) ==========
        y += 50
        x = 340
        
        self.label_homing = QtWidgets.QLabel("Homing Mode:", self.centralwidget)
        self.label_homing.setGeometry(QtCore.QRect(x, y, 120, 20))
        self.label_homing.setStyleSheet("color: #000000; font-weight: bold; background: transparent;")
        
        # Row 1: Homing Method
        y += 28
        self.label_homing_method = QtWidgets.QLabel("Method:", self.centralwidget)
        self.label_homing_method.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_homing_method.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.comboBox_homing_method = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_homing_method.setGeometry(QtCore.QRect(x, y, 160, 24))
        self.comboBox_homing_method.addItems([
            "17: Neg Limit", "18: Pos Limit", "24: Pos Home", 
            "29: Neg Home", "41: Neg Stop", "42: Pos Stop"
        ])
        self.comboBox_homing_method.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
            QComboBox::drop-down { border: none; width: 20px; }
            QComboBox QAbstractItemView {
                background-color: rgba(255, 255, 255, 220);
                color: #000000;
                selection-background-color: #00a1cb;
            }
        """)
        
        # Row 2: Speed
        y += 32
        x = 340
        self.label_homing_vel = QtWidgets.QLabel("Speed:", self.centralwidget)
        self.label_homing_vel.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_homing_vel.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.lineEdit_homing_vel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_homing_vel.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.lineEdit_homing_vel.setPlaceholderText("100")
        self.lineEdit_homing_vel.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Row 3: Search
        y += 32
        x = 340
        self.label_homing_search = QtWidgets.QLabel("Search:", self.centralwidget)
        self.label_homing_search.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_homing_search.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.lineEdit_homing_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_homing_search.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.lineEdit_homing_search.setPlaceholderText("20")
        self.lineEdit_homing_search.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Row 4: Accel
        y += 32
        x = 340
        self.label_homing_accel = QtWidgets.QLabel("Accel:", self.centralwidget)
        self.label_homing_accel.setGeometry(QtCore.QRect(x, y, 80, 24))
        self.label_homing_accel.setStyleSheet("color: #000000; background: transparent;")
        
        x += 85
        self.lineEdit_homing_accel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_homing_accel.setGeometry(QtCore.QRect(x, y, 120, 24))
        self.lineEdit_homing_accel.setPlaceholderText("500")
        self.lineEdit_homing_accel.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)
        
        # Row 5: Homing Start/Stop buttons
        y += 35
        x = 340
        self.pushButton_homing_start = CANopenButton("Homing Start", self.centralwidget)
        self.pushButton_homing_start.setGeometry(QtCore.QRect(x, y, 100, 28))
        
        x += 110
        self.pushButton_homing_stop = CANopenButton("Homing Stop", self.centralwidget)
        self.pushButton_homing_stop.setGeometry(QtCore.QRect(x, y, 100, 28))
        self.pushButton_homing_stop.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 150, 50, 220),
                    stop:1 rgba(220, 120, 30, 220));
                color: white;
                border: 2px solid #ff9933;
                border-radius: 4px;
                padding: 2px 12px;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 170, 70, 230),
                    stop:1 rgba(240, 140, 50, 230));
            }
        """)
        
        # ========== TWO COLUMN LAYOUT ==========
        # Left column: Communication Logs (x=20, width=300)
        # Right column: Velocity/Position/Homing Mode (x=340, width=440)
        
        column_start_y = 125
        left_x = margin  # x = 20
        right_x = 560  # Window 800, left margin 20, right margin 20 -> right_x = 800-20-220  # Symmetric: window 800, left margin 20, right column width 300, right margin 20
        column_width = 300
        column_height = 680  # Both columns same height
        
        # ========== LEFT COLUMN: Communication Logs ==========
        y = column_start_y
        
        self.label_logs = QtWidgets.QLabel("Communication Logs:", self.centralwidget)
        self.label_logs.setGeometry(QtCore.QRect(left_x, y, 150, 20))
        self.label_logs.setStyleSheet("color: #000000; background: transparent;")
        
        # Communication Logs text area
        y += 25
        self.textEdit_log = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_log.setGeometry(QtCore.QRect(left_x, y, column_width, column_height - 60))
        self.textEdit_log.setReadOnly(True)
        self.textEdit_log.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 200);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 4px;
            }
        """)
        
        # Bottom buttons (Clear Logs, Save Logs)
        y += column_height - 30
        self.pushButton_clear_logs = CANopenButton("Clear Logs", self.centralwidget)
        self.pushButton_clear_logs.setGeometry(QtCore.QRect(left_x, y, 100, 32))
        
        x = left_x + 100 + 10
        self.pushButton_save_logs = CANopenButton("Save Logs", self.centralwidget)
        self.pushButton_save_logs.setGeometry(QtCore.QRect(x, y, 100, 32))
        
        # Set central widget
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Menu bar, status bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("CANopen Stepper Motor Driver")


class UartcanDialog(QtWidgets.QDialog):
    """UARTCAN Settings Dialog - Only Save and Cancel buttons"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("UARTCAN Setting")
        self.setFixedSize(300, 120)
        self.setModal(True)
        
        self.label_baud = QtWidgets.QLabel("Baud Rate:", self)
        self.label_baud.setGeometry(QtCore.QRect(20, 20, 80, 25))
        
        self.comboBox_baud = QtWidgets.QComboBox(self)
        self.comboBox_baud.setGeometry(QtCore.QRect(110, 18, 150, 25))
        self.comboBox_baud.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.comboBox_baud.setCurrentText("115200")
        self.comboBox_baud.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 200);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(255, 255, 255, 220);
                color: #000000;
                selection-background-color: #00a1cb;
            }
        """)
        
        self.btn_save = CANopenButton("Save", self)
        self.btn_save.setGeometry(QtCore.QRect(60, 70, 70, 28))
        self.btn_save.clicked.connect(self.on_save)
        
        self.btn_cancel = CANopenButton("Cancel", self)
        self.btn_cancel.setGeometry(QtCore.QRect(160, 70, 70, 28))
        self.btn_cancel.clicked.connect(self.on_cancel)
        
        self.result = False
        self.baud_rate = "115200"
    
    def on_save(self):
        self.baud_rate = self.comboBox_baud.currentText()
        self.result = True
        self.accept()
    
    def on_cancel(self):
        self.result = False
        self.reject()
    
    def get_result(self):
        return self.result, self.baud_rate

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    app.setWindowIcon(QtGui.QIcon("./logo.ico"))
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

