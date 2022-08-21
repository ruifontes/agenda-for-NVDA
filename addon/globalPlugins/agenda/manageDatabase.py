# -*- coding: UTF-8 -*-
# Part of Agenda add-on
# Modul for database routines
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from . import sqlite3
import time
import	datetime

dirDatabase = ""

# Function to convert strings to upper case on  appointements search, used inside database select command
def upcase (field):
	return field.decode().upper()


class manageDatabase():
	def createDatabase(dirDatabase):
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbCursor.execute("""
			CREATE TABLE agenda(
			data integer primary key,
			diadasemana text,
			descricao text,
			alarmedia boolean,
			alarmehora boolean,
			alarmemeiahora boolean,
			alarmequartodehora boolean,
			alarmehoraexata boolean,
			periodicidade text)
			""")
		dbAgenda.commit()
		dbAgenda.close()

	def increasePeriodicity(dirDatabase):
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		# create periodicity table if It isn't exists
		dbCursor.execute("""
		SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
		""")
		resultSet = dbCursor.fetchall()
		flagTable = False
		for table in  resultSet:
			if table[0] =='periodicity':
				flagTable = True
		if not flagTable:
			dbCursor.execute("""
				CREATE TABLE periodicity (
				dataInicial integer primary key,
				tipo integer,
				dataFinal integer)
				""")
			dbAgenda.commit()
		dbAgenda.close()

	def removeItem(itemToRemove, dirDatabase):
		# function that replaces the upper function inside select
		def upcase (field):
			# check variable type to always return str
			if isinstance(field, str):
				return field.upper()
			else:
				return field.decode().upper()
		itemToRemove = str(itemToRemove)
		if itemToRemove[0].isalpha():
			query = "delete from agenda where " + itemToRemove
		else:
			query = "delete from agenda where data= " + itemToRemove
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbAgenda.create_function("upcase", 1, upcase)
		dbCursor.execute(query)
		dbAgenda.commit()
		dbAgenda.close()

	def findItem(what, itemToFind, dirDatabase, all):
		dirDatabase = dirDatabase
		# function that replaces the upper function inside select
		def upcase (field):
			# check variable type to always return str
			if isinstance(field, str):
				return field.upper()
			else:
				return field.decode().upper()
		query = "select " + what + " from agenda where " + itemToFind
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbAgenda.create_function("upcase", 1, upcase)
		dbCursor.execute(query)
		if all == True:
			occurs = dbCursor.fetchall()
		else:
			occurs = dbCursor.fetchone()
		dbAgenda.close()
		return occurs

	def findRepeat(eventInfo, dirDatabase):
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbCursor.execute("select * from periodicity where dataInicial=?", (eventInfo.register,))
		occurs = dbCursor.fetchone()
		if occurs!=None:
			eventInfo.typeRepeat=occurs[1]
			eventInfo.finalDate = occurs[2]
		else:
			eventInfo.typeRepeat=-1
			eventInfo.finalDate=0
		dbAgenda.close()

	def updateRepeat (eventInfo, dirDatabase):
		if eventInfo.typeRepeat>0:
			# Conecting to database
			dbAgenda = sqlite3.connect(dirDatabase)
			dbCursor = dbAgenda.cursor()
			dbCursor.execute("""
				select * 
				from periodicity
				where dataInicial=?
			""", (eventInfo.register,))
			occurs=dbCursor.fetchone()
			if occurs!=None:
				dbCursor.execute("""
					update periodicity
					set tipo=?, dataFinal=?
					where dataInicial=?
					""", (eventInfo.typeRepeat, eventInfo.finalDate, eventInfo.register))
				dbAgenda.commit()
			else:
				dbCursor.execute("""
					insert into periodicity  values (?, ?, ?)
					""", (eventInfo.register, eventInfo.typeRepeat, eventInfo.finalDate))
				dbAgenda.commit()
			dbAgenda.close()

	def removeRepeat (register, dirDatabase):
		# Conecting to database
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbCursor.execute("""
			select * 
			from periodicity
			where dataInicial=?
		""", (register,))
		occurs=dbCursor.fetchone()
		if occurs!=None:
			dbCursor.execute("""
				delete from periodicity
				where dataInicial=?
				""", (register,))
			dbAgenda.commit()
		dbAgenda.close()

	def findRepeatIntervalDate (startDate, endDate, fullDay, dirDatabase):
		dirDatabase = dirDatabase
		countFound = 0
		startYear = int(startDate/100000000)
		startMonth = int(startDate / 1000000)-(startYear * 100)
		startDay = int(startDate / 10000)-(startYear * 10000 + startMonth * 100)
		startHour = int((startDate%10000)/100)
		startMinutes = startDate%100

		# if startDat we will start with 0 hour
		if fullDay:
			startDateToSearch = str(startDate)[:8]+'0000'
		else:
			startDateToSearch = str(startDate)
		startDateInt = int(startDateToSearch)

		endYear = int(endDate / 100000000)
		endMonth = int(endDate / 1000000)-(endYear * 100)
		endDay = int(endDate / 10000)-(endYear * 10000 + endMonth * 100)
		endHour = int((endDate%10000)/100)
		endMinutes = endDate%100
		# get information for full day
		if fullDay:
			endDateToSearch = str(endDate)[:8]+'2359'
		else:
			endDateToSearch = str(endDate)
		endDateInt = int(endDateToSearch)

		allPeriodicEvents = []
		# Search for all occurrences on  date interval
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbCursor.execute("""
			select p.*, a.*
			from periodicity p, agenda a
			where  ((p.dataInicial<=? and p.dataFinal>=?) or 
				(p.dataInicial<=? and p.dataFinal<=? and p.dataFinal>=?) or 
				(p.dataInicial>=? and p.dataInicial<=? and p.dataFinal>=?) or
				(p.dataInicial>=? and p.dataInicial<=? and p.dataFinal<=? and p.dataFinal>=p.dataInicial)) and 
				a.data=p.dataInicial order by p.dataInicial asc
		""", (startDateInt, endDateInt, startDateInt, endDateInt, startDateInt, startDateInt, endDateInt, endDateInt, startDateInt, endDateInt, endDateInt))
		occurs = dbCursor.fetchall()
		if occurs!=None:
			# correct date
			def correctDate(date1):
				monthPeriodic = int(str(date1)[4:6])
				if monthPeriodic>12:
					date1 -= int(monthPeriodic/12.1)*12000000
					date1 += int(monthPeriodic/12)*100000000
					monthPeriodic = monthPeriodic%12.1 if monthPeriodic%12>0 else 12
				yearPeriodic = int(str(date1)[:4])
				dayPeriodic = int(str(date1)[6:8])
				if monthPeriodic in [4, 6, 9, 11] and dayPeriodic>30:
					date1 -= 10000
				if monthPeriodic==2:
					februaryDay = 29  if yearPeriodic%4==0 and yearPeriodic%100>0 else 28
					if dayPeriodic>februaryDay:
						date1 -= (dayPeriodic-februaryDay)*10000
				return date1

			for register in occurs:
				# calculate all occurrences for periodicity
				qtt = occurrencesToDateInterval(register[0], endDateInt, register[1])
				if qtt>0:
					sDate = register[0]
					eventTimeStr = str(sDate)[8:12]
					startPeriodic =  datetime.datetime.strptime(str(sDate)[6:8]+'/'+str(sDate)[4:6]+'/'+str(sDate)[:4]+' '+str(sDate)[8:10]+':'+str(sDate)[10:12], '%d/%m/%Y %H:%M')
					for dateOccurs in range(1, qtt+1):
						# calculate all dates on a periodic event
						if register[1]==1:
							nextEvent  = startPeriodic + datetime.timedelta(days=+dateOccurs)
							periodicDate  = int(datetime.datetime.strftime(nextEvent, '%Y%m%d')+eventTimeStr)
						elif register[1]==2:
							nextEvent  = startPeriodic+ datetime.timedelta(days=+(dateOccurs*7))
							periodicDate  = int(datetime.datetime.strftime(nextEvent, '%Y%m%d')+eventTimeStr)
						elif register[1]==3:
							nextEvent  = startPeriodic + datetime.timedelta(days=+(dateOccurs*14))
							periodicDate  = int(datetime.datetime.strftime(nextEvent, '%Y%m%d')+eventTimeStr)
						elif register[1]>=4 and register[1]<=7:
							periodicDate = correctDate(sDate+(dateOccurs*(register[1]-3)*1000000))
						elif register[1]==8:
							periodicDate = correctDate(sDate+(dateOccurs*6000000))
						elif register[1]==9:
							periodicDate = sDate+(dateOccurs*100000000)
						if periodicDate>=startDateInt and periodicDate<=endDateInt:
							# save dataInicial field of original periodicity register and actual occurrency
							listPeriodic = [register[0], periodicDate]
							typeFrequency = [register[1]]
							allPeriodicEvents += [listPeriodic+list(register[4:])+typeFrequency]

							countFound += 1

			return allPeriodicEvents
		else:
			return []
		dbAgenda.close()

