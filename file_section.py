from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QCheckBox, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPalette, QFont
import os
import pandas as pd

class FileSection(QWidget):
    def __init__(self, title, date):
        super().__init__()
        self.title = title
        self.file_path = None
        self.file_name = None
        self.cutoff = pd.Timestamp(date)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Set overall widget style with dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e2130;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)

        # Section for drag/drop or file selection
        self.drop_label = QLabel(f"Drag and drop or select {self.title} file")
        self.drop_label.setStyleSheet("""
            border: 2px dashed #3498db; 
            padding: 20px; 
            text-align: center;
            background-color: #2a2f45; 
            border-radius: 10px;
            color: #3498db;
            font-size: 14px;
            font-weight: 500;
        """)
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.mousePressEvent = self.openFileDialog
        self.drop_label.setMinimumWidth(300)
        self.drop_label.setMaximumHeight(100)
        self.drop_label.setCursor(Qt.PointingHandCursor)

        # Add a subtle shadow effect to the drop label
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.drop_label.setGraphicsEffect(shadow)

        # Horizontal separator
        self.h_line = QFrame()
        self.h_line.setFrameShape(QFrame.HLine)
        self.h_line.setFrameShadow(QFrame.Sunken)
        self.h_line.setStyleSheet("background-color: #3a4161; margin: 10px 0;")

        layout.addWidget(self.drop_label)
        layout.addWidget(self.h_line)

        # Enable drag and drop
        self.setAcceptDrops(True)

        # Checkboxes container with gradient and proper styling
        self.checkbox_frame = QFrame()
        self.checkbox_frame.setVisible(False)
        self.checkbox_layout = QVBoxLayout(self.checkbox_frame)
        self.checkbox_layout.setContentsMargins(10, 10, 10, 10)
        self.checkbox_layout.setSpacing(5)
        
        # Restore gradient with proper QSS syntax
        self.checkbox_frame.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, 
                x2: 0, y2: 1, 
                stop: 0 #3A7BD5, 
                stop: 1 #2C82C9
            );
            border: 1px solid #1C6093;
            border-radius: 10px;
            padding: 10px;
        """)

        # Add shadow effect to checkbox frame
        checkbox_shadow = QGraphicsDropShadowEffect()
        checkbox_shadow.setBlurRadius(20)
        checkbox_shadow.setOffset(0, 3)
        checkbox_shadow.setColor(QColor(0, 0, 0, 80))
        self.checkbox_frame.setGraphicsEffect(checkbox_shadow)
        
        # Script Checkboxes with default styling
        self.scripts = self.get_scripts()
        self.checkboxes = {}
        for script_name in self.scripts:
            checkbox = QCheckBox(script_name)
            checkbox.setChecked(True)
            # Just set the text color to white for visibility
            checkbox.setStyleSheet("color: white;")
            self.checkboxes[script_name] = checkbox
            self.checkbox_layout.addWidget(checkbox)
        
        layout.addWidget(self.checkbox_frame)

        # Smooth animation for expanding checkboxes
        self.animation = QPropertyAnimation(self.checkbox_frame, b"maximumHeight")
        self.animation.setDuration(300)
    
    def get_scripts(self):
        if self.title == "Recruitment":
            return [
                "Total Screened Particiapnts",
                "Participants that Missed Recruitment Window",
                "Particiapnts In Recruitment Window",
                "Participants Not Yet In Recruitment Window",
                "Particiapnts Currently Scheduled",
                "Average Number of Times Scheduled",
            ]
        elif self.title == "Enrollment":
            return [
                "Total Records",
                "Total Completed Visits",
                "Total Missed Visits",
                f"Completed Visits as of {self.cutoff.date()}",
                "Participants In Visit Window",
                "Particiapnts Not Yet In Visit Window",
            ]

        return []
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.file_path = urls[0].toLocalFile()
            self.file_name = os.path.basename(self.file_path)
            self.drop_label.setText(f"File Selected: {self.file_name}")
            self.drop_label.setStyleSheet("""
                border: 2px solid #2ecc71; 
                padding: 20px; 
                text-align: center;
                background-color: #1e3d2f; 
                border-radius: 10px;
                color: #2ecc71;
                font-size: 14px;
                font-weight: 500;
            """)
            self.expand_checkboxes()

    def openFileDialog(self, event):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File","", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            self.file_path = file_path
            self.file_name = os.path.basename(self.file_path)
            self.drop_label.setText(f"File Selected: {self.file_name}")
            self.drop_label.setStyleSheet("""
                border: 2px solid #2ecc71; 
                padding: 20px; 
                text-align: center;
                background-color: #1e3d2f; 
                border-radius: 10px;
                color: #2ecc71;
                font-size: 14px;
                font-weight: 500;
            """)
            self.expand_checkboxes()
        
    def expand_checkboxes(self):
        # Make sure the frame is visible before starting animation
        self.checkbox_frame.setVisible(True)
        self.checkbox_frame.setMaximumHeight(0)  # Start with zero height
        
        # Create a smooth animation
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.checkbox_frame.sizeHint().height())
        self.animation.setDuration(400)  # Slightly longer for smoother effect
        
        # Use an easing curve for more natural animation
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Start the animation
        self.animation.start()
    
    def get_selected_scripts(self):
        return [name for name, checkbox in self.checkboxes.items() if checkbox.isChecked()]

    def update_cutoff_date(self, new_date):
        """Update the cutoff date and refresh the script names"""
        self.cutoff = pd.Timestamp(new_date)
        
        # Update script names that include the date
        if self.title == "Enrollment":
            # First, find the checkbox with the date
            date_script_name = None
            new_script_name = None
            
            # Find the old script name and create the new one
            for script_name in list(self.checkboxes.keys()):
                if "Completed Visits as of" in script_name:
                    date_script_name = script_name
                    new_script_name = f"Completed Visits as of {self.cutoff.date()}"
                    break
            
            # If we found a date script, update it
            if date_script_name and new_script_name and date_script_name != new_script_name:
                # Get the checkbox
                checkbox = self.checkboxes[date_script_name]
                # Update the checkbox text
                checkbox.setText(new_script_name)
                # Update the dictionary safely
                self.checkboxes[new_script_name] = checkbox
                del self.checkboxes[date_script_name]
