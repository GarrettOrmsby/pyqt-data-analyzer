from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, 
                             QFrame, QGraphicsDropShadowEffect, QScrollBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class ResultsSection(QWidget):
    def __init__(self, title):
        """Initialize a results section with the given title"""
        super().__init__()
        self.title = title
        self.initUI()
        
    def initUI(self):
        """Set up the UI components for the results section"""
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        self.setLayout(layout)
        
        # Set overall widget style with dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e2130;
                color: #e0e0e0;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Title label
        self.title_label = QLabel(f"{self.title} Results")
        self.title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 5px;
            padding: 5px;
        """)
        layout.addWidget(self.title_label)
        
        # Results container with styling
        self.results_frame = QFrame()
        self.results_frame.setFrameShape(QFrame.StyledPanel)
        self.results_frame.setStyleSheet("""
            background-color: #2a2f45;
            border-radius: 8px;
            padding: 5px;
        """)
        
        # Add shadow effect to results frame
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.results_frame.setGraphicsEffect(shadow)
        
        # Layout for results frame
        results_layout = QVBoxLayout(self.results_frame)
        results_layout.setContentsMargins(10, 10, 10, 10)
        
        # Text edit for displaying results
        self.results_content = QTextEdit()
        self.results_content.setReadOnly(True)
        self.results_content.setMinimumHeight(450)  # Increased from 300 to 450 to fit all 6 rows
        self.results_content.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable vertical scrollbar
        self.results_content.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.results_content.setStyleSheet("""
            QTextEdit {
                background-color: #2a2f45;
                border: none;
                color: #e0e0e0;
                font-size: 14px;
                padding: 10px;
            }
            QScrollBar:horizontal {
                background: #1e2130;
                height: 14px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #3498db;
                min-width: 20px;
                border-radius: 7px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        results_layout.addWidget(self.results_content)
        layout.addWidget(self.results_frame)
        
        # Initially hide the results
        self.setVisible(False)
    
    def display_results(self, results):
        """Display the results in a formatted HTML table
        
        Args:
            results (dict): Dictionary of script names and their results
        """
        if not results:
            self.setVisible(False)
            return
        
        # Format the results as HTML with clear spacing and styling
        html_content = """
        <style>
            table { 
                width: 100%; 
                border-collapse: collapse; 
                margin-bottom: 10px;
            }
            td { 
                padding: 15px 10px; 
                border-bottom: 1px solid #3a4161;
                line-height: 1.4;
            }
            tr:last-child td { 
                border-bottom: none; 
            }
            td:first-child { 
                width: 70%; 
                font-weight: bold;
                padding-right: 15px;
            }
            td:last-child { 
                width: 30%; 
                text-align: right;
                color: #3498db;
            }
        </style>
        <table>
        """
        
        for script_name, result in results.items():
            html_content += f"<tr><td>{script_name}</td>"
            html_content += f"<td>{result}</td></tr>"
        
        html_content += "</table>"
        
        # Set the content and make the widget visible
        self.results_content.setHtml(html_content)
        self.setVisible(True)
        
        # Calculate the document height to ensure all content is visible
        document = self.results_content.document()
        document_height = document.size().height()
        
        # If the document is taller than our current minimum height, increase the height
        if document_height > 430:  # Leave some margin
            self.results_content.setMinimumHeight(int(document_height) + 30)
    
    def clear_results(self):
        """Clear the results and hide the section"""
        self.results_content.clear()
        self.setVisible(False) 