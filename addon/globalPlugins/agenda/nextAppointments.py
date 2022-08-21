# -*- coding: UTF-8 -*-
# Part of Agenda add-on
# Module for next appointements routines
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# import the necessary modules.
from .manageDatabase import *
from .varsConfig import * 
# Necessary For translation
addonHandler.initTranslation()

#Global variables
frequency = [_('None'), _("Daily"), _("Weekly"), _("Biweekly"), _("Monthly"), _("Twomonthly"), _("Threemontly"), _("Fourmontly"), _("Sixmonthly"), _("Anualy")]


class nextAppointments(wx.Dialog):
	global dirDatabase
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
				loadedItens += [[tableLine[0], textToShow + ", " + readDate[8:10] + ":" + readDate[10:12], tableLine[2]]]
		self.periodicityRegisters = manageDatabase.findRepeatIntervalDate(todayStart, tomorrowEnd, True, dirDatabase)
		if len(self.periodicityRegisters)>0:
			self.flagRecordExists=True
			for tableLine in self.periodicityRegisters:
				readDate = str(tableLine[1])
				textToShow = ""
				if readDate[:8] == self.dayOfToday:
					textToShow = _("Today")
				elif readDate[:8] == self.dayOfTomorrow:
					textToShow = _("Tomorrow")
				loadedItens += [[tableLine[1], textToShow + ", " + readDate[8:10] + ":" + readDate[10:12], frequency[tableLine[10]] +"; " + tableLine[3]]]

		if not self.flagRecordExists:
			self.label_1.SetLabel(_("No items found:"))
		else:
			# If It found registers, fill  into  listctrl
			loadedSorted = sorted(loadedItens)
			j = 0
			for x in loadedSorted:
				index = self.appointmentsList.InsertItem(j, x[1])
				self.appointmentsList.SetStringItem(index, 1,x[2])
				j+=1
			self.label_1.SetLabel(str(self.appointmentsList.GetItemCount()) + _("Items found:"))
		self.appointmentsList.SetFocus()
		self.appointmentsList.Focus(0)
		self.appointmentsList.Select(0)

	def OnOk(self, event):
		self.Destroy()
		event.Skip()

