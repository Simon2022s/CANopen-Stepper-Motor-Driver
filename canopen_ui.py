# -*- coding: utf-8 -*-
"""
CANopen UI - Fixed Version
UI proportions match background image (800x667), top bar evenly distributed
"""

from PyQt5 import QtCore, QtGui, QtWidgets


QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)


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
        MainWindow.setFixedSize(800, 860)

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

        # Open/Close toggle button: 80
        x += 90 + spacing
        self.pushButton_open = CANopenButton("Open", self.centralwidget)
        self.pushButton_open.setGeometry(QtCore.QRect(x, y, 80, 26))
        
        # Disable/Enable toggle button (was Close button)
        x += 73 + spacing
        self.pushButton_disable = CANopenButton("Disable", self.centralwidget)
        self.pushButton_disable.setGeometry(QtCore.QRect(x, y, 80, 26))

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
        self.pushButton_send.setGeometry(QtCore.QRect(x, y, 80, 26))

        x += 80 + 22
        self.pushButton_clear = CANopenButton("Clear", self.centralwidget)
        self.pushButton_clear.setGeometry(QtCore.QRect(x, y, 80, 26))

        x += 82 + 21
        self.pushButton_fault_reset = CANopenButton("Fault Reset", self.centralwidget)
        self.pushButton_fault_reset.setGeometry(QtCore.QRect(x, y, 90, 26))

        # Define right_x for right column layout
        right_x = 480

        # ========== Basic Parameters Area ==========
        y = 155
        x = 480

        self.label_basic_params = QtWidgets.QLabel("Basic Parameters", self.centralwidget)
        self.label_basic_params.setGeometry(QtCore.QRect(x, y, 180, 20))
        self.label_basic_params.setStyleSheet("color: #ffffff;  background: transparent;")
        self.label_basic_params.setText("<font size='4'>Homing Mode</font>")



        # Row 1: Node ID
        y += 28
        self.label_node_id = QtWidgets.QLabel("Node ID:", self.centralwidget)
        self.label_node_id.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_node_id.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_node_id = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_node_id.setGeometry(QtCore.QRect(x, y, 190, 24))
        self.lineEdit_node_id.setPlaceholderText("1")
        self.lineEdit_node_id.setText("1")
        self.lineEdit_node_id.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)

        # Row 2: Current
        y += 32
        x = right_x
        self.label_current = QtWidgets.QLabel("Current:", self.centralwidget)
        self.label_current.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_current.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_current = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_current.setGeometry(QtCore.QRect(x, y, 190, 24))
        self.lineEdit_current.setPlaceholderText("10")
        self.lineEdit_current.setText("10")
        self.lineEdit_current.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)

        # Row 3: Microstep
        y += 32
        x = right_x
        self.label_microstep = QtWidgets.QLabel("Microstep:", self.centralwidget)
        self.label_microstep.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_microstep.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_microstep = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_microstep.setGeometry(QtCore.QRect(x, y, 190, 24))
        self.lineEdit_microstep.setPlaceholderText("13")
        self.lineEdit_microstep.setText("13")
        self.lineEdit_microstep.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)

        # Row 4: CAN Bit Rate
        y += 32
        x = right_x
        self.label_basic_bitrate = QtWidgets.QLabel("CAN Bit Rate:", self.centralwidget)
        self.label_basic_bitrate.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_basic_bitrate.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_basic_bitrate = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_basic_bitrate.setGeometry(QtCore.QRect(x, y, 190, 24))
        self.lineEdit_basic_bitrate.setPlaceholderText("2")
        self.lineEdit_basic_bitrate.setText("2")
        self.lineEdit_basic_bitrate.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 180);
                color: #000000;
                border: 1px solid #999999;
                border-radius: 4px;
                padding: 2px;
            }
        """)

        # Row 5: Query and Set buttons
        y += 38
        x = right_x
        self.pushButton_query = CANopenButton("One-Click-Query", self.centralwidget)
        self.pushButton_query.setGeometry(QtCore.QRect(x, y, 127, 28))

        x += 169
        self.pushButton_set = CANopenButton("One-Click-Set", self.centralwidget)
        self.pushButton_set.setGeometry(QtCore.QRect(x, y, 127, 28))

        # ========== Velocity & Position Mode Area ==========
        y = 371
        x = 480

        self.label_mode = QtWidgets.QLabel("Velocity & Position Mode", self.centralwidget)
        self.label_mode.setGeometry(QtCore.QRect(x, y, 180, 20))
        self.label_mode.setStyleSheet("color: #ffffff; background: transparent;")
        self.label_mode.setText("<font size='4'>Velocity & Position Mode</font>")

        # Mode selection
        y += 25
        x = 480
        self.label_op_mode = QtWidgets.QLabel("Working Mode:", self.centralwidget)
        self.label_op_mode.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_op_mode.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.comboBox_op_mode = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_op_mode.setGeometry(QtCore.QRect(x, y, 190, 24))
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
        x = 480
        self.label_target_pos = QtWidgets.QLabel("Set Pos. pulses:", self.centralwidget)
        self.label_target_pos.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_target_pos.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_target_pos = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_target_pos.setGeometry(QtCore.QRect(x, y, 190, 24))
        self.lineEdit_target_pos.setPlaceholderText("10000")
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
        x = 480
        self.label_target_vel = QtWidgets.QLabel("Set Vel. Speed:", self.centralwidget)
        self.label_target_vel.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_target_vel.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_target_vel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_target_vel.setGeometry(QtCore.QRect(x, y, 190, 24))
        self.lineEdit_target_vel.setPlaceholderText("50")
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
        x = 480
        self.label_max_vel = QtWidgets.QLabel("Set Pos. Speed:", self.centralwidget)
        self.label_max_vel.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_max_vel.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_max_vel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_max_vel.setGeometry(QtCore.QRect(x, y, 190, 24))
        self.lineEdit_max_vel.setPlaceholderText("500")
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
        x = 480
        self.label_accel = QtWidgets.QLabel("Acceleration:", self.centralwidget)
        self.label_accel.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_accel.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_accel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_accel.setGeometry(QtCore.QRect(x, y, 190, 24))
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
        x = 480
        self.label_decel = QtWidgets.QLabel("Deceleration:", self.centralwidget)
        self.label_decel.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_decel.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_decel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_decel.setGeometry(QtCore.QRect(x, y, 190, 24))
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
        x = 480
        self.pushButton_start = CANopenButton("Start", self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(x, y, 55, 28))

        x += 60
        self.pushButton_move_abs = CANopenButton("Move Abs", self.centralwidget)
        self.pushButton_move_abs.setGeometry(QtCore.QRect(x, y, 84, 28))

        x += 89
        self.pushButton_move_rel = CANopenButton("Move Rel", self.centralwidget)
        self.pushButton_move_rel.setGeometry(QtCore.QRect(x, y, 82, 28))

        x += 87
        self.pushButton_stop = CANopenButton("Stop", self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(x, y, 60, 28))

        # ========== Homing Mode Area (Vertical Layout) ==========
        y += 50
        x = 480

        self.label_homing = QtWidgets.QLabel("Homing Mode:", self.centralwidget)
        self.label_homing.setGeometry(QtCore.QRect(x, y, 120, 20))
        self.label_homing.setStyleSheet("color: #ffffff; font size: 16x; background: transparent;")
        self.label_homing.setText("<font size='4'>Homing Mode</font>")
        # Row 1: Homing Method
        y += 28
        self.label_homing_method = QtWidgets.QLabel("HM. Method:", self.centralwidget)
        self.label_homing_method.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_homing_method.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.comboBox_homing_method = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_homing_method.setGeometry(QtCore.QRect(x, y, 190, 24))
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
        x = 480
        self.label_homing_vel = QtWidgets.QLabel("HM. Speed:", self.centralwidget)
        self.label_homing_vel.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_homing_vel.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_homing_vel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_homing_vel.setGeometry(QtCore.QRect(x, y, 190, 24))
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
        x = 480
        self.label_homing_search = QtWidgets.QLabel("HM. Probing:", self.centralwidget)
        self.label_homing_search.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_homing_search.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_homing_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_homing_search.setGeometry(QtCore.QRect(x, y, 190, 24))
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
        x = 480
        self.label_homing_accel = QtWidgets.QLabel("Acceleration:", self.centralwidget)
        self.label_homing_accel.setGeometry(QtCore.QRect(x, y, 95, 24))
        self.label_homing_accel.setStyleSheet("color: #ffffff; background: transparent;")

        x += 105
        self.lineEdit_homing_accel = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_homing_accel.setGeometry(QtCore.QRect(x, y, 190, 24))
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
        x = 480
        self.pushButton_homing_start = CANopenButton("Homing Start", self.centralwidget)
        self.pushButton_homing_start.setGeometry(QtCore.QRect(x, y, 120, 28))

        x += 175
        self.pushButton_homing_stop = CANopenButton("Homing Stop", self.centralwidget)
        self.pushButton_homing_stop.setGeometry(QtCore.QRect(x, y, 120, 28))

        # ========== TWO COLUMN LAYOUT ==========
        # Left column: Communication Logs
        # Right column: Velocity/Position/Homing Mode

        column_start_y = 125
        left_x = margin  # x = 20
        # right_x already defined above (560)
        column_width = 440
        column_height = 700  # Both columns same height

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
        y += column_height - 50
        self.pushButton_clear_logs = CANopenButton("Clear Logs", self.centralwidget)
        self.pushButton_clear_logs.setGeometry(QtCore.QRect(left_x, y, 180, 28))

        x = left_x + 100 + 160
        self.pushButton_save_logs = CANopenButton("Save Logs", self.centralwidget)
        self.pushButton_save_logs.setGeometry(QtCore.QRect(x, y, 180, 28))

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

    # 再次确保DPI适配生效
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    # 设置全局字体，和代码2一致
    font = QtGui.QFont("Microsoft YaHei UI", 9)
    app.setFont(font)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    app.setWindowIcon(QtGui.QIcon("./logo.ico"))
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())