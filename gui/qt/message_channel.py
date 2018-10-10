from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .util import *
dialogs = []  # Otherwise python randomly garbage collects the dialogs...


def show_dialog(main_window, address,wallet,password, is_new=True):
    d = MessageChannel(main_window, address, wallet,password, is_new)
    dialogs.append(d)
    d.show()


class MessageChannel(QDialog):
    def __init__(self, parent, address,wallet,password, is_new):
        # top level window
        WindowModalDialog.__init__(self, parent=None)
        if is_new:
            title = "Create New Channel"
        else:
            title = "Open Existing Channel"
        self.setWindowTitle(title)
        vbox = QVBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(8)
        grid.addWidget(QLabel("Channel Name : "), 0, 0)
        self.channel = QLineEdit()
        grid.addWidget(self.channel, 0, 1)
        vbox.addLayout(grid)
        hbox = QHBoxLayout()

        def channel_name():
            from .bchmessage_public import show_dialog
            from electroncash import bchmessage

            key = bchmessage.MessagingKey.from_wallet(wallet, address, password)
            pmw = bchmessage.PrivMessageWatcher(wallet, key)
            d = show_dialog(parent, pmw, self.channel.text())
            self.accept()

        b = QPushButton("Ok")
        b.clicked.connect(channel_name)
        hbox.addWidget(b)

        b = QPushButton("Close")
        b.clicked.connect(self.reject)
        hbox.addWidget(b)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.exec()

