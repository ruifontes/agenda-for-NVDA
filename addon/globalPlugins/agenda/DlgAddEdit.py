# -*- coding: UTF-8 -*-
# Part of Agenda add-on
# Module for add and edit window
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
import globalPluginHandler
from .varsConfig import *
from .eventRepeat import dlgRepeat
from .alarmsCheck import CheckAlarms
from .configPanel import *
import threading
# Necessary For translation
addonHandler.initTranslation()


class DlgAddEdit(wx.Dialog):
	global dirDatabase
	def __init__(self, generalVars, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)

		self.globalVars = generalVars
		self.titleAddEd = generalVars.titleAddEd
		self.itemToEdit = generalVars.itemToEdit
		self.scrollDay = None

		self.exitType="Normal"
		self.exitConfirm = False
		self.SetTitle(self.titleAddEd)

		# Store alarmes values
		self.alarmValues = checkBoxVars()

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

		label_1 = wx.StaticText(self, wx.ID_ANY, _("Day:"))
		sizer_3.Add(label_1, 0, 0, 0)
		self.spinDay = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=31)
		sizer_3.Add(self.spinDay, 0, 0, 0)

		label_5 = wx.StaticText(self, wx.ID_ANY, _("Month:"))
		sizer_3.Add(label_5, 0, 0, 0)
		self.comboMonth = wx.ComboBox(self, wx.ID_ANY, choices = months, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		sizer_3.Add(self.comboMonth, 0, 0, 0)

		label_6 = wx.StaticText(self, wx.ID_ANY, _("Year:"))
		sizer_3.Add(label_6, 0, 0, 0)
		self.spinYear = wx.SpinCtrl(self, wx.ID_ANY, "1970", min=1970, max=2050)
		sizer_3.Add(self.spinYear, 0, 0, 0)

		self.weekDay = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
		sizer_3.Add(self.weekDay, 0, 0, 0)

		sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

		label_7 = wx.StaticText(self, wx.ID_ANY, _("Hour:"))
		sizer_4.Add(label_7, 0, 0, 0)
		self.spinHour = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=23)
		sizer_4.Add(self.spinHour, 0, 0, 0)

		label_8 = wx.StaticText(self, wx.ID_ANY, _("Minutes:"))
		sizer_4.Add(label_8, 0, 0, 0)
		self.spinMinutes = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, max=59)
		sizer_4.Add(self.spinMinutes, 0, 0, 0)

		label_3 = wx.StaticText(self, wx.ID_ANY, _("Description:"))
		sizer_1.Add(label_3, 0, 0, 0)
		self.description = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_MULTILINE | wx.TE_WORDWRAP)
		sizer_1.Add(self.description, 0, 0, 0)

		sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)

		self.button_repeat = wx.Button(self, wx.ID_ANY, _("&Repeat"))
		sizer_5.Add(self.button_repeat, 0, 0, 0)

		self.button_alarmesDef =  wx.Button(self, wx.ID_ANY, _("&Alarms"))
		sizer_5.Add(self.button_alarmesDef, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK, _("&Ok"))
		self.button_OK.SetDefault()
		sizer_2.Add(self.button_OK, 0, 0, 0)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, _("&Cancel"))
		sizer_2.AddButton(self.button_CANCEL)

		sizer_2.Realize()
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Layout()
		self.CentreOnScreen()

		occurs = ()
		# Fill the fields with the data of the appointment selected on main or search window
		self.currentYear = str(self.itemToEdit)[:4]
		self.currentMonth = str(self.itemToEdit)[4:6]
		self.currentDay = str(self.itemToEdit)[6:8]
		self.itemToEditStr = str(self.itemToEdit)

		self.eventRepeatData = eventRepeatInfo()
		if self.titleAddEd == _("Add"):
			# We are in the Add window
			# adjust current hour
			self.now = str(datetime.datetime.now())
			self.currentHour = self.now[11:13]
			self.currentMinute = self.now[14:16]
			# correct the variable with the received date from the class, if necessary
			self.itemToEditStr = self.currentYear + self.currentMonth + self.currentDay + self.currentHour + self.currentMinute
			self.itemToEdit = int(self.itemToEditStr)

			# Store informations about description and alarms fields to check if they were changed
			self.originalDescription = ""
			self.checkbox_1_Original = False
			self.checkbox_2_Original = False
			self.checkbox_3_Original = False
			self.checkbox_4_Original = False
			self.checkbox_5_Original = False
		else:
			# We are in the Edit window
			# adjust the hour according with class call
			self.currentHour = self.itemToEditStr[8:10]
			self.currentMinute = self.itemToEditStr[10:12]
			# correct the variable with the date received from class call, if necessary
			self.itemToEditStr = self.currentYear + self.currentMonth + self.currentDay + self.currentHour + self.currentMinute
			self.itemToEdit = int(self.itemToEditStr)

			# As we are Editing, loads from database the selected details of selected item
			# Conecting to database
			from .configPanel import dirDatabase
			what = "*"
			find = "data= " + str(self.itemToEdit)
			occurs = manageDatabase.findItem(what, find, dirDatabase, all=False)
			self.eventRepeatData.register=self.itemToEdit
			manageDatabase.findRepeat(self.eventRepeatData, dirDatabase)
			self.currentDateStr = str(self.itemToEdit)
			self.weekDay.SetValue(occurs[1])
			self.description.SetValue(occurs[2])
			self.alarmValues.checkOneDay = (True if occurs[3] else False) 
			self.alarmValues.checkOneHour = (True if occurs[4] else False)
			self.alarmValues.checkHalfHour = (True if occurs[5] else False)
			self.alarmValues.checkFififteenMinutes = (True if occurs[6] else False)
			self.alarmValues.checkExactTime = (True if occurs[7] else False)

			# Stores informations about description and alarms fields to check if they were changed
			self.originalDescription = occurs[2]
			self.checkbox_1_Original = self.alarmValues.checkOneDay
			self.checkbox_2_Original = self.alarmValues.checkOneHour
			self.checkbox_3_Original = self.alarmValues.checkHalfHour
			self.checkbox_4_Original = self.alarmValues.checkFififteenMinutes
			self.checkbox_5_Original = self.alarmValues.checkExactTime

		# Update date and hour fields. This update is made after current date fields been stored with current date or selected date to edit
		self.spinDay.SetValue(int(self.currentDay))
		self.comboMonth.SetSelection(12-int(self.currentMonth))
		self.spinYear.SetValue(int(self.currentYear))
		self.spinHour.SetValue(int(self.currentHour))
		self.spinMinutes.SetValue(int(self.currentMinute))

		# Records the current date in the database search format
		self.currentDate = int(self.currentYear + self.currentMonth + self.currentDay+ self.currentHour + self.currentMinute)

		# Create Ctrl+Enter keystroke
		self.CtrlEnter= wx.Window.NewControlId()
		accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, wx.WXK_RETURN, self.CtrlEnter)])
		self.SetAcceleratorTable(accel_tbl)

		self.Bind(wx.EVT_BUTTON, self.OnPeriodicity, self.button_repeat)
		self.Bind(wx.EVT_BUTTON, self.OnAlarmDef, self.button_alarmesDef)
		self.Bind(wx.EVT_BUTTON, self.onOk, self.button_OK)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, self.button_CANCEL)
		self.Bind(wx.EVT_SPINCTRL, self.update, self.spinYear)
		self.Bind(wx.EVT_SPINCTRL, self.update, self.spinDay)
		self.Bind(wx.EVT_COMBOBOX, self.update, self.comboMonth)
		self.Bind(wx.EVT_SPINCTRL, self.update, self.spinHour)
		self.Bind(wx.EVT_SPINCTRL, self.update, self.spinMinutes)
		self.Bind(wx.EVT_MENU, self.onOk, id=self.CtrlEnter)

		self.updateData()

		# Gets the date fields to make the search
		#Gets the week day
		self.currentWeek = weekDays[datetime.date (int(self.currentYear), int(self.currentMonth), int(self.currentDay)) .weekday ()]
		# Update the weekDay field
		self.weekDay.SetValue(self.currentWeek)
		self.weekToSave = self.currentWeek
		

	def update(self, event):
		# Just to avoid the event
		self.updateData()

	def updateData(self):
		# Gets the date fields to make the search
		yearToSearch = str(self.spinYear.GetValue())
		monthToSearchStr = self.comboMonth.GetValue()
		monthToSearch = '%02d' % (12-months.index(monthToSearchStr))
		# Gets the maximum days of the month
		year = self.spinYear.GetValue()
		month = 12-months.index(monthToSearchStr)
		dayMax = maxDayMonth(year, month)

		self.spinDay.SetRange(1, dayMax)
		dayToSearch = '%02d' % self.spinDay.GetValue()
		hourToSearch = '%02d' % self.spinHour.GetValue()
		minuteToSearch = '%02d' % self.spinMinutes.GetValue()

		dateToSearch = int(yearToSearch + monthToSearch + dayToSearch + hourToSearch + minuteToSearch)

		#Gets the week day
		# weekToSearch = weekDays[datetime.date (int(self.currentYear), int(self.currentMonth), int(self.currentDay)) .weekday ()]
		weekToSearch = weekDays[datetime.date (int(yearToSearch), int(monthToSearch), int(dayToSearch)) .weekday ()]

		# Update weekday field
		self.weekDay.SetValue(weekToSearch)
		weekToSearch = weekDays[datetime.date (int(yearToSearch), int(monthToSearch), int(dayToSearch)) .weekday ()]

		# If date was changed, search in database for items on this date, if the class be instanced as Add
		if self.titleAddEd == _("Add"):
			# Conecting to database
			from .configPanel import dirDatabase
			what = "*"
			find = "data= " + str(dateToSearch)
			occurs = manageDatabase.findItem(what, find, dirDatabase, all=False)
			if occurs != None:
				self.description.SetValue(occurs[2])
				self.alarmValues.checkOneDay = (True if occurs[3] else False)
				self.alarmValues.checkOneHour = (True if occurs[4] else False)
				self.alarmValues.checkHalfHour = (True if occurs[5] else False)
				self.alarmValues.checkFififteenMinutes = (True if occurs[6] else False)
				self.alarmValues.checkExactTime = (True if occurs[7] else False)
			else:
				self.description.SetValue("")
				self.alarmValues.checkOneDay = False
				self.alarmValues.checkOneHour = False
				self.alarmValues.checkHalfHour = False
				self.alarmValues.checkFififteenMinutes = False
				self.alarmValues.checkExactTime = False

	def OnPeriodicity (self, event):
		if self.titleAddEd == _("Edit"):
			self.eventRepeatData.register= self.itemToEdit
			originalTypeRepeat = self.eventRepeatData.typeRepeat
			originalFinalDate = self.eventRepeatData.finalDate
		else:
			originalTypeRepeat = -1
			originalFinalDate = 0
			yearStr = str(self.spinYear.GetValue())
			monthToStr = self.comboMonth.GetValue()
			monthStr = '%02d' % (12-months.index(monthToStr))
			dayStr = '%02d' % self.spinDay.GetValue()
			hourStr = '%02d' % self.spinHour.GetValue()
			minutesStr = '%02d' % self.spinMinutes.GetValue()
			repeatToFind = int(yearStr+monthStr+dayStr+hourStr+minutesStr)
			self.eventRepeatData.register= repeatToFind
		self.eventRepeatData.dirDatabase=dirDatabase

		dlg = dlgRepeat(self.eventRepeatData, self)
		dlg.ShowModal()
		dlg.Destroy()
		if originalTypeRepeat>0 and self.eventRepeatData.typeRepeat==0:
			dlg = wx.MessageDialog(self, _("You disabled the periodicity of this appointement. Do you really want remove its periodicity?"), _("Remove periodic event"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES:
				manageDatabase.removeRepeat(self.eventRepeatData.register, dirDatabase)
			else:
				self.eventRepeatData.typeRepeat = originalTypeRepeat
				self.eventRepeatData.finalDate = originalFinalDate

		event.Skip()

	def OnAlarmDef (self, event):
		dlg = CheckAlarms(self.alarmValues, self)
		dlg.ShowModal()
		dlg.Destroy()
		event.Skip()

	def onOk(self, event):
		# signals wich exit type
		self.exitType = "OK"
		self.changesEnd()

	def changesEnd(self):
		# global itemToEdit
		# global titleAddEd
		# signals wich exit type
		self.exitType = "OK"
		# Gets date and hour fields to add to database
		self.yearToSave = str(self.spinYear.GetValue())
		self.monthToSaveStr = self.comboMonth.GetValue()
		self.monthToSave = '%02d' % (12-months.index(self.monthToSaveStr))
		self.dayToSave = '%02d' % self.spinDay.GetValue()
		self.hourToSave = '%02d' % self.spinHour.GetValue()
		self.minuteToSave = '%02d' % self.spinMinutes.GetValue()

		# Stores date and hour in a single field
		self.dateToSave = int(self.yearToSave + self.monthToSave + self.dayToSave + self.hourToSave + self.minuteToSave)

		# Gets the weekday field
		self.weekToSave = self.weekDay.GetValue()

		# Gets the description field
		self.descriptionToSave = self.description.GetValue()
		if len(self.descriptionToSave) == 0 or self.descriptionToSave.isspace():
			# If description field is blank and  option is Edit, means user deleted the appointement informations. Check if date keeps the same
			if self.titleAddEd == _("Edit") and self.dateToSave == self.itemToEdit:
				dlg = wx.MessageDialog( self, _("You have deleted the appointment description. Do you want to delete the appointment?"), _("Agenda"), wx.YES_NO)
				if dlg.ShowModal()==wx.ID_YES: 
					# Conecting to database
					from .configPanel import dirDatabase
					manageDatabase.removeItem(self.dateToSave, dirDatabase)
					manageDatabase.removeRepeat(self.dateToSave, dirDatabase)

					dlg2 = wx.MessageDialog( self, _("Appointment removed successfully!"), _("Agenda"), wx.OK)
					dlg2.ShowModal()
					dlg2.Destroy()
					self.Close()
					dlg.Destroy()
					generalVars.loadAlarms = True
					return
				else:
					dlg.Destroy()
					return
			# If option is Edit and original date is different from present date fields avoid edition.
			if self.titleAddEd == _("Edit") and self.dateToSave != self.itemToEdit:
				dlg = wx.MessageDialog( self, _("You have deleted the description and changed the date.\nIf you want to add a new appointment, press the Add button on main or search windows\nIf you want to delete an appointment, go to main or search windows, select the appointment and choose the remove button"), _("Agenda"), wx.OK)
				dlg.ShowModal() 
				dlg.Destroy()
				self.Close()
				event.Skip()
				return

			# If we are in the option Add and description field is empty, go back to the Add window
			if self.titleAddEd == _("Add"):
				dlg = wx.MessageDialog( self, _("No description to the appointment"), _("Agenda"), wx.OK)
				dlg.ShowModal() 
				dlg.Destroy()
				return

		# If description is not blank, Capture alarm informations.
		self.alarmOneDay = self.alarmValues.checkOneDay
		self.alarmOneHour = self.alarmValues.checkOneHour
		self.alarm30Minutes = self.alarmValues.checkHalfHour
		self.alarm15Minutes = self.alarmValues.checkFififteenMinutes
		self.alarmHourExact = self.alarmValues.checkExactTime

		# If any alarm was set, set also alarm for exact hour.
		if self.alarmOneDay or self.alarmOneHour or self.alarm30Minutes or self.alarm15Minutes:
			self.alarmHourExact = True

		# Check if exists any appointement for this date and hour. If exist ask if it is to update
		# Conecting to database
		from .configPanel import dirDatabase
		what = "*"
		find = "data= " + str(self.dateToSave)
		line = manageDatabase.findItem(what, find, dirDatabase, all=False)
		if line != None:
			# If database returns some records, so exist appointment for this date/hour
			dlg = wx.MessageDialog( self, _("Informations for this date and hour already exists on agenda. Do you want to replace original informations?"), _("Agenda"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES: 
				# Conecting to database
				from .configPanel import dirDatabase
				dbAgenda = sqlite3.connect(dirDatabase)
				dbCursor = dbAgenda.cursor()
				dbCursor.execute("""
					update agenda
					set diadasemana=?, descricao=?, alarmedia = ?, alarmehora = ?, alarmemeiahora = ?, alarmequartodehora = ?, alarmehoraexata = ?, periodicidade = ?
					where data=?
					""", (self.weekToSave, self.descriptionToSave, self.alarmOneDay, self.alarmOneHour, self.alarm30Minutes, self.alarm15Minutes, self.alarmHourExact,	'Indefinido', self.dateToSave))
				dbAgenda.commit()
				dbAgenda.close()
				self.eventRepeatData.register=self.dateToSave
				manageDatabase.updateRepeat(self.eventRepeatData, dirDatabase)
				dlg2 = wx.MessageDialog( self, _("Record updated successfully!"), _("Agenda"), wx.OK)
				dlg2.ShowModal()
				dlg2.Destroy()
				self.Destroy()
				generalVars.loadAlarms = True

				# Check last appointment to remove
				if self.dateToSave != self.itemToEdit:
					# Conecting to database
					from .configPanel import dirDatabase
					what = "*"
					find = "data= " + str(self.itemToEdit)
					occurs = manageDatabase.findItem(what, find, dirDatabase, all=False)
					if occurs != None:
						# Conecting to database
						from .configPanel import dirDatabase
						manageDatabase.removeItem(self.itemToEdit, dirDatabase)
						manageDatabase.removeRepeat(self.itemToEdit, dirDatabase)
			dlg.Destroy()
			generalVars.loadAlarms = True
		else:
			# Conecting to database
			from .configPanel import dirDatabase
			dbAgenda = sqlite3.connect(dirDatabase)
			dbCursor = dbAgenda.cursor()
			dbCursor.execute("""
				insert into agenda values (?, ?, ?, ?, ?, ?, ?, ?, ?)
				""", (self.dateToSave, self.weekToSave, self.descriptionToSave, self.alarmOneDay, self.alarmOneHour, self.alarm30Minutes, self.alarm15Minutes, self.alarmHourExact, 'indefinido'))
			dbAgenda.commit()

			# Save event repeat
			if self.eventRepeatData.typeRepeat>0:
				dbCursor.execute("""
					insert into periodicity  values (?, ?, ?)
					""", (self.dateToSave, self.eventRepeatData.typeRepeat, self.eventRepeatData.finalDate))
				dbAgenda.commit()
			dbAgenda.close()
			dlg = wx.MessageDialog( self, _("Record saved successfully!"), _("Agenda"), wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
			self.Destroy()
			generalVars.loadAlarms = True
			# If we are editing and the date or hour are different from saved, remove the old record
			if self.titleAddEd == _("Edit") and self.dateToSave != self.itemToEdit: 
				# Conecting to database
				from .configPanel import dirDatabase
				manageDatabase.removeItem(self.itemToEdit, dirDatabase)
				manageDatabase.removeRepeat(self.itemToEdit, dirDatabase)

			self.Close()
			self.Destroy()
			generalVars.loadAlarms

	def OnCancel(self, event):
		if self.exitType== "OK" or self.exitConfirm:
			self.Close()
			self.Destroy()
			return
			event.Skip()
		else:
			# Get the date and hour fields to add to database
			self.yearToSave = str(self.spinYear.GetValue())
			self.monthToSaveStr = self.comboMonth.GetValue()
			self.monthToSave = '%02d' % (12-months.index(self.monthToSaveStr))
			self.dayToSave = '%02d' % self.spinDay.GetValue()
			self.hourToSave = '%02d' % self.spinHour.GetValue()
			self.minutesToSave = '%02d' % self.spinMinutes.GetValue()

			# Stores date and hour in a single string field
			self.dateToSave = int(self.yearToSave + self.monthToSave + self.dayToSave + self.hourToSave + self.minutesToSave)

			# Start checking for changes
			flagIsChanged =(self.dateToSave !=self.itemToEdit) 

			# Gets description field
			flagIsChanged |= (self.description.GetValue() != self.originalDescription)

			# Gets alarms informations
			flagIsChanged |= (self.alarmValues.checkOneDay != self.checkbox_1_Original)
			flagIsChanged |= (self.alarmValues.checkOneHour != self.checkbox_2_Original)
			flagIsChanged |= (self.alarmValues.checkHalfHour != self.checkbox_3_Original)
			flagIsChanged |= (self.alarmValues.checkFififteenMinutes != self.checkbox_4_Original)
			flagIsChanged |= (self.alarmValues.checkExactTime != self.checkbox_5_Original)

			# Check if something was changed in the window
			if flagIsChanged:
				# Confirms with user if he wants to discard changes
				dlg = wx.MessageDialog(self, _("Do you really want to discard the changes on appointment?"), _("Agenda"), wx.YES_NO)
				dlgAnswer = dlg.ShowModal()
				if dlgAnswer==wx.ID_NO:
					# Answer is no
					dlg.Destroy()
					return
				elif dlgAnswer==wx.ID_YES:
					# Answer is yes
					dlg.Destroy()
					self.exitConfirm=True

			self.Close()
			event.Skip()
			self.Destroy()
			return
