import os
from datetime import datetime

# Classe para salvar arquivo de log
class logDebug(object):
	def __init__(self, msg, exibeHora=False, apagaAntigo=False):
		self.message(msg, exibeHora, apagaAntigo)

	def message(self, msg, exibeHora, apagaAntigo):
		# file to create  a log to debug
		fileDebug = os.path.join (os.path.dirname(__file__), "log.txt")
		if not apagaAntigo:
			openDebug = open(fileDebug, 'a', encoding='utf-8')
		else:
			openDebug = open(fileDebug, 'w', encoding='utf-8')
		tempo = ""
		if exibeHora:
			tempo = str(datetime.strftime(datetime.now(), '%H:%M:%S'))
		openDebug.write(tempo+': '+msg+'\n')
		openDebug.close()

