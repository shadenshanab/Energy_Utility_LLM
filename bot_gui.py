import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout

from query_data import fetch_response


class ChatApplication(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Sets up the user interface for the chat application."""
        self.setWindowTitle('Utility Bot Chat')
        self.setGeometry(100, 100, 400, 600) 

        # Chat history area
        self.conversation = QTextEdit(self)
        self.conversation.setReadOnly(True)
        self.conversation.setStyleSheet("background-color: #FFFFFF; font: 12pt 'Arial';")

        # User input area
        self.user_input = QLineEdit(self)
        self.user_input.setStyleSheet("background-color: #F0F0F0; font: 12pt 'Arial';")

        # Send button
        self.send_button = QPushButton('Send', self)
        self.send_button.setStyleSheet("background-color: #4CAF50; color: white; font: 12pt 'Arial';")
        self.send_button.clicked.connect(self.send)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.conversation)
        hbox = QHBoxLayout()
        hbox.addWidget(self.user_input)
        hbox.addWidget(self.send_button)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def send(self):
        """Processes the sending of a message."""
        user_text = self.user_input.text().strip()
        if not user_text:
            return

        # Update conversation display
        self.update_conversation("You: " + user_text + "\n" + "-----")

        # Get the bot's response
        response = fetch_response(user_text)
        self.update_conversation(response + "\n" + "-----")

        # Clear input
        self.user_input.clear()

    def update_conversation(self, message):
        """Updates the conversation display with a new message."""
        self.conversation.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatApplication()
    ex.show()
    sys.exit(app.exec_())

