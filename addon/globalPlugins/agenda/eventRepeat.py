# -*- coding: UTF-8 -*-
# Agenda add-on: Module for interface to set repetitions and set the respective dates
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# Copyright (C) 2022-2023 Abel Passos Jr. and Rui Fontes
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
from . configPanel import *
from .varsConfig import *
from .convertdate import persian

# To start the translation process
addonHandler.initTranslation()


class dlgRepeat(wx.Dialog):
	def __init__(self, eventInfo, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)

		from . varsConfig import months, persianMonths, weekDays, frequency
		from .configPanel import calendarToUse
		self.eventInfo = eventInfo
		self.register = self.eventInfo.register
		self.currentYear = int(self.register/100000000)
		self.currentMonth = int(self.register/1000000)-(self.currentYear*100)
		self.currentDay = int(self.register/10000)-(self.currentYear*10000 + self.currentMonth*100)
		if self.register < 150000000000:
			gregorianDate = persian.to_gregorian(self.currentYear, self.currentMonth, self.currentDay)
			self.currentYear1 = str(gregorianDate[0])
			self.currentMonth1 = str("%02d" % gregorianDate[1])
			self.currentDay1 = str("%02d" % gregorianDate[2])
			self.hour = str(self.register)[8:]
			self.register = int(self.currentYear1 + self.currentMonth1 + self.currentDay1 + self.hour)
		if calendarToUse == _("Persian") and self.currentYear >1500:
			persianDate = persian.from_gregorian(self.currentYear, self.currentMonth, self.currentDay)
			self.currentYear = persianDate[0]
			self.currentMonth = persianDate[1]
			self.currentDay = persianDate[2]

		# Search for existent registries
		from .configPanel import dirDatabase
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbCursor.execute("select * from periodicity where dataInicial=?", (self.register,))
		occurs = dbCursor.fetchone()
		if occurs!=None:
			self.eventInfo.typeRepeat=occurs[1]
			self.eventInfo.finalDate = occurs[2]
			if self.eventInfo.finalDate < 300000000000:
				endYear = int(self.eventInfo.finalDate/100000000)
				endMonth = int(self.eventInfo.finalDate/1000000)-(endYear*100)
				endDay = int(self.eventInfo.finalDate/10000)-(endYear*10000 + endMonth*100)
				# Change to persian date if necessary
				if calendarToUse == _("Persian"):
					persianDate = persian.from_gregorian(endYear, endMonth, endDay)
					endYear = persianDate[0]
					endMonth = persianDate[1]
					endDay = persianDate[2]

		else:
			self.eventInfo.typeRepeat=-1
			self.eventInfo.finalDate=0
		dbAgenda.close()

		# Translators: Dialog title
		self.SetTitle(_("Set repetitions"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

		# Translators: Group label of ocurrences
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Choose your event repeat:"))
		sizer_3.Add(label_1, 0, 0, 0)

		# Translators: The various ocurrences periods
		self.choice_1 = wx.Choice(self, wx.ID_ANY, choices=frequency)
		if self.eventInfo.typeRepeat>0:
			self.choice_1.SetSelection(self.eventInfo.typeRepeat)
		else:
			self.choice_1.SetSelection(0)
		sizer_3.Add(self.choice_1, 0, 0, 0)

		# Translators: Check box to define if repetitions have a fixed end
		self.checkbox_1 = wx.CheckBox(self, wx.ID_ANY, _("Mark to set when repeat finish"))
		sizer_1.Add(self.checkbox_1, 0, 0, 0)

		sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

		# Translators: Group label to number of repetitions
		label_2 = wx.StaticText(self, wx.ID_ANY, _("Quantity of repeations:"))
		sizer_4.Add(label_2, 0, 0, 0)

		self.spin_ctrl_1 = wx.SpinCtrl(self, wx.ID_ANY, "1", min=0, max=10000)
		sizer_4.Add(self.spin_ctrl_1, 0, 0, 0)

		sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)

		# Translators: Group label to the end date
		label_3 = wx.StaticText(self, wx.ID_ANY, _("End	 date: Day:"))
		sizer_5.Add(label_3, 0, 0, 0)

		self.spin_ctrl_2 = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=31)
		self.spin_ctrl_2.SetValue(int(self.currentDay))
		sizer_5.Add(self.spin_ctrl_2, 0, 0, 0)

		# Translators: Group label to the end date
		label_4 = wx.StaticText(self, wx.ID_ANY, _("Month:"))
		sizer_5.Add(label_4, 0, 0, 0)
		if calendarToUse == _("Gregorian (Default)"):
			self.ComboMonth = wx.ComboBox(self, wx.ID_ANY, choices = months , style=wx.CB_DROPDOWN|wx.CB_READONLY)
		elif calendarToUse == _("Persian"):
			self.ComboMonth = wx.ComboBox(self, wx.ID_ANY, choices = persianMonths , style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.ComboMonth.SetSelection(12-int(self.currentMonth))
		sizer_5.Add(self.ComboMonth, 0, 0, 0)

		# Translators: Group label to the end date
		label_5 = wx.StaticText(self, wx.ID_ANY, _("Year:"))
		sizer_5.Add(label_5, 0, 0, 0)

		self.spin_ctrl_3 = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1300, max=2070)
		self.spin_ctrl_3.SetValue(int(self.currentYear))
		sizer_5.Add(self.spin_ctrl_3, 0, 0, 0)

		self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
		sizer_5.Add(self.text_ctrl_1, 0, 0, 0)

		sizer_1.Add((0, 0), 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK, "")
		self.button_OK.SetDefault()
		sizer_2.AddButton(self.button_OK)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
		sizer_2.AddButton(self.button_CANCEL)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Layout()
		self.CentreOnScreen()

		self.Bind(wx.EVT_SPINCTRL, self.onChangedQuantity, self.spin_ctrl_1)
		self.Bind(wx.EVT_CHOICE, self.onChangedChoice, self.choice_1)
		self.Bind(wx.EVT_SPINCTRL, self.onChangedDate, self.spin_ctrl_2)
		self.Bind(wx.EVT_SPINCTRL, self.onChangedDate, self.spin_ctrl_3)
		self.Bind(wx.EVT_COMBOBOX, self.onChangedDate, self.ComboMonth)
		self.Bind(wx.EVT_CHECKBOX, self.onCheckboxUpdate, self.checkbox_1)
		self.Bind(wx.EVT_BUTTON, self.onOk, self.button_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, self.button_CANCEL)

		# Disable ocorrencies and final date of events
		# if final date is defined 
		if self.eventInfo.finalDate>0 and self.eventInfo.finalDate	<300000000000:
			self.checkbox_1.SetValue(True)
			self.spin_ctrl_2.SetValue(endDay)
			self.ComboMonth.SetSelection(12-int(endMonth))
			self.spin_ctrl_3.SetValue(endYear)
		else:
			self.checkbox_1.SetValue(False)
			# If some repeat choice was  selected
			if self.eventInfo.typeRepeat>0:
				self.checkbox_1.Show()
			else:
				self.checkbox_1.Hide()
				self.spin_ctrl_1.Hide()
				self.spin_ctrl_2.Hide()
				self.ComboMonth.Hide()
				self.spin_ctrl_3.Hide()
				self.text_ctrl_1.Hide()

		# Store the previous date to check what was changed
		self.previousDay = self.currentDay
		self.previousMonth = self.currentMonth
		self.previousYear = self.currentYear
		self.onChangedDate(self)

	def onChangedDate (self, event):
		from . varsConfig import months, persianMonths, weekDays, maxDayMonth
		from .configPanel import calendarToUse
		# Gets the date fields to make the search
		yearToSearch = str(self.spin_ctrl_3.GetValue())
		monthToSearchStr = self.ComboMonth.GetValue()
		if calendarToUse == _("Gregorian (Default)"):
			if monthToSearchStr in months:
				monthToSearch = '%02d' % (12-months.index(monthToSearchStr))
			elif monthToSearchStr in persianMonths:
				monthToSearch = '%02d' % (12 - persianMonths.index(monthToSearchStr))
		elif calendarToUse == _("Persian"):
			if monthToSearchStr in persianMonths:
				monthToSearch = '%02d' % (12 - persianMonths.index(monthToSearchStr))
			elif monthToSearchStr in months:
				monthToSearch = '%02d' % (12-months.index(monthToSearchStr))
		# Gets the maximum days of the month
		year = int(yearToSearch)
		month = int(monthToSearch)
		dayMax = maxDayMonth(year, month)
		self.spin_ctrl_2.SetRange(1, dayMax)

		endYear = str(self.spin_ctrl_3.GetValue())
		monthToSearchStr = self.ComboMonth.GetValue()
		if calendarToUse == _("Gregorian (Default)"):
			endMonth = '%02d' % (12-months.index(monthToSearchStr))
		else:
			endMonth = '%02d' % (12-persianMonths.index(monthToSearchStr))
		endDay = str(self.spin_ctrl_2.GetValue())
		endDate = datetime.datetime.strptime(endDay+'/'+endMonth+'/'+endYear, '%d/%m/%Y').date()
		# Gets the week day
		currentWeek = weekDays[datetime.date (int(endYear), int(endMonth), int(endDay)).weekday()]
		if str(endDate).startswith("14"):
			Date = str(endDate).split("-")
			gregorianDate = persian.to_gregorian(int(Date[0]), int(Date[1]), int(Date[2]))
			endDate = datetime.datetime.strptime(str("%02d" % (gregorianDate[2])) +'/'+ str("%02d" % (gregorianDate[1])) +'/'+ str(gregorianDate[0]), '%d/%m/%Y').date()

			# Gets the week day
			currentWeek = weekDays[datetime.date (int(endYear), int(endMonth), int(endDay)+1).weekday()]
		# Update the weekDay field
		self.text_ctrl_1.SetValue(currentWeek)

		yearStr = str(self.currentYear)
		monthStr = '%02d' % self.currentMonth
		dayStr = '%02d' % self.currentDay
		startDate = datetime.datetime.strptime(dayStr+'/'+monthStr+'/'+yearStr, '%d/%m/%Y').date()
		if str(startDate).startswith("14"):  
			Date = str(startDate).split("-")
			gregorianDate = persian.to_gregorian(int(Date[0]), int(Date[1]), int(Date[2]))
			startDate = datetime.datetime.strptime(str("%02d" % (gregorianDate[2])) +'/'+ str("%02d" % (gregorianDate[1])) +'/'+ str(gregorianDate[0]), '%d/%m/%Y').date()

		if endDate<startDate:
			dlg = wx.MessageDialog(None, _("Your final date is oldest your inicial date."), _("Incorrect date interval"), wx.OK).ShowModal()
		else:
			# Calculate occurrences
			typeRepeat = self.choice_1.GetSelection()
			diffDate1 = abs((endDate-startDate).days)
			occurs = 0
			if typeRepeat==1:
				occurs=diffDate1
			elif typeRepeat==2 or typeRepeat==3:
				occurs = int(diffDate1/(7*(typeRepeat-1)))
			elif typeRepeat>3:
				# Calculate difference between both dates in months
				monthQtt = (int(endMonth)-int(monthStr)) if int(endYear)==int(yearStr) else ((int(endYear)-int(yearStr)-1)*12+(12-int(monthStr))+int(endMonth))
				if typeRepeat<8:
					occurs = int(monthQtt/(typeRepeat-3))
				elif typeRepeat==8:
					occurs = int(monthQtt/6)
				else:
					occurs = int(monthQtt/12)
			self.spin_ctrl_1.SetValue(occurs)

	def onChangedQuantity(self, event):
		from . varsConfig import months, persianMonths, weekDays
		from .configPanel import calendarToUse
		typeRepeat = self.choice_1.GetSelection()
		day = int(self.currentDay)
		month = int(self.currentMonth)
		year = int(self.currentYear)
		occurs = self.spin_ctrl_1.GetValue()

		if typeRepeat>3:
			if typeRepeat<8:
				yearAdd = ((typeRepeat-3)*occurs+month)/12.1 if ((typeRepeat-3)*occurs+month)>12 else 0
				monthQtt = ((typeRepeat-3)*occurs+month)%12 if yearAdd>0 else ((typeRepeat-3)*occurs+month)
				# If yearAdd  > 0 monthQtt will be 0 when occurrences+month will be a multiple of 12 (like occurs = 17 and month = 7), so:
				monthQtt = monthQtt if monthQtt > 0 else 12
			elif typeRepeat==8:
				yearAdd = (6*occurs+month)/12.1 if (6*occurs+month)>12 else 0
				monthQtt = (6*occurs+month)%12 if yearAdd>0 else (6*occurs+month)
				# If yearAdd  > 0 monthQtt will be 0 when occurrences+month will be a multiple of 12 (like occurs = 17 and month = 7), so:
				monthQtt = monthQtt if monthQtt > 0 else 12
			elif typeRepeat==9:
				monthQtt = month
				yearAdd = occurs
			# set combo month and spin year based on occurs value
			if calendarToUse == _("Gregorian (Default)"):
				self.ComboMonth.SetValue(months[12-monthQtt])
			elif calendarToUse == _("Persian"):
				self.ComboMonth.SetValue(persianMonths[12 - monthQtt])
			self.spin_ctrl_3.SetValue(year+yearAdd)
			if "." in str(year+yearAdd):
				yearStr = str(year+yearAdd).split(".")[0]
			else:
				yearStr = str(year+yearAdd)
			monthStr = str(12-months.index(self.ComboMonth.GetValue()))
			dayStr = '%02d' % self.currentDay
			finalDate = datetime.datetime.strptime(dayStr+'/'+monthStr+'/'+yearStr, '%d/%m/%Y').date()
			finalDateStr = str(finalDate)
		elif typeRepeat>0 and typeRepeat<4:
			yearStr = str(self.currentYear)
			monthStr = '%02d' % self.currentMonth
			dayStr = '%02d' % self.currentDay
			initialDate = datetime.datetime.strptime(dayStr+'/'+monthStr+'/'+yearStr, '%d/%m/%Y').date()
			if typeRepeat==1:
				finalDate = initialDate + datetime.timedelta(days=+occurs)
			elif typeRepeat==2:
				finalDate = initialDate + datetime.timedelta(days=+(occurs*7))
			else:
				finalDate = initialDate + datetime.timedelta(days=+(occurs*14))
			finalDateStr = str(finalDate)
			self.spin_ctrl_2.SetValue(int(finalDateStr[8:10]))
			if calendarToUse == _("Gregorian (Default)"):
				self.ComboMonth.SetValue(months[12-int(finalDateStr[5:7])])
			elif calendarToUse == _("Persian"):
				self.ComboMonth.SetValue(persianMonths[12-int(finalDateStr[5:7])])
			self.spin_ctrl_3.SetValue(int(finalDateStr[0:4]))
		# Gets the week day
		if int(finalDateStr[:4]) < 1500:
			currentWeek = weekDays[datetime.date (int(finalDateStr[:4]), int(finalDateStr[5:7]), int(finalDateStr[8:10])+1).weekday()]
		else:
			currentWeek = weekDays[datetime.date (int(finalDateStr[:4]), int(finalDateStr[5:7]), int(finalDateStr[8:10])).weekday()]
		# Update the weekDay field
		self.text_ctrl_1.SetValue(currentWeek)
		# Change persian date to gregorian date
		Date = str(initialDate).split("-")
		gregorianDate = persian.to_gregorian(int(Date[0]), int(Date[1]), int(Date[2]))
		initialDate = datetime.datetime.strptime(str("%02d" % (gregorianDate[2])) +'/'+ str("%02d" % (gregorianDate[1])) +'/'+ str(gregorianDate[0]), '%d/%m/%Y').date()
		Date = str(finalDate).split("-")
		gregorianDate = persian.to_gregorian(int(Date[0]), int(Date[1]), int(Date[2]))
		finalDate = datetime.datetime.strptime(str("%02d" % (gregorianDate[2])) +'/'+ str("%02d" % (gregorianDate[1])) +'/'+ str(gregorianDate[0]), '%d/%m/%Y').date()

	def onChangedChoice (self, event):
		if  self.choice_1.GetSelection()>0:
			self.checkbox_1.Show()
		else:
			self.checkbox_1.SetValue(False)
			self.checkbox_1.Hide()
			self.spin_ctrl_1.Hide()
			self.spin_ctrl_2.Hide()
			self.ComboMonth.Hide()
			self.spin_ctrl_3.Hide()
			self.text_ctrl_1.Hide()

	def onCheckboxUpdate (self, event):
		flagChecked = self.checkbox_1.GetValue()
		if flagChecked:
			self.spin_ctrl_1.Show()
			self.spin_ctrl_2.Show()
			self.ComboMonth.Show()
			self.spin_ctrl_3.Show()
			self.text_ctrl_1.Show()
		else:
			self.spin_ctrl_1.Hide()
			self.spin_ctrl_2.Hide()
			self.ComboMonth.Hide()
			self.spin_ctrl_3.Hide()
			self.text_ctrl_1.Hide()

	def onOk (self,event):
		from . varsConfig import months, persianMonths, weekDays
		from .configPanel import calendarToUse
		checkEternal = self.checkbox_1.GetValue()
		self.eventInfo.typeRepeat = self.choice_1.GetSelection()
		if checkEternal:
			year = str(self.spin_ctrl_3.GetValue())
			monthToSearchStr = self.ComboMonth.GetValue()
			if calendarToUse == _("Gregorian (Default)"):
				month = '%02d' % (12-months.index(monthToSearchStr))
			elif calendarToUse == _("Persian"):
				month = '%02d' % (12 - persianMonths.index(monthToSearchStr))
			day  = '%02d' % self.spin_ctrl_2.GetValue()
			hour = '%02d' % (int((self.register%10000)/100))
			minutes = '%02d' % (int(self.register%100))
			self.eventInfo.finalDate = int(year+month+day+hour+minutes)
			if self.eventInfo.finalDate < 150000000000:
				gregorianDate = persian.to_gregorian(int(year), int(month), int(day))
				self.currentYear1 = str(gregorianDate[0])
				self.currentMonth1 = str("%02d" % gregorianDate[1])
				self.currentDay1 = str("%02d" % gregorianDate[2])
				self.hour = str(self.register)[8:]
				self.eventInfo.finalDate = int(self.currentYear1 + self.currentMonth1 + self.currentDay1 + self.hour)

		else:
			self.eventInfo.finalDate = 300000000000
		event.Skip()

	def onCancel (self, event):
		event.Skip()
