from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QMenuBar, QAction, QMessageBox, QPushButton, QTableWidget
from PyQt5 import QtCore, QtWidgets
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

		self.actionNova.triggered.connect(self.pessoa_inserir)
		self.actionExcluir.triggered.connect(self.pessoa_excluir)
		
		#self.tableWidget.itemChanged.connect(self.pessoa_editar)

		self.tableWidget.setColumnWidth(0,0)
		self.tableWidget.setColumnWidth(1,100)
		self.tableWidget.setColumnWidth(2,200)

		self.carregar_tabela()

		self.show()

	def carregar_tabela(self):
		mydb = self.DBConnection()

		mysql = mydb.cursor()
		SQL = 'SELECT id_pessoa, nome_pessoa, sobrenome_pessoa, CONCAT(nome_pessoa, " ", sobrenome_pessoa) AS nome_completo \
						FROM Pessoa \
						ORDER BY nome_completo'
		mysql.execute(SQL)
		query = mysql.fetchall()

		self.tableWidget.setRowCount(0)
		self.tableWidget.setRowCount(len(query))
		item=0
		for dado in query:
			self.tableWidget.setItem(item, 0, QtWidgets.QTableWidgetItem(str(dado[0])))
			self.tableWidget.setItem(item, 1, QtWidgets.QTableWidgetItem(dado[1]))
			self.tableWidget.setItem(item, 2, QtWidgets.QTableWidgetItem(dado[2]))
		#	print(item, dado[0], dado[1])
			item+=1

		mydb.close()

	def pessoa_inserir(self):

		mydb = self.DBConnection()

		mysql = mydb.cursor()
		SQL = 'INSERT INTO Pessoa \
						(nome_pessoa, sobrenome_pessoa) \
						VALUES ("Marianna","Chaves")'
		mysql.execute(SQL)

		mydb.commit()
		mydb.close()

		self.carregar_tabela()

		QMessageBox.about(self, 'Pessoa', f'Pessoa inserida...')


	def pessoa_excluir(self):
		index = self.tableWidget.currentIndex()
		print(index.row())
		pessoa_pk = self.tableWidget.item(index.row(), 0).text()

		mydb = self.DBConnection()

		mysql = mydb.cursor()
		SQL = f'DELETE FROM Pessoa WHERE id_pessoa={pessoa_pk}'
		try:
			mysql.execute(SQL)
			mydb.commit()
	
			QMessageBox.about(self, 'Pessoa', f'Pessoa excluída...')
		except:
			mydb.rollback()

			QMessageBox.about(self, 'SQL Error', "Error!")

		mydb.close()

		self.carregar_tabela()

	def pessoa_editar(self):
		index = self.tableWidget.currentIndex()
		print('UPD= ',index.row())
		pessoa_pk = self.tableWidget.item(index.row(), 0)
		nome = self.tableWidget.item(index.row(), 1)
		sobrenome = self.tableWidget.item(index.row(), 2)

		mydb = self.DBConnection()

		mysql = mydb.cursor()
		SQL = f'UPDATE Pessoa \
					SET nome_pessoa = "{nome}" , \
						sobrenome_pessoa = "{sobrenome}" \
					WHERE id_pessoa={pessoa_pk}'
		try:
			mysql.execute(SQL)
			mydb.commit()
	
			QMessageBox.about(self, 'Pessoa', f'Pessoa atualizada {SQL}...')
		except:
			mydb.rollback()

			QMessageBox.about(self, 'SQL Error', f"Error! {SQL}")

		mydb.close()

		self.carregar_tabela()

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