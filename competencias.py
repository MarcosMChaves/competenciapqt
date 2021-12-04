from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QMessageBox, QPushButton, QTableWidget
from PyQt5 import QtWidgets
from PyQt5 import uic

import MySQLdb as mdb
import sys
from database import *


class UI(QMainWindow):
	def __init__(self):
		super(UI, self).__init__()

		uic.loadUi('competencias.ui', self)

		self.exit = QAction('&Sair', self)
		self.menubar.addAction(self.exit)
		self.exit.triggered.connect(self.close)

		self.tableWidget.setColumnWidth(0,0)
		self.tableWidget.setColumnWidth(1,300)

		mydb = self.DBConnection()

		mysql = mydb.cursor()
		SQL = 'SELECT id_competencia, nome_competencia FROM Competencia ORDER BY nome_competencia'
		mysql.execute(SQL)
		query = mysql.fetchall()

		self.tableWidget.setRowCount(len(query))
		for dado in query:
			self.tableWidget.setItem(dado[0], 0, QtWidgets.QTableWidgetItem(dado[0]))
			self.tableWidget.setItem(dado[0], 1, QtWidgets.QTableWidgetItem(dado[1]))
			#print(dado[0], dado[1])

		mydb.close()

		self.show()

	def menuSair(self):
		#app.quit()
		self.close

	def DBConnection(self):
		global MYSQL_ENGINE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_NAME
		
		try:
		    db = mdb.connect(MYSQL_ENGINE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_NAME)
#		    QMessageBox.about(self, 'Connection', 'Database Connected Successfully')

		except mdb.Error as e:
#		    QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
		    sys.exit(1)

		return db

app = QApplication(sys.argv)
UIWindow = UI()

widget = QtWidgets.QStackedWidget()
widget.addWidget(UIWindow)
widget.show()


sys.exit(app.exec_())