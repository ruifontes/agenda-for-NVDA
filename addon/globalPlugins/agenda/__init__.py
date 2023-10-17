# -*- coding: UTF-8 -*-
# Agenda add-on
# Provides an accessible agenda with or without alarms
# Shortcut: NVDA+F4
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# Copyright (C) 2022-2023 Abel Passos Jr. and Rui Fontes
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
import globalPluginHandler
from .manageDatabase import *
from .configPanel import *
from .varsConfig import *
from .DlgAddEdit import DlgAddEdit
from .alarmsCheck import CheckAlarms
from .searchWindow import searchWindow
from . nextAppointments import nextAppointments
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__))))
from . import convertdate
from .convertdate import persian
from . import pymeeus
import ui
import threading
from scriptHandler import script

# To start translation
addonHandler.initTranslation()

initConfiguration()

def avoidSecure():
	# Avoid use in secure screens and during installation
	if (globalVars.appArgs.secure or globalVars.appArgs.install or globalVars.appArgs.minimal):
		return


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		# Call of the constructor of the parent class.
		super(globalPluginHandler.GlobalPlugin, self).__init__()

		# Translators: Dialog title
		title = _("Agenda")

		# Adding a NVDA configurations section
		gui.NVDASettingsDialog.categoryClasses.append(AgendaSettingsPanel)

		# Check for database file
		from .configPanel import dirDatabase
		if not os.path.exists(dirDatabase):
			# Does not exist, so creat it
			manageDatabase.createDatabase(dirDatabase)

		# checks for the existence of the periodicity table
		manageDatabase.increasePeriodicity(dirDatabase)

		# Decide if appointments for today and tomorrow are shown
		if not (globalVars.appArgs.install and globalVars.appArgs.minimal):
			if config.conf["agenda"]["show"]:
				# Is shown is set, so display the next appointments
				allow = 1
			else:
				allow = 0
			# Load next alarms and start alarm threading
			loadAlarms(allow)
			t = None
			t = threading.Thread(target = varsConfig.threadAlarm)
			t.setDaemon(True)
			t.start()

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		try:
			NVDASettingsDialog.categoryClasses.remove(AgendaSettingsPanel)
		except Exception:
			pass
		sys.path.remove(sys.path[-1])

	#defining a script with decorator:
	@script(
		gesture="kb:NVDA+f4",
		# Translators: Message to be announced during Keyboard Help	 
		description= _("Main window to access an accessible agenda"),
		# Translators: Name of the section in "Input gestures" dialog.	
		category= _("Agenda"))
	def script_callMainWindow(self, event):
		#Calling the agenda main dialog.
		dialog0 = MainWindow(gui.mainFrame)
		if not dialog0.IsShown():
			gui.mainFrame.prePopup()
			dialog0.Show()
			gui.mainFrame.postPopup()

	#defining a script with decorator:
	@script(
		gesture="kb:NVDA+Shift+f4",
		# Translators: Message to be announced during Keyboard Help	 
		description= _("Calling next appointments dialog"),
		# Translators: Name of the section in "Input gestures" dialog.	
		category= _("Agenda"))
	def script_callNextAppointments(self, event):
		#Calling the agenda next appointments dialog
		dialog1 = nextAppointments(gui.mainFrame)
		if not dialog1.IsShown():
			gui.mainFrame.prePopup()
			dialog1.Show()
			gui.mainFrame.postPopup()


