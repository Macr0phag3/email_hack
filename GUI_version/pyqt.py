import os
import sys
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

class EmailHackerWidget(QWidget):
    def __init__(self):
        super(EmailHackerWidget, self).__init__()
        self.InitUI()
        self.show()

    def InitUI(self):
        self.setWindowTitle("Email Hacker")

        grid = QGridLayout()
        self.setLayout(grid)

        items = ['From Address', 
                 'To Address',
                 'Email Subject',
                 'Thread Num',
                 'Verbose',
                 'Crazy Mode',
                 'Body',
                 'Send']

        self.text_objs = {}
        self.v_group = QButtonGroup(self)
        self.c_group = QButtonGroup(self)
        hight = 0
        for name in items:
            if name == 'Send':
                send_btn = QPushButton(name, self)
                send_btn.clicked.connect(self.run)
                grid.addWidget(send_btn, hight, 3, 1, 2)
                hight += 1
            elif name == 'Body':
                text = QTextEdit(self)
                self.text_objs[name] = text
                grid.addWidget(text, hight, 0, 3, 5)
                hight += 3
            elif name == 'Verbose':
                label = QLabel(name + ': ', self)
                label.setAlignment(Qt.AlignRight)
                grid.addWidget(label, hight, 0, 1, 1)
                for rank in range(4):
                    rb = QRadioButton(str(rank), self)
                    if rank == 0:
                        rb.setChecked(True)
                    self.v_group.addButton(rb, rank)
                    position = rank + 1
                    grid.addWidget(rb, hight, position, 1, 1)
                hight += 1
            elif name == 'Crazy Mode':
                label = QLabel(name + ': ', self)
                label.setAlignment(Qt.AlignRight)
                grid.addWidget(label, hight, 0, 1, 1)
                for i in range(2):
                    rb = QRadioButton(['False', 'True'][i], self)
                    if i == 0: # set default value
                        rb.setChecked(True)
                    self.c_group.addButton(rb, i)
                    position = 2 * i + 1
                    grid.addWidget(rb, hight, position, 1, 2)
                hight += 1
            else:
                label = QLabel(name + ': ', self)
                label.setAlignment(Qt.AlignRight)
                line = QLineEdit(self)
                if name == 'Thread Num':
                    line.setValidator(QIntValidator())
                self.text_objs[name] = line
                grid.addWidget(label, hight, 0, 1, 1)
                grid.addWidget(line, hight, 1, 1, 4)
                hight += 1
            
    def run(self):
        attr = {'From Address': '-faddr', 
                'To Address': '-taddr',
                'Email Subject': '-s',
                'Thread Num': '-tnum',
                'Body': '-b'}
        cmd = 'python3 email_hacker.py'

        for name, obj in self.text_objs.items():
            text = None
            if isinstance(obj, QTextEdit):
                text = obj.toPlainText()
            elif isinstance(obj, QLineEdit):
                text = obj.text()
            else:
                raise ValueError('type<%s> is not support' % type(obj))
            if not text:
                QMessageBox.information(self, 'Information',
                                        '"%s" has not been set, pls check your config' % name)
                return
            if name == 'Email Subject' or name == 'Body':
                text = '"' + text + '"'
            cmd += ' ' + attr[name] + ' ' + text
        verbose_rank = self.v_group.checkedId()
        cmd += ' -v ' + str(verbose_rank)
        if self.c_group.checkedId():
            cmd += ' -c'
        os.system(cmd)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = EmailHackerWidget()
    sys.exit(app.exec_())
