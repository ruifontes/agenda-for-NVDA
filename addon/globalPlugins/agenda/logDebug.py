# -*- coding: UTF-8 -*-
# Agenda add-on: Module for debug log
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# Copyright (C) 2022-2023 Abel Passos Jr. and Rui Fontes
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
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