class MainWindow(wx.Dialog):
	global dirDatabase
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)

		# set a identifier to window and check if another window is opened
		self.name = "SingleApp-%s" % wx.GetUserId()
		self.instance = wx.SingleInstanceChecker(self.name)
		if self.instance.IsAnotherRunning():
			# return if another instance of window is running
			return False

		self.flagSetFocus=False

		self.now = str(datetime.datetime.now())
		self.currentYear = self.now[:4]
		self.currentMonth = self.now[5:7]
		self.currentDay = self.now[8:10]
		if calendarToUse == _("Persian"):
			self.now = persian.from_gregorian(int(self.currentYear ), int(self.currentMonth ), int(self.currentDay))
			self.currentYear = self.now[0]
			self.currentMonth = self.now[1]
			self.currentDay = self.now[2]

		self.SetTitle(_("Agenda"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

		# Translators: Field to select the day
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Day:"))
		sizer_3.Add(label_1, 0, 0, 0)
		self.spinDay = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=31)
		self.spinDay.SetValue(int(self.currentDay))
		sizer_3.Add(self.spinDay, 0, 0, 0)

		# Translators: Field to select the month
		label_2 = wx.StaticText(self, wx.ID_ANY, _("Month:"))
		sizer_3.Add(label_2, 0, 0, 0)
		if calendarToUse == _("Gregorian (Default)"):
			self.ComboMonth = wx.ComboBox(self, wx.ID_ANY, choices = months , style=wx.CB_DROPDOWN|wx.CB_READONLY)
		elif calendarToUse == _("Persian"):
			self.ComboMonth = wx.ComboBox(self, wx.ID_ANY, choices = persianMonths , style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.ComboMonth.SetSelection(12-int(self.currentMonth))
		sizer_3.Add(self.ComboMonth, 0, 0, 0)

		# Translators: Field to select the year
		label_3 = wx.StaticText(self, wx.ID_ANY, _("Year:"))
		sizer_3.Add(label_3, 0, 0, 0)
		self.spinYear = wx.SpinCtrl(self, wx.ID_ANY, "1300", min=1300, max=2050)
		self.spinYear.SetValue(int(self.currentYear))
		sizer_3.Add(self.spinYear, 0, 0, 0)

		self.weekDay = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
		sizer_3.Add(self.weekDay, 0, 0, 0)

		# Translators: Name of the list with the events
		self.label_4 = wx.StaticText(self, wx.ID_ANY, _("items found:"))
		sizer_1.Add(self.label_4, 0, 0, 0)

		self.currentItemsList = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES | wx.LC_SORT_ASCENDING)
		self.currentItemsList.AppendColumn(_("Hour"), format=wx.LIST_FORMAT_LEFT, width = -1)
		self.currentItemsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width = -1)
		sizer_1.Add(self.currentItemsList, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		# Translators: Button to add an event
		self.buttonAdd = wx.Button(self, wx.ID_ANY, _("&Add"))
		sizer_2.Add(self.buttonAdd, 0, 0, 0)

		# Translators: Button to edit an event
		self.buttonEdit = wx.Button(self, wx.ID_ANY, _("&Edit"))
		sizer_2.Add(self.buttonEdit, 0, 0, 0)

		# Translators: Button to remove an event
		self.buttonRemove = wx.Button(self, wx.ID_ANY, _("&Remove"))
		sizer_2.Add(self.buttonRemove, 0, 0, 0)

		# Translators: Button to start a search
		self.buttonSearch = wx.Button(self, wx.ID_ANY, _("&Search"))
		sizer_2.Add(self.buttonSearch, 0, 0, 0)

		# Translators: Button to close the add-on
		self.buttonExit = wx.Button(self, wx.ID_ANY, _("E&xit"))
		sizer_2.Add(self.buttonExit, 0, 0, 0)

		sizer_2.Realize()
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetEscapeId(self.buttonExit.GetId())

		self.Layout()
		self.CentreOnScreen()

		self.Bind(wx.EVT_BUTTON, self.onAdd, self.buttonAdd)
		self.Bind(wx.EVT_BUTTON, self.onEdit, self.buttonEdit)
		self.Bind(wx.EVT_BUTTON, self.onRemove, self.buttonRemove)
		self.Bind(wx.EVT_BUTTON, self.onSearch, self.buttonSearch)
		self.Bind(wx.EVT_SPINCTRL, self.onChangedDate, self.spinYear)
		self.Bind(wx.EVT_SPINCTRL, self.onChangedDate, self.spinDay)
		self.Bind(wx.EVT_COMBOBOX, self.onChangedDate, self.ComboMonth)
		self.Bind(wx.EVT_BUTTON, self.onExit, self.buttonExit)
		self.currentItemsList.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

		self.periodicityRegisters = None
		self.updateItems()
		self.currentItemsList.Focus(0)
		self.currentItemsList.Select(0)
		self.currentItemsList.SetFocus()

		# Creating keystrokes
		# Add an ID for each keystroke
		self.altLeft = wx.Window.NewControlId()
		self.altRight = wx.Window.NewControlId()
		self.Alt1 = wx.Window.NewControlId()
		self.Alt2 = wx.Window.NewControlId()
		self.Alt3 = wx.Window.NewControlId()
		self.Alt4 = wx.Window.NewControlId()
		self.Alt5 = wx.Window.NewControlId()
		self.Alt6 = wx.Window.NewControlId()
		self.Alt7 = wx.Window.NewControlId()
		self.Alt8 = wx.Window.NewControlId()
		self.Alt9 = wx.Window.NewControlId()
		self.Alt0 = wx.Window.NewControlId()
		self.altUp = wx.Window.NewControlId()
		self.altDown = wx.Window.NewControlId()
		self.AltPageUp = wx.Window.NewControlId()
		self.AltPageDown = wx.Window.NewControlId()
		self.CtrlF = wx.Window.NewControlId()
		# Assign to each keystroke ID a method 
		self.Bind(wx.EVT_MENU, self.onAltLeft, id=self.altLeft)
		self.Bind(wx.EVT_MENU, self.onAltRight, id=self.altRight)
		self.Bind(wx.EVT_MENU, self.onAltRight, id=self.Alt1)
		self.Bind(wx.EVT_MENU, self.onAlt2, id=self.Alt2)
		self.Bind(wx.EVT_MENU, self.onAlt3, id=self.Alt3)
		self.Bind(wx.EVT_MENU, self.onAlt4, id=self.Alt4)
		self.Bind(wx.EVT_MENU, self.onAlt5, id=self.Alt5)
		self.Bind(wx.EVT_MENU, self.onAlt6, id=self.Alt6)
		self.Bind(wx.EVT_MENU, self.onAlt7, id=self.Alt7)
		self.Bind(wx.EVT_MENU, self.onAlt8, id=self.Alt8)
		self.Bind(wx.EVT_MENU, self.onAlt9, id=self.Alt9)
		self.Bind(wx.EVT_MENU, self.onAlt0, id=self.Alt0)
		self.Bind(wx.EVT_MENU, self.onAlt7, id=self.altUp)
		self.Bind(wx.EVT_MENU, self.onAltDown, id=self.altDown)
		self.Bind(wx.EVT_MENU, self.onAltPageUp, id=self.AltPageUp)
		self.Bind(wx.EVT_MENU, self.onAltPageDown, id=self.AltPageDown)
		self.Bind(wx.EVT_MENU, self.onCtrlF, id=self.CtrlF)
		# Assign the keystrokes to the respective ID's
		accel_tbl = wx.AcceleratorTable([(wx.ACCEL_ALT, wx.WXK_LEFT, self.altLeft),
			(wx.ACCEL_ALT, wx.WXK_RIGHT, self.altRight),
			(wx.ACCEL_ALT, ord('1'), self.Alt1),
			(wx.ACCEL_ALT, ord('2'), self.Alt2),
			(wx.ACCEL_ALT, ord('3'), self.Alt3),
			(wx.ACCEL_ALT, ord('4'), self.Alt4),
			(wx.ACCEL_ALT, ord('5'), self.Alt5),
			(wx.ACCEL_ALT, ord('6'), self.Alt6),
			(wx.ACCEL_ALT, ord('7'), self.Alt7),
			(wx.ACCEL_ALT, ord('8'), self.Alt8),
			(wx.ACCEL_ALT, ord('9'), self.Alt9),
			(wx.ACCEL_ALT, ord('0'), self.Alt0),
			(wx.ACCEL_ALT, wx.WXK_UP, self.altUp),
			(wx.ACCEL_ALT, wx.WXK_DOWN, self.altDown),
			(wx.ACCEL_ALT, wx.WXK_PAGEUP, self.AltPageUp),
			(wx.ACCEL_ALT, wx.WXK_PAGEDOWN, self.AltPageDown),
			(wx.ACCEL_CTRL, ord('F'), self.CtrlF),
			(wx.ACCEL_CTRL, ord('f'), self.CtrlF)
		])
		self.SetAcceleratorTable(accel_tbl)

		# Variables to scroll the date by keystroke
		scrollDay = 0
		scrollMonth = 0

	def onAlt2(self, event):
		self.keystrokeScrollDay(2)

	def onAlt3(self, event):
		self.keystrokeScrollDay(3)

	def onAlt4(self, event):
		self.keystrokeScrollDay(4)

	def onAlt5(self, event):
		self.keystrokeScrollDay(5)

	def onAlt6(self, event):
		self.keystrokeScrollDay(6)

	def onAlt7(self, event):
		self.keystrokeScrollDay(7)

	def onAlt8(self, event):
		self.keystrokeScrollDay(8)

	def onAlt9(self, event):
		self.keystrokeScrollDay(9)

	def onAlt0(self, event):
		# The value -10 is set to return to current date
		self.keystrokeScrollDay(-10)

	def onAltDown(self, event):
		scrollDay = -7
		self.keystrokeScrollDay(-7)

	def onAltPageUp(self, event):
		self.keystrokeScrollMonth(1)

	def onAltPageDown(self, event):
		self.keystrokeScrollMonth(-1)

	def onAltLeft(self, event):
		self.keystrokeScrollDay(-1)

	def onAltRight(self, event):
		self.keystrokeScrollDay(1)

	def onCtrlF(self, event):
		self.onSearch(event)

	def keystrokeScrollDay (self, scrollDay):
		self.flagSetFocus=True
		# Capture the current date to change the desired controls
		if scrollDay==-10:
			scrollDay = 0
			year = int(datetime.datetime.strftime(datetime.datetime.now(), '%Y'))
			month = int(datetime.datetime.strftime(datetime.datetime.now(), '%m'))
			currentMonth = month
			day = int(datetime.datetime.strftime(datetime.datetime.now(), '%d'))

			# Get the month maximum day
			dayMax = maxDayMonth(year, month)
		else:
			year = self.spinYear.GetValue()
			monthStr = self.ComboMonth.GetValue()
			if calendarToUse == _("Gregorian (Default)"):
				month = 12-months.index(monthStr)
			elif calendarToUse == _("Persian"):
				month = 12-persianMonths.index(monthStr)
			currentMonth = month
			day = self.spinDay.GetValue()
			dayMax = self.spinDay.GetMax()
		dayToScroll = day + scrollDay 

		# If the day is greater than the maximum possible, go to next month
		if dayToScroll < 1:
			month -= 1
			if month < 1:
				month = 12
				year -= 1
		if dayToScroll> dayMax:
			month += 1
			dayToScroll = dayToScroll - dayMax
			if month > 12:
				month = 1
				year += 1

		# If month have changed get the maximum of days
		if month != currentMonth:
			dayMax = maxDayMonth(year, month)

			self.spinDay.SetRange(1, dayMax)
			# If gone to day 0 go to last day of previous month
			if dayToScroll==0:
				dayToScroll = dayMax
			# If gone to 7 days before, gets the correct day
			if dayToScroll < 0:
				dayToScroll += dayMax
		# Update the date controls
		self.spinYear.SetValue(year)
		self.ComboMonth.SetValue(months[12-month])
		self.spinDay.SetValue(dayToScroll)

		# Call the function to update the details of the new date
		self.updateItems()

	def keystrokeScrollMonth(self, scrollMonth):
		self.flagSetFocus=True
		# Read the details to change the date
		year = self.spinYear.GetValue()
		monthStr = self.ComboMonth.GetValue()
		month = 12-months.index(monthStr)
		currentMonth = month
		day = self.spinDay.GetValue()
		dayMax = self.spinDay.GetMax()
		month  += scrollMonth
		# If gone to month 0
		if month < 1:
			month = 12
			year -= 1
		# If gone to month 13
		if month > 12:
			month = 1
			year += 1
		# Check if day number is greater than maximum possible
		dayMax = maxDayMonth(year, month)
		self.spinDay.SetRange(1, dayMax)
		if day > dayMax:
			day = dayMax

		# Update the date details
		self.spinYear.SetValue(year)
		if calendarToUse == _("Gregorian (Default)"):
			self.ComboMonth.SetValue(months[12-month])
		else:
			self.ComboMonth.SetValue(persianMonths[12-month])
		self.spinDay.SetValue(day)

		# Call the function to update the details
		self.updateItems()

	def onChangedDate (self, event):
		self.flagSetFocus=False
		self.updateItems()

	def updateItems(self):
		if calendarToUse == _("Gregorian (Default)"):
			# Gets the date fields to make the search
			yearToSearch = str(self.spinYear.GetValue())
			monthToSearchStr = self.ComboMonth.GetValue()
			monthToSearch = '%02d' % (12-months.index(monthToSearchStr))
			# Gets the maximum days of the month
			year = int(yearToSearch)
			month = 12-months.index(monthToSearchStr)
			dayMax = maxDayMonth(year, month)
			self.spinDay.SetRange(1, dayMax)
			dayToSearch = '%02d' % self.spinDay.GetValue()
			# Gets the week day
			weekToSearch = weekDays[datetime.date (int(yearToSearch),int(monthToSearch),int(dayToSearch)) .weekday ()]
			# Updates week day field
			self.weekDay.SetValue(weekToSearch)
			newTitle = dayToSearch+'/'+monthToSearch+'/'+yearToSearch

		elif calendarToUse == _("Persian"):
			# Gets the date fields to make the search
			yearToSearch = str(self.spinYear.GetValue())
			monthToSearchStr = self.ComboMonth.GetValue()
			monthToSearch = '%02d' % (12 - persianMonths.index(monthToSearchStr))
			# Gets the maximum days of the month
			year = int(yearToSearch)
			month = 12 - persianMonths.index(monthToSearchStr)
			dayMax = maxDayMonth(year, month)
			self.spinDay.SetRange(1, dayMax)
			dayToSearch = '%02d' % self.spinDay.GetValue()
			newTitle = dayToSearch+'/'+monthToSearch+'/'+yearToSearch
			gregorianDate = persian.to_gregorian(int(yearToSearch), int(monthToSearch), int(dayToSearch))
			yearToSearch = str(gregorianDate[0])
			monthToSearch = str("%02d" % (gregorianDate[1]))
			dayToSearch = str("%02d" % (gregorianDate[2]))
			# Gets the week day
			weekToSearch = weekDays[datetime.date (int(yearToSearch),int(monthToSearch),int(dayToSearch)) .weekday ()]
			# Updates week day field
			self.weekDay.SetValue(weekToSearch)

		startDateToSearch = int(yearToSearch + monthToSearch + dayToSearch + '0000')
		finalDateToSearch = int(yearToSearch + monthToSearch + dayToSearch + '2359')

		# If date was changed, search by appointments in database
		# Conecting to database
		from .configPanel import dirDatabase
		what = "*"
		find = "data>= " + str(startDateToSearch) + " and data<= " + str(finalDateToSearch) + " order by data asc"
		occurs = manageDatabase.findItem(what, find, dirDatabase, all=True)
		# Clears listbox and items list
		self.currentItemsList.ClearAll()
		self.flagRecordExists = False
		self.currentItemsList.AppendColumn(_("Hour:"), format=wx.LIST_FORMAT_LEFT, width = 100)
		self.currentItemsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width = 400)
		i = 0
		if len(occurs) !=0:
			self.flagRecordExists = True
			for lineTable in occurs:
				dateRead  = str(lineTable[0])
				index = self.currentItemsList.InsertItem(i, dateRead[8:10] + ':' + dateRead[10:12] + " ")
				self.currentItemsList.SetItem(index, 1,lineTable[2])
				i+=1

		self.periodicityRegisters = manageDatabase.findRepeatIntervalDate(startDateToSearch, finalDateToSearch, True, dirDatabase)
		if len(self.periodicityRegisters)>0:
			self.flagRecordExists = True
			for lineTable in self.periodicityRegisters:
				dateRead  = str(lineTable[1])
				index = self.currentItemsList.InsertItem(i, dateRead[8:10] + ':' + dateRead[10:12] + " ")
				self.currentItemsList.SetItem(index, 1, frequency[lineTable[10]]+', '+lineTable[3])
				i+=1
		self.label_4.SetLabel(_(str(self.currentItemsList .GetItemCount()) + _(" items found")))
		if not self.flagRecordExists:
			self.label_4.SetLabel(_("No items found"))
			self.currentItemsList.InsertItem(0, '')
			self.currentItemsList.SetItem(0, 1, _("No appointments"))
		if self.flagSetFocus:
			self.currentItemsList.Focus(0)
			self.currentItemsList.Select(0)
			self.currentItemsList.SetFocus()
			self.flagSetFocus=False
		else:
			ui.message(self.label_4.Label + ", " + self.currentItemsList.GetItemText(0, 0) + ", " + self.currentItemsList.GetItemText(0, 1))
		self.SetTitle(_(newTitle))

	def onAdd(self, event):
		global itemToEdit, titleAddEd
		generalVars.titleAddEd = _("Add")
		# Gets the date fields to make the search
		yearToSearch = str(self.spinYear.GetValue())
		monthToSearchStr = self.ComboMonth.GetValue()
		if calendarToUse == _("Gregorian (Default)"):
			monthToSearch = '%02d' % (12-months.index(monthToSearchStr))
		elif calendarToUse == _("Persian"):
			monthToSearch = '%02d' % (12-persianMonths.index(monthToSearchStr))
		dayToSearch = '%02d' % self.spinDay.GetValue()

		# The variable must have the date details
		generalVars.itemToEdit = int(yearToSearch+monthToSearch+dayToSearch)
		if calendarToUse == _("Persian"):
			gregorianDate = persian.to_gregorian(int(yearToSearch), int(monthToSearch), int(dayToSearch))
			generalVars.itemToEdit = str(gregorianDate[0]) + str('%02d' % (gregorianDate[1])) + str('%02d' % (gregorianDate[2]))

		dialogAdd = DlgAddEdit(generalVars, self)
		dialogAdd.ShowModal()
		dialogAdd.Destroy()
		loadAlarms(0)
		self.updateItems()
		event.Skip()

	def onEdit(self, event):
		global titleAddEd, itemToEdit
		generalVars.titleAddEd = _("Edit")

		# The variable must have the date details
		if self.flagRecordExists and self.currentItemsList.GetSelectedItemCount() != 0:
			# Gets the date fields to create the complete date to search
			year = str(self.spinYear.GetValue())
			monthStr = self.ComboMonth.GetValue()
			if calendarToUse == _("Gregorian (Default)"):
				month = '%02d' % (12-months.index(monthStr))
			elif calendarToUse == _("Persian"):
				month = '%02d' % (12-persianMonths.index(monthStr))
			day = '%02d' % int(self.spinDay.GetValue())
			strItemToEdit = self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 0)
			hour = strItemToEdit[:2]+strItemToEdit[3:5]
			generalVars.itemToEdit = int(year+month+day+hour)
			if calendarToUse == _("Persian"):
				gregorianDate = persian.to_gregorian(int(year), int(month), int(day))
				generalVars.itemToEdit = int(str(gregorianDate[0]) + str('%02d' % (gregorianDate[1])) + str('%02d' % (gregorianDate[2])) + hour)
			flagGoToEdit = True
			for foundRepeatRegister  in self.periodicityRegisters:
				if foundRepeatRegister[1]==generalVars.itemToEdit:
					dlg = wx.MessageDialog(self, _("You selected a periodic event. You can't edit a date inside on periodic event.\nInstead of, you need edit the original register. Do you want edit It?"), _("Edit periodic event"), wx.YES_NO)
					if dlg.ShowModal()==wx.ID_YES:
						generalVars.itemToEdit= foundRepeatRegister[0]
						break
					else:
						flagGoToEdit = False
						break

			if flagGoToEdit:
				dialogEdit = DlgAddEdit(generalVars, self)
				dialogEdit.ShowModal()
				dialogEdit.Destroy()
				loadAlarms(0)
				self.updateItems()
			self.currentItemsList.SetFocus()
		else:
			dlg = wx.MessageDialog( self, _("You have not selected any appointment to edit."), _("Agenda"), wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
		event.Skip()

	def onRemove(self, event):
		if self.flagRecordExists and self.currentItemsList.GetSelectedItemCount() > 0:
			# Gets all data fields to compose the date
			year = str(self.spinYear.GetValue())
			monthStr = self.ComboMonth.GetValue()
			if calendarToUse == _("Gregorian (Default)"):
				month = '%02d' % (12-months.index(monthStr))
			elif calendarToUse == _("Persian"):
				month = '%02d' % (12-persianMonths.index(monthStr))
			day = '%02d' % int(self.spinDay.GetValue())
			strItemToRemove = self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 0)
			strItemToRemoveMsg = strItemToRemove  + " " + self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 1)
			hour = strItemToRemove[:2]+strItemToRemove[3:5]
			itemToRemove = int(year + month + day + hour)
			if calendarToUse == _("Persian"):
				gregorianDate = persian.to_gregorian(int(year), int(month), int(day))
				itemToRemove = int(str(gregorianDate[0]) + str('%02d' % gregorianDate[1]) + str('%02d' % gregorianDate[2]) + hour)
			msgRemove = (_("Do you really want to remove the  item: ") + strItemToRemoveMsg + "?")
			for foundRepeatRegister  in self.periodicityRegisters:
				if foundRepeatRegister[1]==itemToRemove:
					originalDate = str(foundRepeatRegister[0])
					originalDateStr = originalDate[6:8]+'/'+originalDate[4:6]+'/'+originalDate[:4]+', '+originalDate[8:10]+':'+originalDate[10:12]+', '+foundRepeatRegister[3]
					msgRemove = _("You can't remove just one periodic event. Instead of, you need remove the original register. If you make this, alldates on this periodic event will be deleted.\nDo you want to delete the original register and all   dates of this {} event:\n{}?").format(frequency[foundRepeatRegister[10]], originalDateStr)
					itemToRemove= foundRepeatRegister[0]
					break
			dlg = wx.MessageDialog(self, msgRemove, _("Remove item"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES:
				# Conecting to database
				from .configPanel import dirDatabase
				manageDatabase.removeItem(itemToRemove, dirDatabase)
				manageDatabase.removeRepeat(itemToRemove, dirDatabase)
				dlg2 = wx.MessageDialog( self, _("Appointment removed successfully!"), _("Agenda"), wx.OK)
				dlg2.ShowModal()
				dlg2.Destroy()
			self.updateItems()
			self.currentItemsList.SetFocus()
			loadAlarms(0)
		else:
			dlg = wx.MessageDialog( self, _("You have not selected any appointment to be removed."), _("Agenda"), wx.OK)
			dlg.ShowModal()
			dlg.Destroy()

	def onKeyPress(self, event):
		event.Skip()
		# Sets enter key  to edit the appointment, if exist or to add if not exist, and delete to remove it.
		keycode = event.GetKeyCode()
		if keycode == wx.WXK_RETURN and self.label_4.Label == _("No items found"):
			self.onAdd(event)
		elif keycode == wx.WXK_RETURN and self.currentItemsList.GetItemCount():
			self.onEdit(event)
		elif keycode == wx.WXK_DELETE and self.currentItemsList.GetItemCount():
			self.onRemove(event)

	def onSearch(self, event):
		# Loads the search window
		dialogSearch = searchWindow(None)
		dialogSearch.ShowModal()
		dialogSearch.Destroy()
		self.updateItems()
		self.currentItemsList.SetFocus()
		self.currentItemsList.Focus(0)
		self.currentItemsList.Select(0)

	def onExit(self, event):
		self.Close()
		self.Destroy()
