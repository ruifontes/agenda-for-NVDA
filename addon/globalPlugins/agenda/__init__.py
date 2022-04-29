# -*- coding: utf-8 -*-
# Agenda add-on
# Provides an accessible agenda with or without alarms
# Shortcut: NVDA+F4
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
import globalPluginHandler
import core
import os
import wx
import gui
import ui
from . import sqlite3
import threading
import time
import	datetime
# For update process
from .update import *
# Necessary For translation
from scriptHandler import script
import addonHandler
addonHandler.initTranslation()

#Global variables
dirDatabase = os.path.join(os.path.dirname(__file__), "agenda.db")
firstDatabase = ""
altDatabase = ""
indexDB = 0
months = [_("December"), _("November"), _("October"), _("September"), _("August"), _("July"), _("June"), _("May"), _("April"), _("March"), _("February"), _("January")]
weekDays = [_("Monday"), _("tuesday"), _("Wednesday"), _("Thursday"), _("Friday"), _("Saturday"), _("Sunday")]
titleAddEd = ""
itemToEdit = 0
dateToSearch = ""
endAlarms = False
flagPauseAlarm=False
dictNextAlarms={}

initConfiguration()

flagAlarmDayAfter = False if config.conf[ourAddon.name]["show"] else True

# Gets the maximum day of the month passed to the function
def maxDayMonth(year, month):
	dayMax =0
	if month in [1, 3, 5, 7, 8, 10, 12]:
		dayMax=31
	elif month in [4, 6, 9, 11]:
		dayMax=30
	else:
		if (year/4)==(year//4) and (year/100)!=(year//100):
			dayMax=29
		else:	 
			dayMax=28
	return dayMax

def avoidSecure():
	# Avoid use in secure screens and during installation
	if (globalVars.appArgs.secure or globalVars.appArgs.install or globalVars.appArgs.minimal):
		return

def threadAlarm ():
	global dictNextAlarms
	# check each minute if alarm exists
	while not endAlarms:
		while  flagPauseAlarm:
			time.sleep(5)
		m = int(datetime.datetime.strftime(datetime.datetime.now(), '%M'))
		x = m	 
		while x==m:
			m = datetime.datetime.strftime(datetime.datetime.now(), '%M')
			#Check every 5 seconds if the minutes value was changed
			time.sleep(5)
		# if minute increase, check dictionary
		selfNow = datetime.datetime.now()
		nextDays = selfNow + datetime.timedelta(days=+1)
		justNow = int(datetime.datetime.strftime(selfNow, '%Y%m%d%H%M'))
		tomorrowStart = int(datetime.datetime.strftime(nextDays, '%Y%m%d')+'0000')
		tomorrowEnd = int(datetime.datetime.strftime(nextDays, '%Y%m%d')+'2359')
		if len(dictNextAlarms) != 0:
			oneHourBefore = int(datetime.datetime.strftime(selfNow + datetime.timedelta(minutes=60), '%Y%m%d%H%M')) 
			halfHourBefore = int(datetime.datetime.strftime(selfNow + datetime.timedelta(minutes=30), '%Y%m%d%H%M')) 
			fifteenMinutesBefore = int(datetime.datetime.strftime(selfNow + datetime.timedelta(minutes=15), '%Y%m%d%H%M')) 
			msgNextDay =	''
			msgAlarm1 = ""
			for dictLine in dictNextAlarms:
				# clear field to create message to show
				titleAlarm = ""
				msgAlarm = ""

				# Saves alarm flags status
				flagAlarmOneDay = int(dictNextAlarms[dictLine][1])
				flagAlarmOneHour = int(dictNextAlarms[dictLine][2])
				flagAlarm30Minutes = int(dictNextAlarms[dictLine][3])
				flagAlarm15Minutes = int(dictNextAlarms[dictLine][4])
				flagAlarmExactHour = int(dictNextAlarms[dictLine][5])

				# If database has any alarm to play, play it!
				if (dictLine in [justNow, oneHourBefore, halfHourBefore, fifteenMinutesBefore] or dictLine >= tomorrowStart and dictLine <= tomorrowEnd):
					# Alarm for appointments next day
					if flagAlarmOneDay and dictLine>=tomorrowStart and dictLine<=tomorrowEnd:
						flagAlarmOneDay = False
						dictNextAlarms[dictLine][1]=0
						msgAlarm1 = _("You have the following appointment tomorrow:\n")
						msgAddHour=str(dictLine)[8:10] + ':' + str(dictLine)[10:]
						msgNextDay += msgAddHour+', '+dictNextAlarms[dictLine][0]+'\n'
						msgAlarm1 += msgNextDay

					# Alarm for appointments in an hour
					if flagAlarmOneHour and dictLine == oneHourBefore:
						flagAlarmOneHour = False
						dictNextAlarms[dictLine][2]=0
						titleAlarm = _("Reminder!")
						msgAlarm = _("You have the following appointment in one hour:\n")

					# Alarm for appointments in 30 minutes
					if flagAlarm30Minutes and dictLine == halfHourBefore:
						flagAlarm30Minutes = False
						dictNextAlarms[dictLine][3]=0
						titleAlarm = _("Reminder!")
						msgAlarm = _("You have the following appointment in 30 minutes:\n")

					# Alarm for appointments in 15 minutes
					if flagAlarm15Minutes and dictLine==fifteenMinutesBefore:
						flagAlarm15Minutes = False
						dictNextAlarms[dictLine][4]=0
						titleAlarm = _("Reminder!")
						msgAlarm = _("You have the following appointment in 15 minutes:\n")

					# Alarm for appointments now
					if flagAlarmExactHour and dictLine == justNow:
						flagAlarmExactHour = False
						dictNextAlarms[dictLine][5]=0
						titleAlarm = _("Reminder!")
						msgAlarm = _("You have now the following appointment:\n")

					# If we have a title, we have an alarm, so show the message
					if len(titleAlarm)>0:
						ringFile = os.path.join(os.path.dirname(__file__), "ringin.wav")
						winsound.PlaySound(ringFile, winsound.SND_FILENAME|winsound.SND_ASYNC)
						dlg = wx.MessageDialog(None, msgAlarm + dictNextAlarms[dictLine][0], titleAlarm, wx.OK)
						dlg.ShowModal() 
						dlg.Destroy()
			# if flagOneDay was set
			if len(msgAlarm1) != 0:
				ringFile = os.path.join(os.path.dirname(__file__), "ringin.wav")
				winsound.PlaySound(ringFile, winsound.SND_FILENAME|winsound.SND_ASYNC)
				dlg = wx.MessageDialog(None, msgAlarm1, _("Reminder!"), wx.OK)
				dlg.ShowModal() 
				dlg.Destroy()

# Load all alarms after now
def loadAlarms(allow):
	global flagPauseAlarm, dictNextAlarms, flagAlarmDayAfter
	allow = allow
	# Get date and time
	dateTimeNow = int(datetime.datetime.strftime(datetime.datetime.now(), '%y%m%d%H%M'))
	# Stop threadAlarme
	flagPauseAlarm=True
	# Conecting to database
	what = "data, descricao, alarmedia, alarmehora, alarmemeiahora, alarmequartodehora, alarmehoraexata"
	find = "data>= " + str(dateTimeNow) + " and " + "(alarmedia or alarmehora or alarmemeiahora or alarmequartodehora or alarmehoraexata)"
	occurs = manageDatabase.findItem(what, find, all=True)

	# If we have alarms scheduled, save them in dict
	dictNextAlarms = {}
	if occurs != None:
		for regLine in occurs:
			dictNextAlarms[int(regLine[0])] = list(regLine[1:])
			# Disable alert dialog if next appointments window was showed
			if not flagAlarmDayAfter:
				dictNextAlarms[int(regLine[0])][1]=0
		flagAlarmDayAfter=True
	flagPauseAlarm=False
	if allow == 1:
		gui.mainFrame._popupSettingsDialog(nextAppointments)
	else:
		pass


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	# Creating the constructor of the newly created GlobalPlugin class.
	def __init__(self):
		# Call of the constructor of the parent class.
		super(globalPluginHandler.GlobalPlugin, self).__init__()

		# Avoid use in secure screens
		if globalVars.appArgs.secure:
			return

		# Translators: Dialog title
		title = _("Agenda")

		# Adding a NVDA configurations section
		gui.NVDASettingsDialog.categoryClasses.append(AgendaSettingsPanel)

		# To allow waiting end of network tasks
		core.postNvdaStartup.register(self.networkTasks)

		# To check if agenda settings panel should be shown or not
		config.post_configProfileSwitch.register(self.handleConfigProfileSwitch)

		# Read configuration on INI file to know where are the agenda.db files...
		global dirDatabase, firstDatabase, altDatabase, indexDB
		try:
			if config.conf[ourAddon.name]["xx"]:
				# index of agenda.db file to use
				indexDB = int(config.conf[ourAddon.name]["xx"])
				if indexDB == 0:
					dirDatabase = 				config.conf[ourAddon.name]["path"]
				else:
					dirDatabase = 				config.conf[ourAddon.name]["altPath"]
				firstDatabase = config.conf[ourAddon.name]["path"]
				altDatabase = config.conf[ourAddon.name]["altPath"]
		except:
			# Not registered, so use the default path
			pass

		# Check for database file
		if not os.path.exists(dirDatabase):
			# Does not exist, so creat it
			manageDatabase.createDatabase()
		# Decide if appointments for today and tomorrow are shown
		if not (globalVars.appArgs.install and globalVars.appArgs.minimal):
			if config.conf[ourAddon.name]["show"]:
				# Is shown is set, so display the today and tomorrow appointments
				allow = 1
			else:
				allow = 0
			# Load next alarms and start alarm threading
			loadAlarms(allow)
			t = None
			t = threading.Thread(target=threadAlarm)
			t.setDaemon(True)
			t.start()

	# Check if we are with a active profile or not, to decide if agenda settings panel is shown
	def handleConfigProfileSwitch(self):
		if config.conf.profiles[-1].name:
			try:
				NVDASettingsDialog.categoryClasses.remove(AgendaSettingsPanel)
			except Exception:  # panel is not present
				pass
		elif not AgendaSettingsPanel in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.append(AgendaSettingsPanel)

	def networkTasks(self):
		# Calling the update process...
		_MainWindows = Initialize()
		_MainWindows.start()

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		try:
			NVDASettingsDialog.categoryClasses.remove(AgendaSettingsPanel)
		except Exception:
			pass
		config.post_configProfileSwitch.unregister(self.handleConfigProfileSwitch)
		core.postNvdaStartup.unregister(self.networkTasks)

	#defining a script with decorator:
	@script(
		gesture="kb:NVDA+f4",
		# Translators: Message to be announced during Keyboard Help	 
		description= _("Main window to access an accessible agenda"),
		# For translators: Name of the section in "Input gestures" dialog.	
		category= _("Agenda"))
	def script_callMainWindow(self, event):
		#Calling the agenda main dialog.
		gui.mainFrame._popupSettingsDialog(MainWindow)


class AgendaSettingsPanel(gui.SettingsPanel):
	# Translators: Title of the Agenda settings dialog in the NVDA settings.
	title = _("Agenda")

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		# Translators: Checkbox name in the configuration dialog
		self.showNextAppointmentsWnd = wx.CheckBox(self, label = _("Show next appointments at startup"))
		self.showNextAppointmentsWnd.SetValue(config.conf[ourAddon.name]["show"])
		settingsSizerHelper.addItem(self.showNextAppointmentsWnd)

		# Translators: Checkbox name in the configuration dialog
		self.shouldUpdateChk = wx.CheckBox(self, label = _("Check for updates at startup"))
		self.shouldUpdateChk.SetValue(config.conf[ourAddon.name]["isUpgrade"])
		settingsSizerHelper.addItem(self.shouldUpdateChk)

		# Translators: Name of combobox with the agenda files path
		pathBoxSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label = _("Path of agenda files:"))
		pathBox = pathBoxSizer.GetStaticBox()
		pathGroup = guiHelper.BoxSizerHelper(self, sizer = pathBoxSizer)
		settingsSizerHelper.addItem(pathGroup)

		global firstDatabase
		if firstDatabase == "":
			firstDatabase = dirDatabase
		self.pathList = [firstDatabase, altDatabase]
		self.pathNameCB = pathGroup.addLabeledControl("", wx.Choice, choices = self.pathList)
		self.pathNameCB.SetSelection(indexDB)

		# Translators: This is the label for the button used to add or change a agenda.db location
		changePathBtn = wx.Button(pathBox, label = _("&Select or add a directory"))
		changePathBtn.Bind(wx.EVT_BUTTON,self.OnDirectory)

	def OnDirectory(self, event):
		self.Freeze()
		global dirDatabase, firstDatabase, altDatabase, indexDB
		lastDir = os.path.dirname(__file__)
		dDir = lastDir
		dFile = "agenda.db"
		frame = wx.Frame(None, -1, 'teste')
		frame.SetSize(0,0,200,50)
		dlg = wx.FileDialog(frame, _("Choose where to save the agenda file"), dDir, dFile,
				wildcard = _("Database files (*.db)"),
				style = wx.FD_SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			fname = dlg.GetPath()
			index = self.pathNameCB.GetSelection()
			if index == 0:
				if os.path.exists(fname):
					firstDatabase = fname
				else:
					os.rename(firstDatabase, fname)
					firstDatabase = fname
			else:
				if os.path.exists(fname):
					altDatabase = fname
				else:
					if altDatabase == "":
						altDatabase = fname
					else:
						os.rename(altDatabase, fname)
						altDatabase = fname
			dirDatabase = fname
			self.pathList = [firstDatabase, altDatabase]
		dlg.Close() 
		self.onPanelActivated()
		self._sendLayoutUpdatedEvent()
		self.Thaw()
		event.Skip()

	def onSave (self):
		global dirDatabase, indexDB
		config.conf[ourAddon.name]["show"] = self.showNextAppointmentsWnd.GetValue()
		config.conf[ourAddon.name]["isUpgrade"] = self.shouldUpdateChk.GetValue()
		config.conf[ourAddon.name]["path"] = firstDatabase
		config.conf[ourAddon.name]["altPath"] = altDatabase
		config.conf[ourAddon.name]["xx"] = str(self.pathList.index(self.pathNameCB.GetStringSelection()))
		config.conf.save()
		indexDB = self.pathNameCB.GetSelection()
		dirDatabase = self.pathList[indexDB]

	def terminate(self):
		super(AgendaSettingsPanel, self).terminate()
		pass

class nextAppointments(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		self.SetTitle(_("Appointments for today and tomorrow"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Items found:"))
		sizer_1.Add(self.label_1, 0, 0, 0)

		self.appointmentsList = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.appointmentsList.AppendColumn(_("Date/Hour"), format=wx.LIST_FORMAT_LEFT, width=100)
		self.appointmentsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width=400)
		sizer_1.Add(self.appointmentsList, 1, wx.EXPAND, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK, _("&Ok"))
		self.button_OK.SetDefault()
		sizer_2.AddButton(self.button_OK)

		sizer_2.Realize()
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.Bind(wx.EVT_BUTTON, self.OnOk, self.button_OK)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnOk, self.appointmentsList)

		self.Layout()
		self.CentreOnScreen()

		# Define the date range to find appointements
		Now = datetime.datetime.now()
		todayStart = int(datetime.datetime.strftime(Now, '%Y%m%d')+'0000')
		nextDays = Now + datetime.timedelta(days=+1)
		tomorrowEnd = int(datetime.datetime.strftime(nextDays, '%Y%m%d')+'2359')
		# Conecting to database
		what = "*"
		find = "data>= " + str(todayStart) + " and data<= " + str(tomorrowEnd)
		occurs = manageDatabase.findItem(what, find, all=True)
		# Create the list of appointements
		if len(occurs)>0:
			i=0
			for lines in occurs:
				dateRead  = str(lines[0])
				today=str(todayStart)
				tomorrow =str(tomorrowEnd) 
				dayText = ""
				if dateRead[:8] == today[0:8]:
					dayText = _("Today")
				else:
					dayText = _("Tomorrow")
				self.appointmentsList.InsertItem(i, dayText + ', ' + dateRead[8:10] + ':' + dateRead[10:12] + " ")
				self.appointmentsList.SetItem(i, 1,lines[2])
				i+=1
			# Add the numbers of itens to the label...
			self.label_1.SetLabel(str(self.appointmentsList.GetItemCount()) + _(" items found"))
			self.appointmentsList.SetFocus()
			self.appointmentsList.Focus(0)
			self.appointmentsList.Select(0)
		else:
			# Announce no appointements
			self.appointmentsList.Hide()
			label_1 = wx.StaticText(self, wx.ID_ANY, _("You do not have any appointments for today and tomorrow!"))
			label_1.SetFocus()
			sizer_1.Add(label_1, 0, 0, 0)

	def OnOk(self, event):
		self.Destroy()
		event.Skip()


class MainWindow(wx.Dialog):
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
		self.SetTitle(_("Agenda"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

		label_1 = wx.StaticText(self, wx.ID_ANY, _("Day:"))
		sizer_3.Add(label_1, 0, 0, 0)
		self.spinDay = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=31)
		self.spinDay.SetValue(int(self.currentDay))
		sizer_3.Add(self.spinDay, 0, 0, 0)

		label_2 = wx.StaticText(self, wx.ID_ANY, _("Month:"))
		sizer_3.Add(label_2, 0, 0, 0)
		self.ComboMonth = wx.ComboBox(self, wx.ID_ANY, choices = months , style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.ComboMonth.SetSelection(12-int(self.currentMonth))
		sizer_3.Add(self.ComboMonth, 0, 0, 0)

		label_3 = wx.StaticText(self, wx.ID_ANY, _("Year:"))
		sizer_3.Add(label_3, 0, 0, 0)
		self.spinYear = wx.SpinCtrl(self, wx.ID_ANY, "1970", min=1970, max=2050)
		self.spinYear.SetValue(int(self.currentYear))
		sizer_3.Add(self.spinYear, 0, 0, 0)

		self.weekDay = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
		sizer_3.Add(self.weekDay, 0, 0, 0)

		self.label_4 = wx.StaticText(self, wx.ID_ANY, _("items found:"))
		sizer_1.Add(self.label_4, 0, 0, 0)

		self.currentItemsList = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.currentItemsList.AppendColumn(_("Hour"), format=wx.LIST_FORMAT_LEFT, width = -1)
		self.currentItemsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width = -1)
		sizer_1.Add(self.currentItemsList, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.buttonAdd = wx.Button(self, wx.ID_ANY, _("&Add"))
		sizer_2.Add(self.buttonAdd, 0, 0, 0)

		self.buttonEdit = wx.Button(self, wx.ID_ANY, _("&Edit"))
		sizer_2.Add(self.buttonEdit, 0, 0, 0)

		self.buttonRemove = wx.Button(self, wx.ID_ANY, _("&Remove"))
		sizer_2.Add(self.buttonRemove, 0, 0, 0)

		self.buttonSearch = wx.Button(self, wx.ID_ANY, _("&Search"))
		sizer_2.Add(self.buttonSearch, 0, 0, 0)

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
			month = 12-months.index(monthStr)
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
		self.ComboMonth.SetValue(months[12-month])
		self.spinDay.SetValue(day)

		# Call the function to update the details
		self.updateItems()

	def onChangedDate (self, event):
		self.flagSetFocus=False
		self.updateItems()

	def updateItems(self):
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
		startDateToSearch = int(yearToSearch + monthToSearch + dayToSearch + '0000')
		finalDateToSearch = int(yearToSearch + monthToSearch + dayToSearch + '2359')
		newTitle = dayToSearch+'/'+monthToSearch+'/'+yearToSearch

		#Gets the week day
		weekToSearch = weekDays[datetime.date (int(yearToSearch),int(monthToSearch),int(dayToSearch)) .weekday ()]
		# Updates week day field
		self.weekDay.SetValue(weekToSearch)

		# If date was changed, search by appointments in database
		# Check if database exist
		if not os.path.exists(dirDatabase):
			# Does not exist, so create it
			manageDatabase.createDatabase()
		# Conecting to database
		what = "*"
		find = "data>= " + str(startDateToSearch) + " and data<= " + str(finalDateToSearch) + " order by data asc"
		occurs = manageDatabase.findItem(what, find, all=True)
		# Clears listbox and items list
		self.currentItemsList.ClearAll()
		self.flagRecordExists = False
		self.currentItemsList.AppendColumn(_("Hour:"), format=wx.LIST_FORMAT_LEFT, width = 100)
		self.currentItemsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width = 400)
		if len(occurs) !=0:
			self.flagRecordExists = True
			i = 0
			for lineTable in occurs:
				dateRead  = str(lineTable[0])
				self.currentItemsList.InsertItem(i, dateRead[8:10] + ':' + dateRead[10:12] + " ")
				self.currentItemsList.SetItem(i, 1,lineTable[2])
				i+=1
			self.label_4.SetLabel(_(str(self.currentItemsList .GetItemCount()) + " items found"))
		else:
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
		titleAddEd = _("Add")
		# Gets the date fields to make the search
		yearToSearch = str(self.spinYear.GetValue())
		monthToSearchStr = self.ComboMonth.GetValue()
		monthToSearch = '%02d' % (12-months.index(monthToSearchStr))
		dayToSearch = '%02d' % self.spinDay.GetValue()

		# The variable must have the date details
		itemToEdit = int(yearToSearch+monthToSearch+dayToSearch)

		dialogAdd = DlgAddEdit(None)
		dialogAdd.ShowModal()
		dialogAdd.Destroy()
		self.updateItems()
		event.Skip()

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

	def onEdit(self, event):
		global titleAddEd
		titleAddEd = _("Edit")
		global itemToEdit
		# The variable must have the date details
		if self.flagRecordExists:
			# Gets the date fields to create the complete date to search
			year = str(self.spinYear.GetValue())
			monthStr = self.ComboMonth.GetValue()
			month = '%02d' % (12-months.index(monthStr))
			day = '%02d' % int(self.spinDay.GetValue())
			strItemToEdit = self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 0)
			hour = strItemToEdit[:2]+strItemToEdit[3:5]
			itemToEdit = int(year+month+day+hour)
			dialogEdit = DlgAddEdit(None)
			dialogEdit.ShowModal()
			dialogEdit.Destroy()
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
			month = '%02d' % (12-months.index(monthStr))
			day = '%02d' % int(self.spinDay.GetValue())
			strItemToRemove = self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 0)
			strItemToRemoveMsg = strItemToRemove  + " " + self.currentItemsList.GetItemText(self.currentItemsList.GetFocusedItem(), 1)
			hour = strItemToRemove[:2]+strItemToRemove[3:5]
			itemToRemove = int(year + month + day + hour)

			dlg = wx.MessageDialog(self, (_("Do you really want to remove the  item: ") + strItemToRemoveMsg + "?"), _("Agenda"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES:
				# Conecting to database
				manageDatabase.removeItem(itemToRemove)
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


class DlgAddEdit(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)

		global titleAddEd, itemToEdit, scrollDay
		self.exitType="Normal"
		self.exitConfirm = False
		self.SetTitle(titleAddEd)

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

		self.checkbox_1 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm for the day before"))
		self.checkbox_1.SetValue(1)
		sizer_1.Add(self.checkbox_1, 0, 0, 0)

		self.checkbox_2 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm to one hour before"))
		self.checkbox_2.SetValue(1)
		sizer_1.Add(self.checkbox_2, 0, 0, 0)

		self.checkbox_3 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm to half hour before"))
		self.checkbox_3.SetValue(1)
		sizer_1.Add(self.checkbox_3, 0, 0, 0)

		self.checkbox_4 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm to 15 minutes before"))
		self.checkbox_4.SetValue(1)
		sizer_1.Add(self.checkbox_4, 0, 0, 0)

		self.checkbox_5 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm to the exact hour"))
		self.checkbox_5.SetValue(1)
		sizer_1.Add(self.checkbox_5, 0, 0, 0)

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
		self.currentYear = str(itemToEdit)[:4]
		self.currentMonth = str(itemToEdit)[4:6]
		self.currentDay = str(itemToEdit)[6:8]
		self.itemToEditStr = str(itemToEdit)

		if titleAddEd == _("Add"):
			# We are in the Add window
			# adjust current hour
			self.now = str(datetime.datetime.now())
			self.currentHour = self.now[11:13]
			self.currentMinute = self.now[14:16]
			# correct the variable with the received date from the class, if necessary
			self.itemToEditStr = self.currentYear + self.currentMonth + self.currentDay + self.currentHour + self.currentMinute
			itemToEdit = int(self.itemToEditStr)

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
			itemToEdit = int(self.itemToEditStr)

			# As we are Editing, loads from database the selected details of selected item
			# Conecting to database
			what = "*"
			find = "data= " + str(itemToEdit)
			occurs = manageDatabase.findItem(what, find, all=False)
			self.currentDateStr = str(itemToEdit)
			self.weekDay.SetValue(occurs[1])
			self.description.SetValue(occurs[2])
			self.checkbox_1.SetValue(True if occurs[3] else False) 
			self.checkbox_2.SetValue(True if occurs[4] else False)
			self.checkbox_3.SetValue(True if occurs[5] else False)
			self.checkbox_4.SetValue(True if occurs[6] else False)
			self.checkbox_5.SetValue(True if occurs[7] else False)

			# Stores informations about description and alarms fields to check if they were changed
			self.originalDescription = occurs[2]
			self.checkbox_1_Original = self.checkbox_1.GetValue()
			self.checkbox_2_Original = self.checkbox_2.GetValue()
			self.checkbox_3_Original = self.checkbox_3.GetValue()
			self.checkbox_4_Original = self.checkbox_4.GetValue()
			self.checkbox_5_Original = self.checkbox_5.GetValue()

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
		if titleAddEd == _("Add"):
			# Conecting to database
			what = "*"
			find = "data= " + str(dateToSearch)
			occurs = manageDatabase.findItem(what, find, all=False)
			if occurs != None:
				self.description.SetValue(occurs[2])
				self.checkbox_1.SetValue(True if occurs[3] else False)
				self.checkbox_2.SetValue(True if occurs[4] else False)
				self.checkbox_3.SetValue(True if occurs[5] else False)
				self.checkbox_4.SetValue(True if occurs[6] else False)
				self.checkbox_5.SetValue(True if occurs[7] else False)
			else:
				self.description.SetValue("")
				self.checkbox_1.SetValue(False)
				self.checkbox_2.SetValue(False)
				self.checkbox_3.SetValue(False)
				self.checkbox_4.SetValue(False)
				self.checkbox_5.SetValue(False)

	def onOk(self, event):
		# signals wich exit type
		self.exitType = "OK"
		self.changesEnd()

	def changesEnd(self):
		global itemToEdit
		global titleAddEd
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
			if titleAddEd == _("Edit") and self.dateToSave == itemToEdit:
				dlg = wx.MessageDialog( self, _("You have deleted the appointment description. Do you want to delete the appointment?"), _("Agenda"), wx.YES_NO)
				if dlg.ShowModal()==wx.ID_YES: 
					# Conecting to database
					manageDatabase.removeItem(self.dateToSave)

					dlg2 = wx.MessageDialog( self, _("Appointment removed successfully!"), _("Agenda"), wx.OK)
					dlg2.ShowModal()
					dlg2.Destroy()
					self.Close()
					dlg.Destroy()
					loadAlarms(0)
				else:
					dlg.Destroy()
			# If option is Edit and original date is different from present date fields avoid edition.
			if titleAddEd == _("Edit") and self.dateToSave != itemToEdit:
				dlg = wx.MessageDialog( self, _("You have deleted the description and changed the date.\nIf you want to add a new appointment, press the Add button on main or search windows\nIf you want to delete an appointment, go to main or search windows, select the appointment and choose the remove button"), _("Agenda"), wx.OK)
				dlg.ShowModal() 
				dlg.Destroy()
				self.Close()
				event.Skip()
				return

			# If we are in the option Add and description field is empty, go back to the Add window
			if titleAddEd == _("Add"):
				dlg = wx.MessageDialog( self, _("No description to the appointment"), _("Agenda"), wx.OK)
				dlg.ShowModal() 
				dlg.Destroy()
				return

		# If description is not blank, Capture alarm informations.
		self.alarmOneDay = self.checkbox_1.GetValue()
		self.alarmOneHour = self.checkbox_2.GetValue()
		self.alarm30Minutes = self.checkbox_3.GetValue()
		self.alarm15Minutes = self.checkbox_4.GetValue()
		self.alarmHourExact = self.checkbox_5.GetValue()

		# If any alarm was set, set also alarm for exact hour.
		if self.alarmOneDay or self.alarmOneHour or self.alarm30Minutes or self.alarm15Minutes:
			self.alarmHourExact = True

		# Check if exists any appointement for this date and hour. If exist ask if it is to update
		# Conecting to database
		what = "*"
		find = "data= " + str(self.dateToSave)
		line = manageDatabase.findItem(what, find, all=False)
		if line != None:
			# If database returns some records, so exist appointment for this date/hour
			dlg = wx.MessageDialog( self, _("Informations for this date and hour already exists on agenda. Do you want to replace original informations?"), _("Agenda"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES: 
				# Conecting to database
				dbAgenda = sqlite3.connect(dirDatabase)
				dbCursor = dbAgenda.cursor()
				dbCursor.execute("""
					update agenda
					set diadasemana=?, descricao=?, alarmedia = ?, alarmehora = ?, alarmemeiahora = ?, alarmequartodehora = ?, alarmehoraexata = ?, periodicidade = ?
					where data=?
					""", (self.weekToSave, self.descriptionToSave, self.alarmOneDay, self.alarmOneHour, self.alarm30Minutes, self.alarm15Minutes, self.alarmHourExact,	'Indefinido', self.dateToSave))
				dbAgenda.commit()
				dbAgenda.close()
				dlg2 = wx.MessageDialog( self, _("Record updated successfully!"), _("Agenda"), wx.OK)
				dlg2.ShowModal()
				dlg2.Destroy()
				self.Destroy()
				loadAlarms(0)

				# Check last appointment to remove
				if self.dateToSave != itemToEdit:
					# Conecting to database
					what = "*"
					find = "data= " + str(self.itemToEdit)
					occurs = manageDatabase.findItem(what, find, all=False)
					if occurs != None:
						# Conecting to database
						manageDatabase.removeItem(itemToEdit)

			dlg.Destroy()
			loadAlarms(0)
		else:
				# Conecting to database
			dbAgenda = sqlite3.connect(dirDatabase)
			dbCursor = dbAgenda.cursor()
			dbCursor.execute("""
				insert into agenda values (?, ?, ?, ?, ?, ?, ?, ?, ?)
				""", (self.dateToSave, self.weekToSave, self.descriptionToSave, self.alarmOneDay, self.alarmOneHour, self.alarm30Minutes, self.alarm15Minutes, self.alarmHourExact, 'indefinido'))
			dbAgenda.commit()
			dbAgenda.close()
			dlg = wx.MessageDialog( self, _("Record saved successfully!"), _("Agenda"), wx.OK)
			dlg.ShowModal()
			dlg.Destroy()
			self.Destroy()
			loadAlarms(0)
			# If we are editing and the date or hour are different from saved, remove the old record
			if titleAddEd == _("Edit") and self.dateToSave != itemToEdit: 
				# Conecting to database
				manageDatabase.removeItem(itemToEdit)

			self.Close()
			self.Destroy()
			loadAlarms(0)

	def OnCancel(self, event):
		global itemToEdit
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
			flagIsChanged =(self.dateToSave !=itemToEdit) 

			# Gets description field
			flagIsChanged |= (self.description.GetValue() != self.originalDescription)

			# Gets alarms informations
			flagIsChanged |= (self.checkbox_1.GetValue() != self.checkbox_1_Original)
			flagIsChanged |= (self.checkbox_2.GetValue() != self.checkbox_2_Original)
			flagIsChanged |= (self.checkbox_3.GetValue() != self.checkbox_3_Original)
			flagIsChanged |= (self.checkbox_4.GetValue() != self.checkbox_4_Original)
			flagIsChanged |= (self.checkbox_5.GetValue() != self.checkbox_5_Original)

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


class searchWindow(wx.Dialog):
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Title of search window
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

		# Specify the search type
		self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Type of search:"))
		sizer_1.Add(self.label_1, 0, 0, 0)

		# The various search type
		self.comboSearchType = wx.ComboBox(self, wx.ID_ANY, choices=[_("Search by text"), _("Next 7 days"), _("Next 30 days"), _("Date range")], style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.comboSearchType.SetSelection(0)
		sizer_1.Add(self.comboSearchType, 0, 0, 0)

		# Asking user to enter the text to search
		self.label_2 = wx.StaticText(self, wx.ID_ANY, _("Enter the text to search:"))
		sizer_1.Add(self.label_2, 0, 0, 0)

		self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "")
		sizer_1.Add(self.text_ctrl_1, 0, 0, 0)

		sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

		# Day of initial date
		self.label_3 = wx.StaticText(self, wx.ID_ANY, _("Initial date: Day:"))
		sizer_3.Add(self.label_3, 0, 0, 0)

		self.spinInitialDay = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=31)
		self.spinInitialDay.SetValue(int(self.currentDay))
		sizer_3.Add(self.spinInitialDay, 0, 0, 0)

		self.label_4 = wx.StaticText(self, wx.ID_ANY, _("Month:"))
		sizer_3.Add(self.label_4, 0, 0, 0)

		self.ComboInitialMonth = wx.ComboBox(self, wx.ID_ANY, choices = months, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.ComboInitialMonth.SetSelection(12-int(self.currentMonth))
		sizer_3.Add(self.ComboInitialMonth, 0, 0, 0)

		self.label_5 = wx.StaticText(self, wx.ID_ANY, _("Year:"))
		sizer_3.Add(self.label_5, 0, 0, 0)

		self.spinInitialYear = wx.SpinCtrl(self, wx.ID_ANY, "1970", min=1970, max=2050)
		self.spinInitialYear.SetValue(int(self.currentYear))
		sizer_3.Add(self.spinInitialYear, 0, 0, 0)

		sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

		# Day of final date
		self.label_6 = wx.StaticText(self, wx.ID_ANY, _("Final date: Day:"))
		sizer_4.Add(self.label_6, 0, 0, 0)

		self.spinFinalDay = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=31)
		self.spinFinalDay.SetValue(int(self.currentDay))
		sizer_4.Add(self.spinFinalDay, 0, 0, 0)

		self.label_7 = wx.StaticText(self, wx.ID_ANY, _("Month:"))
		sizer_4.Add(self.label_7, 0, 0, 0)

		self.ComboFinalMonth = wx.ComboBox(self, wx.ID_ANY, choices = months, style=wx.CB_DROPDOWN|wx.CB_READONLY)
		self.ComboFinalMonth.SetSelection(12-int(self.currentMonth))
		sizer_4.Add(self.ComboFinalMonth, 0, 0, 0)

		self.label_8 = wx.StaticText(self, wx.ID_ANY, _("Year:"))
		sizer_4.Add(self.label_8, 0, 0, 0)

		self.spinFinalYear = wx.SpinCtrl(self, wx.ID_ANY, "1970", min=1970, max=2050)
		self.spinFinalYear.SetValue(int(self.currentYear))
		sizer_4.Add(self.spinFinalYear, 0, 0, 0)

		# Label of button to execute the search
		self.button_1 = wx.Button(self, wx.ID_ANY, _("&Search"))
		self.button_1.SetDefault()
		sizer_1.Add(self.button_1, 0, 0, 0)

		# Label of the list were the itens found will land
		self.label_9 = wx.StaticText(self, wx.ID_ANY, _("Items found:"))
		sizer_1.Add(self.label_9, 0, 0, 0)

		self.currentItemsList = wx.ListCtrl(self, wx.ID_ANY, size = (500, 200), style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		self.currentItemsList.AppendColumn(_("Date/Hour"), format=wx.LIST_FORMAT_LEFT, width = -1)
		self.currentItemsList.AppendColumn("Compromisso:", format=wx.LIST_FORMAT_LEFT, width = -1)
		self.flagRecordExists = False
		sizer_1.Add(self.currentItemsList, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.ButtonAdd = wx.Button(self, wx.ID_ANY, _("&Add"))
		sizer_2.Add(self.ButtonAdd, 0, 0, 0)

		self.ButtonEdit = wx.Button(self, wx.ID_ANY, _("&Edit"))
		sizer_2.Add(self.ButtonEdit, 0, 0, 0)

		self.ButtonRemove = wx.Button(self, wx.ID_ANY, _("&Remove"))
		sizer_2.Add(self.ButtonRemove, 0, 0, 0)

		# Label of button to remove all appointments
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
		self.lastSearch=''
		now = datetime.datetime.now()

		flagquery = 0
		SearchType = self.comboSearchType.GetValue()
		if SearchType == _("Search by text"):
			textToSearch = self.text_ctrl_1.GetValue()
			if len(textToSearch) == 0:
				# If the text to search is empty notifies the user
				dlg = wx.MessageDialog( self, _("Insert what to search or choose another type of search."), _("Agenda"), wx.OK)
				dlg.ShowModal() 
				dlg.Destroy()
				return
			else:	 
				flagquery = 1
				textToSearch_upper = "%" + textToSearch.upper() + "%"
				# Conecting to database
				what = "*"
				find = "upper(descricao) like '"+textToSearch_upper+"' order by data asc"
				self.lastSearch="upper(descricao) like '"+textToSearch_upper+"'"
		elif SearchType==_("Next 7 days"):
			# Search on the Next 7 days
			flagquery = 1
			nextDays = now + datetime.timedelta(days=+8)
			startDay = now + datetime.timedelta(days=+1)
			startDate = int(startDay.strftime ('%Y%m%d') + '0000')
			finalDate  = int(nextDays.strftime ('%Y%m%d') + '2359')
			# Conecting to database
			what = "*"
			find = "data>= " + str(startDate) + " and data<= " + str(finalDate) + " order by data asc"
			self.lastSearch='data>='+str(startDate)+' and data<='+str(finalDate)
		elif SearchType==_("Next 30 days"):
			# Search on the Next 30 days
			flagquery = 1
			nextDays = now + datetime.timedelta(days=+31)
			startDay = now + datetime.timedelta(days=+1)
			startDate = int(startDay.strftime ('%Y%m%d') + '0000')
			finalDate  = int(nextDays.strftime ('%Y%m%d') + '2359')
			# Conecting to database
			what = "*"
			find = "data>= " + str(startDate) + " and data<= " + str(finalDate) + " order by data asc"

			self.lastSearch='data>='+str(startDate)+' and data<='+str(finalDate)
		elif SearchType == _("Date range"):
			flagquery = 1
			# Gets the date fields to make the search
			startYearToSearch = str(self.spinInitialYear.GetValue())
			monthToSearchStr = self.ComboInitialMonth.GetValue()
			startMonthToSearch = '%02d' % (12-months.index(monthToSearchStr))
			startDayToSearch = '%02d' % self.spinInitialDay.GetValue()
			startDateToSearch = int(startYearToSearch + startMonthToSearch + startDayToSearch + "0000")

			finalYearToSearch = str(self.spinFinalYear.GetValue())
			monthToSearchStr = self.ComboFinalMonth.GetValue()
			finalMonthToSearch = '%02d' % (12-months.index(monthToSearchStr))
			finalDayToSearch = '%02d' % self.spinFinalDay.GetValue()
			finalDateToSearch = int(finalYearToSearch + finalMonthToSearch + finalDayToSearch + "2359")

			if finalDateToSearch<startDateToSearch:
				dlg = wx.MessageDialog( self, _("The end date must be equal or after the start date."), _("Agenda"), wx.OK)
				dlg.ShowModal() 
				dlg.Destroy()
				return

			# Conecting to database
			what = "*"
			find = "data>= " + str(startDateToSearch) + " and data<= " + str(finalDateToSearch) + " order by data asc"

			self.lastSearch = "data>=" +str(startDateToSearch) + " and data<=" + str(finalDateToSearch)

		if flagquery==1:   # Case some query was started loads from database
			occurs = manageDatabase.findItem(what, find, all=True)

		# Clear the listbox
		self.currentItemsList.ClearAll()
		self.currentItemsList.AppendColumn(_("Date/Hour"), format=wx.LIST_FORMAT_LEFT, width = 100)
		self.currentItemsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width = 400)
		self.dayOfToday = ""
		self.dayOfTomorrow = ""
		self.flagRecordExists=False
		if len(occurs) != 0:
			self.flagRecordExists=True
			# Items were found, so fill the listbox with them
			now = datetime.datetime.now()
			tomorrow = now + datetime.timedelta(days=+1)
			self.dayOfToday = datetime.datetime.strftime(now, '%Y%m%d')
			self.dayOfTomorrow = datetime.datetime.strftime(tomorrow, '%Y%m%d')
			i=0
			for tableLine in occurs:
				readDate = str(tableLine[0])
				textToShow = ""
				if readDate[:8] == self.dayOfToday:
					textToShow = _("Today")
				elif readDate[:8] == self.dayOfTomorrow:
					textToShow = _("Tomorrow")
				else:
					weekToShow = weekDays[datetime.date (int(readDate[:4]),int(readDate[4:6]),int(readDate[6:8])) .weekday()]
					textToShow = weekToShow + ", " + readDate[6:8] + "/" + readDate[4:6] + "/" + readDate[:4]
				self.currentItemsList.InsertItem(i, textToShow + ", " + readDate[8:10] + ":" + readDate[10:12])
				self.currentItemsList.SetItem(i, 1,tableLine[2])
				i+=1
			self.label_9.SetLabel(str(self.currentItemsList.GetItemCount()) + _("Items found:"))
		else:
			self.lastSearch = ""
			self.label_9.SetLabel(_("No items found:"))
		self.currentItemsList.SetFocus()
		self.currentItemsList.Focus(0)
		self.currentItemsList.Select(0)

	def OnAddSearch(self, event):
		global titleAddEd, itemToEdit
		titleAddEd = _("Add")
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

		itemToEdit = int(dateToEdit + hour)
		dialogAdd = DlgAddEdit(None)
		dialogAdd.ShowModal()
		dialogAdd.Destroy()
		self.executeSearch(event)
		event.Skip()

	def executeEdit(self, event):
		global titleAddEd
		titleAddEd = _("Edit")
		global itemToEdit
		# The variable should contain the details of appointment to edit
		if self.flagRecordExists:
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

			itemToEdit = int(dateToEdit + hour)
			dialogEdit = DlgAddEdit(None)
			dialogEdit.ShowModal()
			dialogEdit.Destroy()
		else:
			dlg = wx.MessageDialog(None, _("No appointment selected to edit..."), _("Agenda"), wx.OK)
			dlg.ShowModal() 
			dlg.Destroy()
		self.executeSearch(event)
		event.Skip()

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
			dlg = wx.MessageDialog(self, (_("Do you really want to remove the  item: ") + strItemToRemoveMsg + "?"), _("Agenda"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES: 
				# Conecting to database
				manageDatabase.removeItem(itemToRemove)
				dlg2 = wx.MessageDialog( self, _("Appointment removed successfully!"), _("Agenda"), wx.OK)
				dlg2.ShowModal()
				dlg2.Destroy()
				self.executeSearch(event)
				loadAlarms(0)
		else:
			dlg = wx.MessageDialog(None, _("No appointment selected to delete"), _("Agenda"), wx.OK)
			dlg.ShowModal() 
			dlg.Destroy()
		event.Skip()

	def onDeleteAll(self, event):
		if self.lastSearch == "":
			dlg = wx.MessageDialog(None, _("No itens to delete. Please, you need search something to delete all itens."), _("Agenda"), wx.OK)
			dlg.ShowModal() 
			dlg.Destroy()
		else:
			dlg = wx.MessageDialog(self, _("Do you really want to delete all itens found?"), _("Agenda"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES: 
				# Conecting to database
				manageDatabase.removeItem(self.lastSearch)

				dlg2 = wx.MessageDialog( self, _("All appointments deleted successfully!"), _("Agenda"), wx.OK)
				dlg2.ShowModal()
				dlg2.Destroy()
				self.executeSearch(event)
				loadAlarms(0)

	def OnCancel2(self, event):
		self.Close()
		event.Skip()

class manageDatabase():
	def createDatabase():
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

	def removeItem(itemToRemove):
		itemToRemove = str(itemToRemove)
		if itemToRemove[0].isalpha():
			query = "delete from agenda where " + itemToRemove
		else:
			query = "delete from agenda where data= " + itemToRemove
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbCursor.execute(query)
		dbAgenda.commit()
		dbAgenda.close()

	def findItem(what, itemToFind, all):
		query = "select " + what + " from agenda where " + itemToFind
		dbAgenda = sqlite3.connect(dirDatabase)
		dbCursor = dbAgenda.cursor()
		dbCursor.execute(query)
		if all == True:
			occurs = dbCursor.fetchall()
		else:
			occurs = dbCursor.fetchone()
		dbAgenda.close()
		return occurs
