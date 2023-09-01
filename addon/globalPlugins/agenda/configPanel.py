# -*- coding: UTF-8 -*-
# Module for Agenda add-on settings panel
# written by Abel Passos do Nascimento Jr. <abel.passos@gmail.com>, Rui Fontes <rui.fontes@tiflotecnia.com> and Ângelo Abrantes <ampa4374@gmail.com> and 
# Copyright (C) 2022-2023 Abel Passos Jr. and Rui Fontes
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Import the necessary modules
import os
import gui
from gui.settingsDialogs import NVDASettingsDialog, SettingsPanel
from gui import guiHelper
import wx
import globalVars
import config
from configobj import ConfigObj
import winsound
from .varsConfig import *
import addonHandler

# To start the translation process
addonHandler.initTranslation()

# Constants
dirDatabase = os.path.join(os.path.dirname(__file__), "agenda.db")
alarmSoundToUse = ""
soundToUse = ""

"""
def initConfiguration():
	confspec = {
		"show" : "boolean(default=True)",
		"days" : "integer(1, 30, default=1)",
		"alarmSoundToUse" : "string(default="")",
		"playSound" : "boolean(default=False)",
		"soundToUse" : "string(default="")",
		"calendar" : "string(default="")",
		"path" : "string(default="")",
		"altPath" : "string(default="")",
		"xx" : "string(default="")",
	}
	config.conf.spec["agenda"] = confspec
"""
initConfiguration()

# Read configuration on INI file to know how many days to include in next events
global nDays
nDays = 2
try:
	if config.conf["agenda"]["days"]:
		# Number of days to include in next events
		nDays = int(config.conf["agenda"]["days"])
except:
	pass

# Read configuration on INI file to know wich sound to use for alarm
#global alarmSoundToUse
try:
	if config.conf["agenda"]["alarmSoundToUse"]:
		# Sound to use for alarm
		alarmSoundToUse = config.conf["agenda"]["alarmSoundToUse"]
except:
	alarmSoundToUse = "ringing.wav"

# Read configuration on INI file to know if should play sound on nextEvents dialog
try:
	if config.conf["agenda"]["playSound"]:
		playSound = config.conf["agenda"]["playSound"]
except KeyError:
	playSound = False

# Read configuration on INI file to know wich sound to use
#global soundToUse
try:
	if config.conf["agenda"]["soundToUse"]:
		# Sound to use
		soundToUse = config.conf["agenda"]["soundToUse"]
except:
	soundToUse = "isrtime.wav"

# Read configuration on INI file to know wich calendar to use
from .varsConfig import calendars
global calendarToUse
calendarToUse = _("Gregorian (Default)")
try:
	if config.conf["agenda"]["calendar"]:
		# Calendar to use
		calendarToUse = calendars[int(config.conf["agenda"]["calendar"])]
except:
	pass

# Read configuration on INI file to know where are the agenda.db files...
dirDatabase = os.path.join(os.path.dirname(__file__), "agenda.db")
firstDatabase = ""
altDatabase = ""
indexDB = 0

try:
	if config.conf["agenda"]["xx"]:
		# index of agenda.db file to use
		indexDB = int(config.conf["agenda"]["xx"])
		if indexDB == 0:
			dirDatabase = 				config.conf["agenda"]["path"]
		else:
			dirDatabase = 				config.conf["agenda"]["altPath"]
		firstDatabase = config.conf["agenda"]["path"]
		altDatabase = config.conf["agenda"]["altPath"]
except:
	# Not registered, so use the default path
	pass


