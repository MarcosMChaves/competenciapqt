from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QPushButton
from PyQt5 import uic

import sys


class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		uic.loadUi('competencia.ui', self)

		self.texto = self.findChild(QTextEdit,'texto')
		self.clique_aqui = self.findChild(QPushButton,'clique_aqui')
		self.text_label = self.findChild(QLabel,'text_label')

		self.clique_aqui.clicked.connect(self.clique_me)

		self.show()

	def clique_me(self):
		self.text_label.setText(f'Alô {self.texto.toPlainText()}!')
		self.texto.setPlainText('')

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()