def occurrencesToDateInterval(sDate, eDate, typeRepeat):
	startDate = datetime.datetime.strptime(str(sDate)[6:8]+'/'+str(sDate)[4:6]+'/'+str(sDate)[:4], '%d/%m/%Y').date()
	endDate = datetime.datetime.strptime(str(eDate)[6:8]+'/'+str(eDate)[4:6]+'/'+str(eDate)[:4], '%d/%m/%Y').date()

	if endDate<startDate:
		dlg = wx.MessageDialog(None, _("Your final date is oldest your inicial date."), _("Incorrect date interval"), wx.OK).ShowModal()
		return 0
	else:
		startYear = int(sDate/100000000)
		startMonth = int(sDate/1000000)-(startYear*100)
		startDay = int(sDate/10000)-(startYear*10000 + startMonth*100)

		endYear = int(eDate/100000000)
		endMonth = int(eDate/1000000)-(endYear*100)
		endDay = int(eDate/10000)-(endYear*10000 + endMonth*100)

		# Calculate occurrences
		diffDate1 = abs((endDate-startDate).days)
		occurs = 0
		if typeRepeat==1:
			occurs=diffDate1
		elif typeRepeat==2 or typeRepeat==3:
			occurs = int(diffDate1/(7*(typeRepeat-1)))
		elif typeRepeat>3:
			# Calculate difference between both dates in months
			monthQtt = (endMonth-startMonth) if endYear==startYear else ((endYear-startYear-1)*12+(12-startMonth)+endMonth)
			if typeRepeat<8:
				occurs = int(monthQtt/(typeRepeat-3))
			elif typeRepeat==8:
				occurs = int(monthQtt/6)
			else:
				occurs = int(monthQtt/12)
		return occurs
