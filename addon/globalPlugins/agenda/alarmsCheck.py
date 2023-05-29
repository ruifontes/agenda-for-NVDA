# -*- coding: UTF-8 -*-
# Agenda add-on: Interface to set alarms 
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# Copyright (C) 2022-2023 Abel Passos Jr. and Rui Fontes
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
import wx
import addonHandler

# To start the translation process
addonHandler.initTranslation()


class CheckAlarms(wx.Dialog):
	def __init__(self, checkVars, *args, **kwds):
		kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
		wx.Dialog.__init__(self, *args, **kwds)

		# Translators: Dialog title
		self.SetTitle(_("Alarms Setting"))

		sizer_1 = wx.BoxSizer(wx.VERTICAL)

		sizer_3 = wx.BoxSizer(wx.VERTICAL)
		sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

		# Translators: Title of group to select alarms
		label_1 = wx.StaticText(self, wx.ID_ANY, _("Select when alarms will be play"))
		sizer_3.Add(label_1, 0, 0, 0)

		# Load values of checkboxes 
		self.checkVars = checkVars
		self.checkOneDay = self.checkVars.checkOneDay
		self.checkOneHour = self.checkVars.checkOneHour
		self.checkHalfHour = self.checkVars.checkHalfHour
		self.checkFififteenMinutes = self.checkVars.checkFififteenMinutes
		self.checkExactTime = self.checkVars.checkExactTime

		# Translators: When the alarm is to play
		self.checkbox_1 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm for the day before"))
		self.checkbox_1.SetValue(self.checkOneDay)
		sizer_3.Add(self.checkbox_1, 0, 0, 0)

		# Translators: When the alarm is to play
		self.checkbox_2 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm to one hour before"))
		self.checkbox_2.SetValue(self.checkOneHour)
		sizer_3.Add(self.checkbox_2, 0, 0, 0)

		# Translators: When the alarm is to play
		self.checkbox_3 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm to half hour before"))
		self.checkbox_3.SetValue(self.checkHalfHour)
		sizer_3.Add(self.checkbox_3, 0, 0, self.checkHalfHour)

		# Translators: When the alarm is to play
		self.checkbox_4 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm to 15 minutes before"))
		self.checkbox_4.SetValue(self.checkFififteenMinutes)
		sizer_3.Add(self.checkbox_4, 0, 0, 0)

		# Translators: When the alarm is to play
		self.checkbox_5 = wx.CheckBox(self, wx.ID_ANY, _("Set alarm to the exact hour"))
		self.checkbox_5.SetValue(self.checkExactTime)
		sizer_3.Add(self.checkbox_5, 0, 0, 0)

		sizer_2 = wx.StdDialogButtonSizer()
		sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

		self.button_OK = wx.Button(self, wx.ID_OK)
		self.button_OK.SetDefault()
		sizer_2.Add(self.button_OK, 0, 0, 0)

		self.button_CANCEL = wx.Button(self, wx.ID_CANCEL)
		sizer_2.AddButton(self.button_CANCEL)

		sizer_2.Realize()
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)

		self.SetAffirmativeId(self.button_OK.GetId())
		self.SetEscapeId(self.button_CANCEL.GetId())

		self.Layout()
		self.CentreOnScreen()

		self.Bind(wx.EVT_BUTTON, self.OnOk, self.button_OK)

	def OnOk (self, event):
		self.checkVars.checkOneDay = self.checkbox_1.GetValue()
		self.checkVars.checkOneHour = self.checkbox_2.GetValue()
		self.checkVars.checkHalfHour = self.checkbox_3.GetValue()
		self.checkVars.checkFififteenMinutes = self.checkbox_4.GetValue()
		self.checkVars.checkExactTime = self.checkbox_5.GetValue()
		event.Skip()
		return
