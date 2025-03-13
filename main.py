from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                            QApplication, QHBoxLayout, QLabel, QDateEdit,
                            QDialog, QTextEdit, QToolButton, QScrollArea, QFrame)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import sys
from file_section import FileSection
from results_section import ResultsSection
import pandas as pd
import datetime
from Logic.logic import Logic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BTCF: Recruitment & Enrollment Data Processor")
        self.setGeometry(100, 100, 900, 800)

        # Set application style with dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e2130;
            }
            QWidget {
                background-color: #1e2130;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 0, y2: 1, 
                    stop: 0 #3498db, 
                    stop: 1 #2980b9
                );
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 0, y2: 1, 
                    stop: 0 #2980b9, 
                    stop: 1 #2471a3
                );
            }
            QPushButton:pressed {
                background: #2471a3;
            }
        """)

        # Create a scroll area for the main content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)  # Remove the frame
        self.setCentralWidget(scroll_area)

        # Create the central widget that will contain all content
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)  # Add some spacing between elements
        layout.setContentsMargins(15, 15, 15, 15)  # Add some margins

        # Set the central widget as the scroll area's widget
        scroll_area.setWidget(central_widget)
        
        # Header with title
        header_label = QLabel("BTCF: Recruitment & Enrollment Data Processor")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #3498db;
            margin: 15px 0;
        """)
        layout.addWidget(header_label)

        # Date selection widget
        date_container = QWidget()
        date_layout = QHBoxLayout(date_container)
        date_layout.setContentsMargins(10, 5, 10, 5)
        date_label = QLabel("Select Cutoff Date:")
        date_label.setStyleSheet("font-size: 16px; margin-right: 10px;")

        self.date_selector = QDateEdit()
        self.date_selector.setDate(datetime.date.today())
        self.date_selector.setCalendarPopup(True)
        self.date_selector.setDisplayFormat("MM/dd/yyyy")
        self.date_selector.setStyleSheet("""
            QDateEdit {
                background-color: #2a2f45;
                border: 1px solid #3498db;
                border-radius: 4px;
                padding: 5px;
                color: white;
                font-size: 14px;
            }
            QDateEdit::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #3498db;
                image: url(data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24'%3E%3Cpath fill='%23ffffff' d='M7 10l5 5 5-5z'/%3E%3C/svg%3E);
            }
        """)

        date_layout.addWidget(date_label)
        date_layout.addWidget(self.date_selector)
        date_layout.addStretch()

        layout.addWidget(date_container)

        # Two sections for file upload
        self.recruitment_section = FileSection("Recruitment", datetime.date.today())
        self.enrollment_section = FileSection("Enrollment", datetime.date.today())

        # Layout for both sections with spacing
        sections_layout = QHBoxLayout()
        sections_layout.setSpacing(20)
        sections_layout.setContentsMargins(10, 10, 10, 10)
        sections_layout.addWidget(self.recruitment_section)
        sections_layout.addWidget(self.enrollment_section)
        layout.addLayout(sections_layout)
        
        # Create a container for the process button with a horizontal layout
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Add process button with modern styling
        process_button = QPushButton("Process Data")
        process_button.setCursor(Qt.PointingHandCursor)
        process_button.setFixedSize(200, 50)  # Set a fixed size that won't change
        process_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 0, y2: 1, 
                    stop: 0 #3498db, 
                    stop: 1 #2980b9
                );
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 0, y2: 1, 
                    stop: 0 #2980b9, 
                    stop: 1 #2471a3
                );
            }
            QPushButton:pressed, QPushButton:focus {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 0, y2: 1, 
                    stop: 0 #3498db, 
                    stop: 1 #2980b9
                );
                outline: none;
                border: none;
            }
        """)

        # Connect the process button to the process_data method
        process_button.clicked.connect(self.process_data)

        # Add stretches on both sides to center the button and prevent resizing
        button_layout.addStretch(1)
        button_layout.addWidget(process_button)
        button_layout.addStretch(1)

        # Add the button container to the main layout
        layout.addWidget(button_container)
        
        # Add a status bar for feedback
        self.statusBar().setStyleSheet("""
            background-color: #2a2f45;
            color: #e0e0e0;
            padding: 8px;
            font-size: 14px;
        """)
        self.statusBar().showMessage("Ready to process data")

        # Results container (initially hidden)
        self.results_container = QWidget()
        self.results_container.setVisible(False)
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setContentsMargins(10, 10, 10, 20)
        self.results_layout.setSpacing(20)

        # Add a title for the results section
        results_title = QLabel("Processing Results")
        results_title.setAlignment(Qt.AlignCenter)
        results_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #3498db;
            margin: 10px 0;
        """)
        self.results_layout.addWidget(results_title)

        # Create result sections using the new ResultsSection class
        self.recruitment_results = ResultsSection("Recruitment")
        self.enrollment_results = ResultsSection("Enrollment")
        
        # Add result sections to the results container
        self.results_layout.addWidget(self.recruitment_results)
        self.results_layout.addWidget(self.enrollment_results)

        # Add the results container to the main layout
        layout.addWidget(self.results_container)

        # Add a large spacer at the bottom to ensure everything is visible
        bottom_spacer = QWidget()
        bottom_spacer.setMinimumHeight(120)
        layout.addWidget(bottom_spacer)

        # Connect date selector to update file sections when date changes
        self.date_selector.dateChanged.connect(self.date_changed)

    def process_data(self):
        # Get the selected date
        selected_date = self.date_selector.date().toPyDate()
        
        # Update status
        self.statusBar().showMessage("Processing data...")
        
        # Track if we have any results to show
        has_results = False
        
        # Process Recruitment data if a file is selected
        if self.recruitment_section.file_path:
            recruitment_scripts = self.recruitment_section.get_selected_scripts()
            if recruitment_scripts:
                try:
                    recruitment_logic = Logic(
                        script_type="Recruitment",
                        selected_scripts=recruitment_scripts,
                        file_path=self.recruitment_section.file_path,
                        cutoff_date=selected_date
                    )
                    recruitment_results = recruitment_logic.runScripts()
                    self.recruitment_results.display_results(recruitment_results)
                    has_results = True
                except Exception as e:
                    self.statusBar().showMessage(f"Error processing recruitment data: {str(e)}")
        
        # Process Enrollment data if a file is selected
        if self.enrollment_section.file_path:
            enrollment_scripts = self.enrollment_section.get_selected_scripts()
            if enrollment_scripts:
                try:
                    enrollment_logic = Logic(
                        script_type="Enrollment",
                        selected_scripts=enrollment_scripts,
                        file_path=self.enrollment_section.file_path,
                        cutoff_date=selected_date
                    )
                    enrollment_results = enrollment_logic.runScripts()
                    self.enrollment_results.display_results(enrollment_results)
                    has_results = True
                except Exception as e:
                    self.statusBar().showMessage(f"Error processing enrollment data: {str(e)}")
        
        # Show and animate the results container if we have results
        if has_results:
            self.animate_results_container()
            self.statusBar().showMessage("Processing complete")
        else:
            self.statusBar().showMessage("No data to process. Please select files and scripts.")

    def animate_results_container(self):
        # Make sure the container is visible
        self.results_container.setVisible(True)
        
        # Set a minimum height for the container
        self.results_container.setMinimumHeight(1000)  # Increased from 500 to 1000 to accommodate taller results sections
        
        # Create animation for the container
        self.results_animation = QPropertyAnimation(self.results_container, b"maximumHeight")
        self.results_animation.setDuration(500)  # Half a second for the animation
        self.results_animation.setStartValue(0)
        
        # Calculate a reasonable end value - either the sizeHint or a minimum of 1000
        end_height = max(self.results_container.sizeHint().height(), 1000)
        self.results_animation.setEndValue(end_height)
        
        self.results_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Start the animation
        self.results_animation.start()

    def date_changed(self):
        """Handle date changes and update file sections"""
        new_date = self.date_selector.date().toPyDate()
        
        # Update both file sections with the new date
        self.recruitment_section.update_cutoff_date(new_date)
        self.enrollment_section.update_cutoff_date(new_date)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())