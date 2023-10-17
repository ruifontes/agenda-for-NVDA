# -*- coding: UTF-8 -*-
# Module for next appointements routines of Agenda add-on
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# Copyright (C) 2022-2023 Abel Passos Jr. and Rui Fontes
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
from .manageDatabase import *
from .varsConfig import *
from .DlgAddEdit import DlgAddEdit
from .convertdate import persian
import winsound

# To start the translation process
addonHandler.initTranslation()

#Global variables
frequency = [_('None'), _("Daily"), _("Weekly"), _("Biweekly"), _("Monthly"), _("Twomonthly"), _("Threemontly"), _("Fourmontly"), _("Sixmonthly"), _("Anualy")]


class nextAppointments(wx.Dialog):
	global dirDatabase
	def __init__(self, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)
		# Translators: Dialog title
		self.SetTitle(_("Appointments for the next days"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		# Translators: List label
		self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Items found:"))
		sizer_1.Add(self.label_1, 0, 0, 0)

		self.appointmentsList = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
		# Translators: Column title
		self.appointmentsList.AppendColumn(_("Date/Hour"), format=wx.LIST_FORMAT_LEFT, width=100)
		# Translators: Column title
		self.appointmentsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width=400)
		sizer_1.Add(self.appointmentsList, 1, wx.EXPAND, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		# Translators: Button name to open the main dialog
		self.button_Open = wx.Button(self, wx.ID_ANY, _("&Open"))
		sizer_2.AddButton(self.button_Open)

		self.button_OK = wx.Button(self, wx.ID_OK)
		self.button_OK.SetDefault()
		sizer_2.AddButton(self.button_OK)

		sizer_2.Realize()
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		# Adding an ID for each keystroke event
		self.Delete = wx.Window.NewControlId()
		# Assigns to each keystroke ID a method to the associated event
		self.Bind(wx.EVT_MENU, self.executeRemove, id=self.Delete)
		# Assigns the keystrokes to the ID's
		accel_tbl = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_DELETE, self.Delete)])
		self.SetAcceleratorTable(accel_tbl)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.Bind(wx.EVT_BUTTON, self.OnOpen, self.button_Open)
		self.Bind(wx.EVT_BUTTON, self.OnOk, self.button_OK)
		self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.executeEdit, self.appointmentsList)

		self.Layout()
		self.CentreOnScreen()

		self.update()

	def update(self):
		from .configPanel import calendarToUse
		playSound = False
		# Define the date range to find appointements
		Now = datetime.datetime.now()
		todayStart = int(datetime.datetime.strftime(Now, '%Y%m%d')+'0000')
		# Check how many days should be included
		try:
			if config.conf["agenda"]["days"]:
				# Number of days to include in next events
				nDays = int(config.conf["agenda"]["days"])
		except:
			nDays = 2
		nextDays = Now + datetime.timedelta(days=nDays-1)
		tomorrowEnd = int(datetime.datetime.strftime(nextDays, '%Y%m%d')+'2359')
		# Conecting to database
		from .configPanel import dirDatabase
		what = "*"
		find = "data>= " + str(todayStart) + " and data<= " + str(tomorrowEnd)
		occurs = manageDatabase.findItem(what, find, dirDatabase, all=True)

		# Clear the listbox
		self.appointmentsList.ClearAll()
		self.appointmentsList.AppendColumn(_("Date/Hour"), format=wx.LIST_FORMAT_LEFT, width = 100)
		self.appointmentsList.AppendColumn(_("Appointment"), format=wx.LIST_FORMAT_LEFT, width = 400)
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
			# Items were found, so look for repetitions
			for tableLine in occurs:
				# check for periodic event to this appointement
				checkRepeat = _("No repeat")
				readDate = str(tableLine[0])
				textToShow = ""
				if readDate[:8] == self.dayOfToday:
					textToShow = _("Today")
					playSound = True
				elif readDate[:8] == self.dayOfTomorrow:
					textToShow = _("Tomorrow")
					playSound = True
				else:
					from .varsConfig import weekDays
					weekToShow = weekDays[datetime.date(int(readDate[:4]),int(readDate[4:6]),int(readDate[6:8])).weekday()] 
					if calendarToUse == _("Gregorian (Default)"):
						textToShow = weekToShow + ", " + readDate[6:8] + "/" + readDate[4:6] + "/" + readDate[:4] 
					else:
						persianDate = persian.from_gregorian(int(readDate[:4]), int(readDate[4:6]), int(readDate[6:8]))
						textToShow = weekToShow + ", " + str("%02d" % persianDate[2]) + "/" + str("%02d" % persianDate[1]) + "/" + str(persianDate[0])
				loadedItens += [[tableLine[0], textToShow + ", " + readDate[8:10] + ":" + readDate[10:12], tableLine[2]]]
		self.periodicityRegisters = manageDatabase.findRepeatIntervalDate(todayStart, tomorrowEnd, True, dirDatabase)
		if len(self.periodicityRegisters)>0:
			self.flagRecordExists=True
			for tableLine in self.periodicityRegisters:
				readDate = str(tableLine[1])
				textToShow = ""
				if readDate[:8] == self.dayOfToday:
					textToShow = _("Today")
					playSound = True
				elif readDate[:8] == self.dayOfTomorrow:
					textToShow = _("Tomorrow")
					playSound = True
				else:
					from .varsConfig import weekDays
					weekToShow = weekDays[datetime.date(int(readDate[:4]),int(readDate[4:6]),int(readDate[6:8])).weekday()] 
					if calendarToUse == _("Gregorian (Default)"):
						textToShow = weekToShow + ", " + readDate[6:8] + "/" + readDate[4:6] + "/" + readDate[:4] 
					else:
						persianDate = persian.from_gregorian(int(readDate[:4]), int(readDate[4:6]), int(readDate[6:8]))
						textToShow = weekToShow + ", " + str(persianDate[2]) + "/" + str('%02d' % (persianDate[1])) + "/" + str('%02d' % (persianDate[0]))
				loadedItens += [[tableLine[1], textToShow + ", " + readDate[8:10] + ":" + readDate[10:12], frequency[tableLine[10]] +"; " + tableLine[3]]]

		if not self.flagRecordExists:
			self.label_1.SetLabel(_("No items found:"))
		else:
			# If It found registers, fill  into  listctrl
			loadedSorted = sorted(loadedItens)
			j = 0
			for x in loadedSorted:
				index = self.appointmentsList.InsertItem(j, x[1])
				self.appointmentsList.SetItem(index, 1, x[2])
				j+=1
			self.label_1.SetLabel(str(self.appointmentsList.GetItemCount()) + _("Items found:"))
			self.appointmentsList.Focus(0)
			self.appointmentsList.Select(0)
		self.appointmentsList.SetFocus()
		from .configPanel import soundToUse
		if config.conf["agenda"]["playSound"] and playSound == True:
			ringFile = os.path.join(os.path.dirname(__file__), "sounds", soundToUse)
			winsound.PlaySound(ringFile, winsound.SND_FILENAME|winsound.SND_ASYNC)

	def executeEdit(self, event):
		global itemToEdit
		from . varsConfig import generalVars
		generalVars.titleAddEd = _("Edit")
		flagGoToEdit = False
		# The variable should contain the details of appointment to edit
		if self.flagRecordExists and self.appointmentsList.GetSelectedItemCount() != 0:
			# Get appointment details to make the date to edit
			strItemToEdit = self.appointmentsList.GetItemText(self.appointmentsList.GetFocusedItem(), 0)
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
				if calendarToUse == _("Persian"):
					gregorianDate = persian.to_gregorian(int(strItemToEdit[6:10]), int(strItemToEdit[3:5]), int(strItemToEdit[:2]))
					dateToEdit = str(gregorianDate[0]) + str('%02d' % (gregorianDate[1])) + str('%02d' % (gregorianDate[2]))

			generalVars.itemToEdit = int(dateToEdit + hour)
			flagGoToEdit = True
			for foundRepeatRegister  in self.periodicityRegisters:
				if foundRepeatRegister[1] == generalVars.itemToEdit:
					# Translators: Dialog to ask if it is to edit the first registry.
					dlg = wx.MessageDialog(self, _("You selected a periodic event. You can't edit a date inside on periodic event.\nInstead of, you need edit the original registry. Do you want to edit It?"), _("Edit periodic event"), wx.YES_NO)
					if dlg.ShowModal()==wx.ID_YES:
						generalVars.itemToEdit= foundRepeatRegister[0]
						break
					else:
						flagGoToEdit = False
						break

			if flagGoToEdit:
				dlgAdEd = DlgAddEdit(generalVars, self).ShowModal()
		else:
			# Translators: Inform that no event was selected...
			dlg = wx.MessageDialog(None, _("No appointment selected to edit..."), _("Agenda"), wx.OK)
			dlg.ShowModal() 
			dlg.Destroy()
		event.Skip()
		self.update()

	def executeRemove(self, event):
		# The variable should contain the details of appointment to remove
		if self.flagRecordExists and self.appointmentsList.GetSelectedItemCount() > 0:
			# Get appointments fields to create the date
			strItemToRemove = self.appointmentsList.GetItemText(self.appointmentsList.GetFocusedItem(), 0)
			strItemToRemoveMsg = self.appointmentsList.GetItemText(self.appointmentsList.GetFocusedItem(), 1)
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

				if calendarToUse == _("Persian"):
					gregorianDate = persian.to_gregorian(int(strItemToRemove[6:10]), int(strItemToRemove[3:5]), int(strItemToRemove[:2]))
					dateToRemove = str(gregorianDate[0]) + str('%02d' % (gregorianDate[1])) + str('%02d' % (gregorianDate[2]))

			itemToRemove= int(dateToRemove + hour)
			msgRemove = (_("Do you really want to remove the  item: ") + strItemToRemoveMsg + "?")
			for foundRepeatRegister  in self.periodicityRegisters:
				if foundRepeatRegister[1]==itemToRemove:
					originalDate = str(foundRepeatRegister[0])
					originalDateStr = originalDate[6:8]+'/'+originalDate[4:6]+'/'+originalDate[:4]+', '+originalDate[8:10]+':'+originalDate[10:12]+', '+foundRepeatRegister[3]
					# Translators: Asking to delete the original registry and not one single event...
					msgRemove = _("You can't remove just one periodic event. Instead of, you need remove the original registry. If you make this, alldates on this periodic event will be deleted.\nDo you want to delete the original register and all   dates of this {} event:\n{}?").format(frequency[foundRepeatRegister[10]], originalDateStr)
					itemToRemove= foundRepeatRegister[0]
					break
			# Translators: Confirm deletion
			dlg = wx.MessageDialog(self, msgRemove, _("Remove event"), wx.YES_NO)
			if dlg.ShowModal()==wx.ID_YES: 
				# Conecting to database
				from .configPanel import dirDatabase
				manageDatabase.removeItem(itemToRemove, dirDatabase)
				manageDatabase.removeRepeat(itemToRemove, dirDatabase)
				# Translators: Informative about event deletion
				dlg2 = wx.MessageDialog( self, _("Appointment removed successfully!"), _("Agenda"), wx.OK)
				dlg2.ShowModal()
				#self.Destroy()
				self.update()
		event.Skip()

	def OnOpen(self, event):
		self.Destroy()
		from . import MainWindow
		dialog0 = MainWindow(gui.mainFrame)
		if not dialog0.IsShown():
			gui.mainFrame.prePopup()
			dialog0.Show()
			gui.mainFrame.postPopup()
		event.Skip()

	def OnOk(self, event):
		self.Destroy()
		event.Skip()