class AgendaSettingsPanel(gui.settingsDialogs.SettingsPanel):
	# Translators: Title of the Agenda settings dialog in the NVDA settings.
	title = _("Agenda")

	def makeSettings(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer = settingsSizer)

		# Translators: Checkbox name in the configuration dialog
		self.showNextAppointmentsWnd = wx.CheckBox(self, label = _("Show next appointments at startup"))
		self.showNextAppointmentsWnd.SetValue(bool(config.conf["agenda"]["show"]))
		settingsSizerHelper.addItem(self.showNextAppointmentsWnd)

		label_1 = wx.StaticText(self, wx.ID_ANY, _("Number of days in next events:"))
		settingsSizerHelper.addItem(label_1)
		# Translators: EditComboBox name in the configuration dialog to set the number of days included in the events notification
		self.days = wx.SpinCtrl(self, wx.ID_ANY, "1", min=1, max=30)
		self.days .SetValue(config.conf["agenda"]["days"])
		settingsSizerHelper.addItem(self.days)

		# Translators: Label of a  combobox used to choose the sound to use for alarm
		from . varsConfig import soundsList
		alarmSoundToUseLabel = _("&Sound for alarm")
		self.alarmSoundCB = sHelper.addLabeledControl(alarmSoundToUseLabel, wx.Choice, choices = soundsList, style = 0)
		# Set selection to the item set in configurations
		self.alarmSoundCB.SetSelection(soundsList.index(alarmSoundToUse))
		self.alarmSoundCB.Bind(wx.EVT_CHOICE, self.onSelectAlarmSound)

		# Translators: Checkbox name in the configuration dialog
		self.playSoundCB = wx.CheckBox(self, label = _("Play a sound if appointments today or tomorrow"))
		self.playSoundCB.SetValue(bool(config.conf["agenda"]["playSound"]))
		settingsSizerHelper.addItem(self.playSoundCB)
		self.playSoundCB.Bind(wx.EVT_CHECKBOX, self.updateFields)

		# Translators: Label of a  combobox used to choose the sound to use
		from . varsConfig import soundsList
		soundToUseLabel = _("&Sound to use")
		self.soundCB = sHelper.addLabeledControl(soundToUseLabel, wx.Choice, choices = soundsList, style = 0)
		# Set selection to the item set in configurations
		self.soundCB.SetSelection(soundsList.index(soundToUse))
		self.soundCB.Bind(wx.EVT_CHOICE, self.onSelectSound)
		if not self.playSoundCB.GetValue():
			self.soundCB.Hide()

		# Translators: Label of a  combobox used to choose the calendar to use
		from . varsConfig import calendars
		calendarLabel = _("&Calendar:")
		self.calendarCB = sHelper.addLabeledControl(calendarLabel, wx.Choice, choices = calendars, style = 0)
		# Set selection to the item set in configurations
		self.calendarCB.SetSelection(calendars.index(calendarToUse))

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

	def updateFields(self, evt):
		if self.playSoundCB.IsChecked():
			self.soundCB.Show()
		else:
			self.soundCB.Hide()

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

	def onSelectAlarmSound(self, evt):
		soundToUse = self.alarmSoundCB.GetStringSelection()
		ringFile = os.path.join(os.path.dirname(__file__), "sounds", soundToUse)
		winsound.PlaySound(ringFile, winsound.SND_FILENAME|winsound.SND_ASYNC)

	def onSelectSound(self, evt):
		soundToUse = self.soundCB.GetStringSelection()
		ringFile = os.path.join(os.path.dirname(__file__), "sounds", soundToUse)
		winsound.PlaySound(ringFile, winsound.SND_FILENAME|winsound.SND_ASYNC)

	def onSave (self):
		from . varsConfig import calendars
		global dirDatabase, indexDB, days, calendarToUse, soundToUse, alarmSoundToUse
		config.conf["agenda"]["show"] = self.showNextAppointmentsWnd.GetValue()
		config.conf["agenda"]["days"] = self.days.GetValue()
		config.conf["agenda"]["alarmSoundToUse"] = self.alarmSoundCB.GetStringSelection()
		config.conf["agenda"]["playSound"] = self.playSoundCB.GetValue()
		config.conf["agenda"]["soundToUse"] = self.soundCB.GetStringSelection()
		calendarToSave = self.calendarCB.GetStringSelection()
		if calendarToSave == pgettext("calendars", _("Gregorian (Default)")):
			calendarToSave = 0
		else:
			calendarToSave = 1
		config.conf["agenda"]["calendar"] = str(calendarToSave)
		config.conf["agenda"]["path"] = firstDatabase
		config.conf["agenda"]["altPath"] = altDatabase
		config.conf["agenda"]["xx"] = str(self.pathList.index(self.pathNameCB.GetStringSelection()))
		indexDB = self.pathNameCB.GetSelection()
		dirDatabase = self.pathList[indexDB]
		alarmSoundToUse = self.alarmSoundCB.GetStringSelection()
		soundToUse = self.soundCB.GetStringSelection()
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()
		#self.Hide()

	def onPanelActivated(self):
		# Deactivate all profile triggers and active profiles
		config.conf.disableProfileTriggers()
		self.Show()

	def onPanelDeactivated(self):
		# Reactivate profiles triggers
		config.conf.enableProfileTriggers()
		self.Hide()

	def terminate(self):
		super(AgendaSettingsPanel, self).terminate()
		self.onPanelDeactivated()

