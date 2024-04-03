import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QComboBox, QProgressBar
from PyQt5.QtGui import QFont, QColor, QCursor
from PyQt5.QtCore import Qt, QTimer

class AppGenerator(QWidget):
    def __init__(self, onSubmit):
        super().__init__()
        self.onSubmit = onSubmit
        self.initUI()

    def initUI(self):
        self.setWindowTitle('App Generator')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.platformLabel = QLabel('Platform:')
        self.platformInput = QComboBox()
        self.platformInput.addItems(['MacOS', 'Linux', 'Windows'])
        layout.addWidget(self.platformLabel)
        layout.addWidget(self.platformInput)

        self.projectNameLabel = QLabel('Project Name:')
        self.projectNameInput = QLineEdit()
        self.projectNameInput.textChanged.connect(self.removeSpaces)
        layout.addWidget(self.projectNameLabel)
        layout.addWidget(self.projectNameInput)

        self.promptLabel = QLabel('Prompt:')
        self.promptInput = QTextEdit()
        layout.addWidget(self.promptLabel)
        layout.addWidget(self.promptInput)

        self.generateButton = QPushButton('Generate')
        self.generateButton.setStyleSheet('''
            QPushButton {
                background-color: #000000;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #050505;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        ''')
        self.generateButton.clicked.connect(self.generateApp)
        layout.addWidget(self.generateButton)

        self.progressBar = QProgressBar()
        self.progressBar.setVisible(False)
        layout.addWidget(self.progressBar)

        self.setLayout(layout)

        self.projectNameInput.textChanged.connect(self.validateFields)
        self.promptInput.textChanged.connect(self.validateFields)

        self.validateFields()

    def removeSpaces(self, text):
        self.projectNameInput.setText(text.replace(' ', ''))

    def validateFields(self):
        project_name = self.projectNameInput.text()
        prompt = self.promptInput.toPlainText()

        if project_name and len(prompt) >= 10:
            self.generateButton.setEnabled(True)
            self.generateButton.setStyleSheet('''
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3e8e41;
                }
            ''')
        else:
            self.generateButton.setEnabled(False)
            self.generateButton.setStyleSheet('''
                QPushButton {
                    background-color: #CCCCCC;
                    color: #999999;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                }
            ''')

    def generateApp(self):
        platform = self.platformInput.currentText()
        project_name = self.projectNameInput.text()
        prompt = self.promptInput.toPlainText()

        self.generateButton.setEnabled(False)
        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        QTimer.singleShot(0, lambda: self.simulateLoading(platform, project_name, prompt))
        
    def removeSpaces(self, text):
        self.projectNameInput.setText(text.replace(' ', ''))

    def validateFields(self):
        project_name = self.projectNameInput.text()
        prompt = self.promptInput.toPlainText()

        if project_name and len(prompt) >= 10:
            self.generateButton.setEnabled(True)
            self.generateButton.setStyleSheet('''
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3e8e41;
                }
            ''')
        else:
            self.generateButton.setEnabled(False)
            self.generateButton.setStyleSheet('''
                QPushButton {
                    background-color: #CCCCCC;
                    color: #999999;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                }
            ''')

    def generateApp(self):
        project_name = self.projectNameInput.text()
        prompt = self.promptInput.toPlainText()

        platform = self.platformInput.currentText()

        self.generateButton.setEnabled(False)
        self.progressBar.setVisible(True)
        self.progressBar.setValue(0)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        QTimer.singleShot(0, lambda: self.simulateLoading(platform, project_name, prompt))

    def simulateLoading(self, platform, project_name, prompt):
        for i in range(101):
            self.progressBar.setValue(i)
            QApplication.processEvents()  # Process events to update the UI
            if i == 100:
                self.generateButton.setEnabled(True)
                self.progressBar.setVisible(False)
                QApplication.restoreOverrideCursor()  # Restore the default cursor
                self.onSubmit(project_name, prompt, platform)
            QTimer.singleShot(20, lambda: None)