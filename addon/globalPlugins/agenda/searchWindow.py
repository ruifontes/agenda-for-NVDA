# -*- coding: UTF-8 -*-
# Agenda add-on: Module responsible for search window and all possible operations on it.
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# Copyright (C) 2022-2023 Abel Passos Jr. and Rui Fontes
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
from .logDebug import logDebug
from .varsConfig import *
from .manageDatabase import *
from .configPanel import *
from .DlgAddEdit import DlgAddEdit
from .alarmsCheck import CheckAlarms

# Tostart the translation process
addonHandler.initTranslation()


class searchWindow(wx.Dialog):
	global dirDatabase
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Title of search window
		self.SetTitle(_("Agenda search"))

		self.lastSearch = ''
		self.dayOfToday = ""
		self.dayOfTomorrow= ""
		self.flagRecordExists = False
		self.now = str(datetime.datetime.now())
		self.currentYear = self.now[:4]
		self.currentMonth = self.now[5:7]
		self.currentDay = self.now[8:10]

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# Translators: The search type
		self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Type of search:"))
		sizer_1.Add(self.label_1, 0, 0, 0)

		# Translators: The various search types
		self.comboSearchType = wx.ComboBox(self, wx.ID_ANY, choices=[_("Search by text"), _("Next 7 days"), _("Next 30 days"), _("Date range")], style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.comboSearchType.SetSelection(0)
		sizer_1.Add(self.comboSearchType, 0, 0, 0)

		# Translators: Asking user to enter the text to search
		self.label_2 = wx.StaticText(self, wx.ID_ANY, _("Enter the text to search:"))
		sizer_1.Add(self.label_2, 0, 0, 0)

		self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
		sizer_1.Add(self.text_ctrl_1, 0, 0, 0)

		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

		# Translators: Day of initial date
		self.label_3 = wx.StaticText(self, wx.ID_ANY, _("Initial date: Day:"))
		sizer_3.Add(self.label_3, 0, 0, 0)

		self.spinInitialDay = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=31)
		self.spinInitialDay.SetValue(int(self.currentDay))
		sizer_3.Add(self.spinInitialDay, 0, 0, 0)

		# Translators: month of initial date
		self.label_4 = wx.StaticText(self, wx.ID_ANY, _("Month:"))
		sizer_3.Add(self.label_4, 0, 0, 0)

		self.ComboInitialMonth = wx.ComboBox(self, wx.ID_ANY, choices = months, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.ComboInitialMonth.SetSelection(12-int(self.currentMonth))
		sizer_3.Add(self.ComboInitialMonth, 0, 0, 0)

		# Translators: Year of initial date
		self.label_5 = wx.StaticText(self, wx.ID_ANY, _("Year:"))
		sizer_3.Add(self.label_5, 0, 0, 0)

		self.spinInitialYear = wx.SpinCtrl(self, wx.ID_ANY, "1970", min=1970, max=2050)
		self.spinInitialYear.SetValue(int(self.currentYear))
		sizer_3.Add(self.spinInitialYear, 0, 0, 0)

		sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

		# Translators: Day of final date
		self.label_6 = wx.StaticText(self, wx.ID_ANY, _("Final date: Day:"))
		sizer_4.Add(self.label_6, 0, 0, 0)

		self.spinFinalDay = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=31)
		self.spinFinalDay.SetValue(int(self.currentDay))
		sizer_4.Add(self.spinFinalDay, 0, 0, 0)

		# Translators: Month of final date
		self.label_7 = wx.StaticText(self, wx.ID_ANY, _("Month:"))
		sizer_4.Add(self.label_7, 0, 0, 0)

		self.ComboFinalMonth = wx.ComboBox(self, wx.ID_ANY, choices = months, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.ComboFinalMonth.SetSelection(12-int(self.currentMonth))
		sizer_4.Add(self.ComboFinalMonth, 0, 0, 0)

		# Translators: Year of final date
		self.label_8 = wx.StaticText(self, wx.ID_ANY, _("Year:"))
		sizer_4.Add(self.label_8, 0, 0, 0)

		self.spinFinalYear = wx.SpinCtrl(self, wx.ID_ANY, "1970", min=1970, max=2050)
		self.spinFinalYear.SetValue(int(self.currentYear))
		sizer_4.Add(self.spinFinalYear, 0, 0, 0)

		# Translators: Label of button to execute the search
		self.button_1 = wx.Button(self, wx.ID_ANY, _("&Search"))
		self.button_1.SetDefault()
		sizer_1.Add(self.button_1, 0, 0, 0)

		# Translators: Label of the list were the itens found will land
		self.label_9 = wx.StaticText(self, wx.ID_ANY, _("Items found:"))
		sizer_1.Add(self.label_9, 0, 0, 0)

		self.currentItemsList = wx.ListCtrl(self, wx.ID_ANY, size = (500, 200), style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.currentItemsList.AppendColumn(_("Date/Hour"), format=wx.LIST_FORMAT_LEFT, width = -1)
		self.currentItemsList.AppendColumn("Compromisso:", format=wx.LIST_FORMAT_LEFT, width = -1)
		self.flagRecordExists = False
		sizer_1.Add(self.currentItemsList, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		# 
		# Translators: Add button label
		self.ButtonAdd = wx.Button(self, wx.ID_ANY, _("&Add"))
		sizer_2.Add(self.ButtonAdd, 0, 0, 0)

		# Translators: Edit button label
		self.ButtonEdit = wx.Button(self, wx.ID_ANY, _("&Edit"))
		sizer_2.Add(self.ButtonEdit, 0, 0, 0)

		# Translators: Remove button label
		self.ButtonRemove = wx.Button(self, wx.ID_ANY, _("&Remove"))
		sizer_2.Add(self.ButtonRemove, 0, 0, 0)

		# Translators: Label of button to remove all appointments
		self.ButtonDeleteAll = wx.Button(self, wx.ID_ANY, _("Remove A&ll"))
		sizer_2.Add(self.ButtonDeleteAll, 0, 0, 0)

		self.ButtonCancel = wx.Button(self, wx.ID_ANY, _("&Cancel"))
		sizer_2.Add(self.ButtonCancel, 0, 0, 0)

		# Adding an ID for each keystroke event
		self.Delete = wx.Window.NewControlId()
		# Assigns to each keystroke ID a method to the associated event
		self.Bind(wx.EVT_MENU, self.executeRemove, id=self.Delete)
		# Assigns the keystrokes to the ID's
		accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_DELETE, self.Delete)])
		self.SetAcceleratorTable(accel_tbl)

		sizer_2.Realize()

		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.Layout()
		self.CentreOnScreen()

		self.Bind(wx.EVT_BUTTON, self.executeSearch, self.button_1)
		self.Bind(wx.EVT_BUTTON, self.OnAddSearch, self.ButtonAdd)
		self.Bind(wx.EVT_BUTTON, self.executeEdit, self.ButtonEdit)
		self.Bind(wx.EVT_BUTTON, self.executeRemove, self.ButtonRemove)
		self.Bind(wx.EVT_BUTTON, self.onDeleteAll, self.ButtonDeleteAll)
		self.Bind(wx.EVT_BUTTON, self.OnCancel2, self.ButtonCancel)
		self.Bind(wx.EVT_COMBOBOX, self.onSearchChange, self.comboSearchType)
		self.Bind(wx.EVT_SPINCTRL, self.onDateRangeChange, self.spinInitialYear)
		self.Bind(wx.EVT_SPINCTRL, self.onDateRangeChange, self.spinInitialDay)
		self.Bind(wx.EVT_COMBOBOX, self.onDateRangeChange, self.ComboInitialMonth)
		self.Bind(wx.EVT_SPINCTRL, self.onDateRangeChange, self.spinFinalYear)
		self.Bind(wx.EVT_SPINCTRL, self.onDateRangeChange, self.spinFinalDay)
		self.Bind(wx.EVT_COMBOBOX, self.onDateRangeChange, self.ComboFinalMonth)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.executeEdit, self.currentItemsList)

		self.SetEscapeId(self.ButtonCancel.GetId())


		# Hide all fields untill user choose type of search. Exception for the preselected type, text...
		self.label_3.Hide()
		self.spinInitialDay.Hide()
		self.label_4.Hide()
		self.ComboInitialMonth.Hide()
		self.label_5.Hide()
		self.spinInitialYear.Hide()
		self.label_6.Hide()
		self.spinFinalDay.Hide()
		self.label_7.Hide()
		self.ComboFinalMonth.Hide()
		self.label_8.Hide()
		self.spinFinalYear.Hide()
		self.periodicityRegisters = None

	def onDateRangeChange(self, event):
		# Adjusts the date fields to be valids one
		# Adjust initial date fields
		monthToSearchStr = self.ComboInitialMonth.GetValue()
		# Gets the maximum days of the month
		month = 12-months.index(monthToSearchStr)
		year = self.spinInitialYear.GetValue()
		dayMax = maxDayMonth(year, month)

		self.spinInitialDay.SetRange(1, dayMax)

		# Adjust final date fields
		monthToSearchStr = self.ComboFinalMonth.GetValue()
		# Gets the maximum days of the month
		year = self.spinInitialYear.GetValue()
		month = 12-months.index(monthToSearchStr)
		dayMax = maxDayMonth(year, month)

		self.spinFinalDay.SetRange(1, dayMax)

	def onSearchChange(self, event):
		# Show or hide the fields according to search type
		SearchType = self.comboSearchType.GetValue()
		if SearchType == _("Search by text"):
			# Enable fields to Search by text
			self.label_2.Show()
			self.text_ctrl_1.Show()
			# Disable fields to search by Date range
			self.label_3.Hide()
			self.spinInitialDay.Hide()
			self.label_4.Hide()
			self.ComboInitialMonth.Hide()
			self.label_5.Hide()
			self.spinInitialYear.Hide()
			self.label_6.Hide()
			self.spinFinalDay.Hide()
			self.label_7.Hide()
			self.ComboFinalMonth.Hide()
			self.label_8.Hide()
			self.spinFinalYear.Hide()
		if SearchType == _("Next 7 days") or SearchType == _("Next 30 days"):
			# Disable fields to Search by text
			self.label_2.Hide()
			self.text_ctrl_1.Hide()
			# Disable fields to search by Date range
			self.label_3.Hide()
			self.spinInitialDay.Hide()
			self.label_4.Hide()
			self.ComboInitialMonth.Hide()
			self.label_5.Hide()
			self.spinInitialYear.Hide()
			self.label_6.Hide()
			self.spinFinalDay.Hide()
			self.label_7.Hide()
			self.ComboFinalMonth.Hide()
			self.label_8.Hide()
			self.spinFinalYear.Hide()
		if SearchType == _("Date range"):
			# Disable fields to Search by text
			self.label_2.Hide()
			self.text_ctrl_1.Hide()
			# Enable fields to search by Date range
			self.label_3.Show()
			self.spinInitialDay.Show()
			self.label_4.Show()
			self.ComboInitialMonth.Show()
			self.label_5.Show()
			self.spinInitialYear.Show()
			self.label_6.Show()
			self.spinFinalDay.Show()
			self.label_7.Show()
			self.ComboFinalMonth.Show()
			self.label_8.Show()
			self.spinFinalYear.Show()

	def executeSearch(self, event): 
		global dateToSearch 
		self.lastSearch = ""
		now = datetime.datetime.now() 

		flagquery = 0 
		self.SearchType = self.comboSearchType.GetValue() 
		self.periodicityRegisters = None 
		startDate = None 
		finalDate = None 
		if self.SearchType == _("Search by text"): 
			textToSearch = self.text_ctrl_1.GetValue() 
			if len(textToSearch) == 0: 
				# Translators: If the text to search is empty notifies the user 
				dlg = wx.MessageDialog( self, _("Insert what to search or choose another type of search."), _("Agenda"), wx.OK) 
				dlg.ShowModal() 
				dlg.Destroy() 
				return 
			else: 
				flagquery = 1 
				textToSearch_upper = textToSearch.upper()
				# What to search in database
				what = "*" 
				find = " upcase(descricao) like '%"+textToSearch_upper+"%' order by data asc"
				self.lastSearch = "upcase(descricao) like '%"+textToSearch_upper+"%'"
		elif self.SearchType==_("Next 7 days"): 
			# Search on the Next 7 days 
			flagquery = 1 
			nextDays = now + datetime.timedelta(days=+8) 
			startDay = now + datetime.timedelta(days=+1) 
			startDate = int(startDay.strftime ('%Y%m%d') + '0000') 
			finalDate  = int(nextDays.strftime ('%Y%m%d') + '2359') 
			# What to search in database
			what = "*" 
			find = "data>= " + str(startDate) + " and data<= " + str(finalDate) + " order by data asc" 
			self.lastSearch = 'data>='+str(startDate)+' and data<='+str(finalDate)
		elif self.SearchType==_("Next 30 days"): 
			# Search on the Next 30 days 
			flagquery = 1 
			nextDays = now + datetime.timedelta(days=+31) 
			startDay = now + datetime.timedelta(days=+1) 
			startDate = int(startDay.strftime ('%Y%m%d') + '0000') 
			finalDate  = int(nextDays.strftime ('%Y%m%d') + '2359') 
			# What to search in database
			what = "*" 
			find = "data>= " + str(startDate) + " and data<= " + str(finalDate) + " order by data asc" 
			self.lastSearch='data>='+str(startDate)+' and data<='+str(finalDate) 
		elif self.SearchType == _("Date range"): 
			flagquery = 1 
			# Gets the date fields to make the search 
			startYearToSearch = str(self.spinInitialYear.GetValue()) 
			monthToSearchStr = self.ComboInitialMonth.GetValue() 
			startMonthToSearch = '%02d' % (12-months.index(monthToSearchStr)) 
			startDayToSearch = '%02d' % self.spinInitialDay.GetValue() 
			startDate = int(startYearToSearch + startMonthToSearch + startDayToSearch + "0000") 

			finalYearToSearch = str(self.spinFinalYear.GetValue()) 
			monthToSearchStr = self.ComboFinalMonth.GetValue() 
			finalMonthToSearch = '%02d' % (12-months.index(monthToSearchStr)) 
			finalDayToSearch = '%02d' % self.spinFinalDay.GetValue() 
			finalDate = int(finalYearToSearch + finalMonthToSearch + finalDayToSearch + "2359") 

			if finalDate<startDate: 
				dlg = wx.MessageDialog( self, _("The end date must be equal or after the start date."), _("Agenda"), wx.OK) 
				dlg.ShowModal() 
				dlg.Destroy() 
				return 

			# What to search in database
			what = "*" 
			find = "data>= " + str(startDate) + " and data<= " + str(finalDate) + " order by data asc" 
			self.lastSearch = "data>=" +str(startDate) + " and data<=" + str(finalDate) 

		if flagquery==1:
			# Case some query was started loads from database 
			from .configPanel import dirDatabase 
			occurs = manageDatabase.findItem(what, find, dirDatabase, all=True) 

		# Clear the listbox 
		self.currentItemsList.ClearAll() 
		self.currentItemsList.AppendColumn(_("Date/Hour"), format=wx.LIST_FORMAT_LEFT, width = 100) 
		self.currentItemsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width = 400) 
		loadedItens = [] 
		self.dayOfToday = "" 
		self.dayOfTomorrow = "" 
		self.flagRecordExists=False 
		now = datetime.datetime.now() 
		tomorrow = now + datetime.timedelta(days=+1) 
		self.dayOfToday = datetime.datetime.strftime(now, '%Y%m%d') 
		self.dayOfTomorrow = datetime.datetime.strftime(tomorrow, '%Y%m%d') 
		if len(occurs) != 0: 
			self.flagRecordExists=True 
			# Items were found, so fill the listbox with them 
			dbAgenda = sqlite3.connect(dirDatabase) 
			dbCursor = dbAgenda.cursor() 
			for tableLine in occurs: 
				# check for periodic event to this appointement 
				checkRepeat = _("No repeat") 
				readDate = str(tableLine[0]) 
				textToShow = "" 
				if readDate[:8] == self.dayOfToday: 
					textToShow = _("Today") 
				elif readDate[:8] == self.dayOfTomorrow: 
					textToShow = _("Tomorrow") 
				else: 
					weekToShow = weekDays[datetime.date (int(readDate[:4]),int(readDate[4:6]),int(readDate[6:8])) .weekday()] 
					textToShow = weekToShow + ", " + readDate[6:8] + "/" + readDate[4:6] + "/" + readDate[:4] 
				dbCursor.execute(""" 
					select tipo 
					from periodicity 
					where dataInicial=? 
				""", (tableLine[0],)) 
				foundRepeat = dbCursor.fetchone() 
				if foundRepeat!=None: 
					checkRepeat = frequency[foundRepeat[0]] 
					if self.SearchType == _("Search by text"): 
						loadedItens += [[tableLine[0], textToShow + ", " + readDate[8:10] + ":" + readDate[10:12]+', ', checkRepeat + "; " + tableLine[2]]] 
					else: 
						loadedItens += [[tableLine[0], textToShow + ", " + readDate[8:10] + ":" + readDate[10:12], tableLine[2]]] 
				else: 
						loadedItens += [[tableLine[0], textToShow + ", " + readDate[8:10] + ":" + readDate[10:12], tableLine[2]]] 

		if startDate!=None: 
			self.periodicityRegisters = manageDatabase.findRepeatIntervalDate(startDate, finalDate, True, dirDatabase) 
			# logDebug('Quantidade de registros periódicos encontrados: {0}'.format(len(self.periodicityRegisters)))
			if len(self.periodicityRegisters)>0: 
				self.flagRecordExists=True 
				for tableLine in self.periodicityRegisters: 
					readDate = str(tableLine[1]) 
					sd = readDate
					dateToExame = datetime.datetime.strptime(sd[6:8]+'/'+sd[4:6]+'/'+sd[:4]+' '+sd[8:10]+':'+sd[10:12], '%d/%m/%Y %H:%M')
					# # logDebug('Data a adicionar: {0}'.format(dateToExame))

					textToShow = "" 
					if readDate[:8] == self.dayOfToday: 
						textToShow = _("Today") 
					elif readDate[:8] == self.dayOfTomorrow: 
						textToShow = _("Tomorrow") 
					else: 
						# # logDebug('Data a buscar o dia da semana: {0}'.format(readDate))
						weekToShow = weekDays[datetime.date (int(readDate[:4]),int(readDate[4:6]),int(readDate[6:8])).weekday()] 
						textToShow = weekToShow + ", " + readDate[6:8] + "/" + readDate[4:6] + "/" + readDate[:4] 
					loadedItens += [[tableLine[1], textToShow + ", " + readDate[8:10] + ":" + readDate[10:12] + ', ', frequency[tableLine[10]] + "; " + tableLine[3]]] 

		if not self.flagRecordExists: 
			self.lastSearch = "" 
			self.label_9.SetLabel(_("No items found:")) 
		else: 
			# If It found registers, fill  into  listctrl 
			loadedSorted = sorted(loadedItens) 
			j = 0 
			for x in loadedSorted: 
				index = self.currentItemsList.InsertItem(j, x[1]) 
				self.currentItemsList.SetItem(index, 1,x[2]) 
				j+=1 
		self.label_9.SetLabel(str(self.currentItemsList.GetItemCount()) + _("Items found:")) 
		self.currentItemsList.SetFocus() 
		self.currentItemsList.Focus(0) 
		self.currentItemsList.Select(0) 

	def OnAddSearch(self, event):
		generalVars.titleAddEd = _("Add")
		# The variable should contain the details of appointment to add
		if self.flagRecordExists:
			# Get appointment details to make the date to add
			strItemToEdit = self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 0)
			dateToEdit = ""
			if strItemToEdit.startswith(_("Today")):
				dateToEdit = self.dayOfToday
				hour = strItemToEdit[6:8] + strItemToEdit[9:11]
			elif strItemToEdit.startswith(_("Tomorrow")):
				dateToEdit=self.dayOfTomorrow
				hour = strItemToEdit[8:10] + strItemToEdit[11:13]
			else:
				strItemToEdit = strItemToEdit.split(", ")[1]
				dateToEdit = strItemToEdit[6:10] + strItemToEdit[3:5] + strItemToEdit[:2]
				hour = strItemToEdit[12:14] + strItemToEdit[15:17]

		else:
			now = datetime.datetime.now()
			self.dayOfToday = datetime.datetime.strftime(now, '%Y%m%d')
			dateToEdit = datetime.datetime.strftime(now, '%Y%m%d')
			hour = datetime.datetime.strftime(now, '%H%M')

		generalVars.itemToEdit = int(dateToEdit + hour)
		dialogAdd = DlgAddEdit(generalVars, self)
		dialogAdd.ShowModal()
		dialogAdd.Destroy()
		self.executeSearch(event)
		event.Skip()

	def executeEdit(self, event):
		global itemToEdit
		generalVars.titleAddEd = _("Edit")
		flagGoToEdit = False
		# The variable should contain the details of appointment to edit
		if self.flagRecordExists and self.currentItemsList.GetSelectedItemCount() != 0:
			# Get appointment details to make the date to edit
			strItemToEdit = self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 0)
			dateToEdit = ""
			if strItemToEdit.startswith(_("Today")):
				dateToEdit = self.dayOfToday
				hour = strItemToEdit[6:8] + strItemToEdit[9:11]
			elif strItemToEdit.startswith(_("Tomorrow")):
				dateToEdit = self.dayOfTomorrow
				hour = strItemToEdit[8:10] + strItemToEdit[11:13]
			else:
				strItemToEdit = strItemToEdit.split(", ")[1] + ", " + strItemToEdit.split(", ")[2]
				dateToEdit = strItemToEdit[6:10] + strItemToEdit[3:5]+strItemToEdit[:2]
				hour = strItemToEdit[12:14] + strItemToEdit[15:17]

			generalVars.itemToEdit = int(dateToEdit + hour)
			flagGoToEdit = True
			if self.SearchType != _("Search by text"):
				for foundRepeatRegister  in self.periodicityRegisters:
					if foundRepeatRegister[1] == generalVars.itemToEdit:
						dlg = wx.MessageDialog(self, _("You selected a periodic event. You can't edit a date inside on periodic event.\nInstead of, you need edit the original register. Do you want edit It?"), _("Edit periodic event"), wx.YES_NO)
						if dlg.ShowModal()==wx.ID_YES:
							generalVars.itemToEdit= foundRepeatRegister[0]
							break
						else:
							flagGoToEdit = False
							break
			else:
					pass

			if flagGoToEdit:
				dlgAdEd = DlgAddEdit(generalVars, self).ShowModal()
		else:
			# Translators: Informing no event selected.
			dlg = wx.MessageDialog(None, _("No appointment selected to edit..."), _("Agenda"), wx.OK)
			dlg.ShowModal() 
			dlg.Destroy()
		self.executeSearch(event)
		event.Skip()
		loadAlarms(0)

	def executeRemove(self, event):
		# The variable should contain the details of appointment to remove
		if self.flagRecordExists and self.currentItemsList.GetSelectedItemCount() > 0:
			# Get appointments fields to create the date
			strItemToRemove = self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 0)
			strItemToRemoveMsg = self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 1)
			dateToRemove = ""
			if strItemToRemove.startswith(_("Today")):
				dateToRemove = self.dayOfToday
				hour = strItemToRemove[6:8]+strItemToRemove[9:11]
			elif strItemToRemove.startswith(_("Tomorrow")):
				dateToRemove=self.dayOfTomorrow
				hour = strItemToRemove[8:10]+strItemToRemove[11:13]
			else:
				strItemToRemove = strItemToRemove.split(", ")[1] + ", " + strItemToRemove.split(", ")[2]
				dateToRemove=strItemToRemove[6:10]+strItemToRemove[3:5]+strItemToRemove[:2]
				hour = strItemToRemove[12:14]+strItemToRemove[15:17]

			itemToRemove= int(dateToRemove + hour)
			# Translators: To confirm remotion of the event
			msgRemove = (_("Do you really want to remove the  item: ") + strItemToRemoveMsg + "?")
			if self.SearchType != _("Search by text"):
				for foundRepeatRegister  in self.periodicityRegisters:
					if foundRepeatRegister[1]==itemToRemove:
						originalDate = str(foundRepeatRegister[0])
						originalDateStr = originalDate[6:8]+'/'+originalDate[4:6]+'/'+originalDate[:4]+', '+originalDate[8:10]+':'+originalDate[10:12]+', '+foundRepeatRegister[3]
						#Translators: Inform that is necessary to remove the original event
						msgRemove = _("You can't remove just one periodic event. Instead of, you need remove the original register. If you make this, alldates on this periodic event will be deleted.\nDo you want to delete the original register and all   dates of this {} event:\n{}?").format(frequency[foundRepeatRegister[10]], originalDateStr)
						itemToRemove= foundRepeatRegister[0]
						break
			# Translators: Asking confirmation to delete
			dlg = wx.MessageDialog(self, msgRemove, _("Remove event"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES: 
				# Conecting to database
				from .configPanel import dirDatabase
				manageDatabase.removeItem(itemToRemove, dirDatabase)
				manageDatabase.removeRepeat(itemToRemove, dirDatabase)
				# Translators: Informing success of remotion
				dlg2 = wx.MessageDialog( self, _("Appointment removed successfully!"), _("Agenda"), wx.OK)
				dlg2.ShowModal()
				dlg2.Destroy()
				self.executeSearch(event)
				loadAlarms(0)
		else:
			# Translators: Informing no event selected.
			dlg = wx.MessageDialog(None, _("No appointment selected to delete"), _("Agenda"), wx.OK)
			dlg.ShowModal() 
			dlg.Destroy()
		event.Skip()

	def onDeleteAll(self, event):
		if self.lastSearch == "":
			# Translators: Informing no event selected.
			dlg = wx.MessageDialog(None, _("No itens to delete. Please, you need search something to delete all itens."), _("Agenda"), wx.OK)
			dlg.ShowModal() 
			dlg.Destroy()
		else:
			# Translators: Confirmation to delete all selected events
			dlg = wx.MessageDialog(self, _("Do you really want to delete all itens found?"), _("Agenda"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES: 
				# Conecting to database
				from .configPanel import dirDatabase
				manageDatabase.removeItem(self.lastSearch, dirDatabase)

				# Translators: Informing success of all events deleted
				dlg2 = wx.MessageDialog( self, _("All appointments deleted successfully!"), _("Agenda"), wx.OK)
				dlg2.ShowModal()
				dlg2.Destroy()
				self.executeSearch(event)
				loadAlarms(0)

	def OnCancel2(self, event):
		self.Close()
		event.Skip()

