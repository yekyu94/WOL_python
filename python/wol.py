import sys
import socket, struct, time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class LayoutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        wg = WidgetSet()
        self.setCentralWidget(wg)
        self.statusBar().showMessage('Youngq.tistory.com')

        self.setWindowTitle('WOL Program')
        self.setWindowIcon(QIcon('./img/web.png'))
        self.setGeometry(500, 500, 350, 180)
        self.show()

class WidgetSet(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Line 1 : Wol 이미지 + msg 영역
        hbox0 = QHBoxLayout()
        hbox0.setAlignment(Qt.AlignVCenter)

        pixmap = QPixmap('./img/wol_mini.png')
        pixmap = pixmap.scaledToWidth(35)
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        hbox0.addWidget(lbl_img)
        hbox0.addStretch(200)

        msg = QLabel()
        msg.setFixedSize(200,25)
        msg.setText("Ready")
        msg.setAlignment(Qt.AlignRight)
        self.err = msg
        hbox0.addWidget(msg)

        # Line 2 : 대역폭입력 + 콤보박스
        hbox1 = QHBoxLayout()
        hbox1.setAlignment(Qt.AlignVCenter)

        qle1 = QLineEdit(self)
        qle1.setFixedSize(170, 25)
        qle1.setPlaceholderText("목적지 IP주소 또는 망주소 입력")
        self.ip = qle1
        hbox1.addWidget(qle1)
        hbox1.addStretch(20)

        cIP = QLabel()
        cIP.setFixedSize(110, 30)
        currentIP = self.ipaddr()
        cIP.setText("IP : "+currentIP)
        hbox1.addWidget(cIP)

        # Line 3 : 맥주소 입력 + 전송버튼
        hbox2 = QHBoxLayout()
        hbox2.setAlignment(Qt.AlignHorizontal_Mask)
        qle2 = QLineEdit(self)
        qle2.setFixedSize(170, 25)
        qle2.setPlaceholderText("MAC 주소 입력")
        self.mac = qle2
        hbox2.addWidget(qle2)
        hbox2.addStretch(20)

        btn = QPushButton(self)
        btn.setText('Send')
        btn.setFixedSize(70, 30)
        self.sendBtn = btn
        btn.clicked.connect(self.sending) # EventH

        hbox2.addWidget(btn)
        # Stacking : 레이아웃 배치
        vbox = QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        self.setLayout(vbox)

    def sending(self):
        try:
            WOL(self.mac.text(), self.ip.text())
            self.err.setText("신호 전송완료")
        except:
            self.err.setText("잘못된 입력이 존재합니다.")

    def ipaddr(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

def WOL(macAddr, network):
    sep = macAddr[2]
    macAddr = macAddr.replace(sep, '')

    data = b'FFFFFFFFFFFF' + (macAddr * 16).encode()
    send_data = b''

    for i in range(0, len(data), 2):
        send_data += struct.pack('B', int(data[i: i + 2], 16))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for i in range(3):
        sock.sendto(send_data, (network, 9))
        time.sleep(0.05)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LayoutWindow()
    sys.exit(app.exec_())
